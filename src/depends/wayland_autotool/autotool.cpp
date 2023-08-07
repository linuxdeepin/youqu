
// SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

// SPDX-License-Identifier: GPL-2.0-only

#include "autotool.h"
#include <unistd.h>
#include <linux/input-event-codes.h>

#include <QPushButton>
#include <QApplication>
#include <QClipboard>
#include <QDebug>
#include <QMimeData>
#include <QFile>
#include <QBuffer>
#include <QImageWriter>
#include <QByteArray>
#include <QUrl>
#include <QMutexLocker>
#include <QtConcurrent>
#include <QDesktopWidget>

#include <KWayland/Client/fakeinput.h>
#include <KWayland/Client/output.h>

AutoTool::AutoTool(QObject *parent)
    : QObject(parent)
{
    init();
}

AutoTool::~AutoTool()
{

}

void AutoTool::init()
{
    m_mimeData=new QMimeData();
    m_registry = new KWayland::Client::Registry(this);
    m_registry->create(KWayland::Client::ConnectionThread::fromApplication(this));
    m_registry->setup();
    connect(m_registry, &KWayland::Client::Registry::fakeInputAnnounced, this, [this] (quint32 name, quint32 version) {
       m_fakeInput = m_registry->createFakeInput(name, version, this);
       m_fakeInput->authenticate("wayland_autotool","NanJing AutoTestTool");
       //使光标焦点于当前桌面，否则剪贴板数据无法写入读取
       this->moveTo(0,0);
    });
    connect(m_registry, &KWayland::Client::Registry::seatAnnounced, this, [this] (quint32 name, quint32 version) {
       m_seat = m_registry->createSeat(name, version, this);
    });
    connect(m_registry, &KWayland::Client::Registry::ddeSeatAnnounced, this, [this] (quint32 name, quint32 version) {
       m_ddeSeat = m_registry->createDDESeat(name, version, this);
       m_ddePointer=m_ddeSeat->createDDePointer(this);
    });
    connect(m_registry, &KWayland::Client::Registry::dataControlDeviceManagerAnnounced, this, [this] (quint32 name, quint32 version) {
       m_dataControlDeviceManager = m_registry->createDataControlDeviceManager(name, version, this);
       if (m_dataControlDeviceManager != Q_NULLPTR)
       {
           m_dataControlSourceV1=m_dataControlDeviceManager->createDataSource(this);
           m_dataControlDeviceV1=m_dataControlDeviceManager->getDataDevice(m_seat, this);
           if (!m_dataControlSourceV1)
               return;
           if (!m_dataControlDeviceV1)
               return;
           connect(m_dataControlDeviceV1, &KWayland::Client::DataControlDeviceV1::dataOffered, this, [this](KWayland::Client::DataControlOfferV1* offer){
               qDebug() << "data offered";
               if (!offer)
                   return;

               if(m_mimeDataRead==nullptr)
               {
                   m_mimeDataRead=new QMimeData();
               }else {
                   delete m_mimeDataRead;
                   m_mimeDataRead=new QMimeData();
               }
               m_mimeDataRead->clear();

               QList<QString> mimeTypeList = offer->offeredMimeTypes();
               int mimeTypeCount = mimeTypeList.count();

               // 将所有的数据插入到mime data中
               static QMutex setMimeDataMutex;
               static int mimeTypeIndex = 0;
               mimeTypeIndex = 0;
               for (const QString &mimeType : mimeTypeList) {
                   int pipeFds[2];
                   if (pipe(pipeFds) != 0) {
                       qWarning() << "Create pipe failed.";
                       return;
                   }

                   // 根据mime类取数据，写入pipe中
                   offer->receive(mimeType, pipeFds[1]);
                   close(pipeFds[1]);
                   // 异步从pipe中读取数据写入mime data中
                   QtConcurrent::run([pipeFds, this, mimeType, mimeTypeCount] {
                       QFile readPipe;
                       if (readPipe.open(pipeFds[0], QIODevice::ReadOnly)) {
                           if (readPipe.isReadable()) {
                               const QByteArray &data = readPipe.readAll();
                               if (!data.isEmpty()) {
                                   // 需要加锁进行同步，否则可能会崩溃
                                   QMutexLocker locker(&setMimeDataMutex);
                                   m_mimeDataRead->setData(mimeType, data);
                               } else {
                                   qWarning() << "Pipe data is empty, mime type: " << mimeType;
                               }
                           } else {
                               qWarning() << "Pipe is not readable";
                           }
                       } else {
                           qWarning() << "Open pipe failed!";
                       }
                       close(pipeFds[0]);
                       if (++mimeTypeIndex >= mimeTypeCount) {
                           mimeTypeIndex = 0;
                       }
                   });
               }

           });
           //m_dataControlOfferV1=m_dataControlDeviceV1->offeredSelection();
           connect(m_dataControlSourceV1, &KWayland::Client::DataControlSourceV1::sendDataRequested,this,[this] (const QString &mimeType, qint32 fd) {
               //qDebug()<<"enter:"<<mimeType;
               QFile f;
               if (f.open(fd, QFile::WriteOnly, QFile::AutoCloseHandle)) {
                   QByteArray content=m_mimeData->text().toUtf8();
                   const QByteArray &ba = content;
                   f.write(ba);
                   f.close();
               }
            });

       }
    });

}
//void AutoTool::exit()
//{
//    if (m_mimeData !=nullptr)
//    {
//        delete m_mimeData;
//        m_mimeData=nullptr;
//    }
//    if (m_dataControlSourceV1 !=nullptr)
//    {
//        delete m_dataControlSourceV1;
//        m_dataControlSourceV1=nullptr;
//    }
//    if (m_dataControlDeviceV1 !=nullptr)
//    {
//        delete m_dataControlDeviceV1;
//        m_dataControlDeviceV1=nullptr;
//    }
//    if (m_dataControlDeviceManager !=nullptr)
//    {
//        delete m_dataControlDeviceManager;
//        m_dataControlDeviceManager=nullptr;
//    }
//    if (m_ddePointer !=nullptr)
//    {
//        delete m_ddePointer;
//        m_ddePointer=nullptr;
//    }
//    if (m_ddeSeat !=nullptr)
//    {
//        delete m_ddeSeat;
//        m_ddeSeat=nullptr;
//    }
//    if (m_seat !=nullptr)
//    {
//        delete m_seat;
//        m_seat=nullptr;
//    }
//    if (m_fakeInput !=nullptr)
//    {
//        delete m_fakeInput;
//        m_fakeInput=nullptr;
//    }
//    if (m_registry !=nullptr)
//    {
//        m_registry->destroy();
//        delete m_registry;
//        m_registry=nullptr;
//    }
//}

void AutoTool::click(QString method)
{
    if (method=="left")
    {
        m_fakeInput->requestPointerButtonClick(Qt::MouseButton::LeftButton);
    }else if (method=="right")
    {
        m_fakeInput->requestPointerButtonClick(Qt::MouseButton::RightButton);
    }else if (method=="middle")
    {
        m_fakeInput->requestPointerButtonClick(Qt::MouseButton::MiddleButton);
    }

}

void AutoTool::mouseDown(QString method)
{
    if (method=="left")
    {
        m_fakeInput->requestPointerButtonPress(Qt::MouseButton::LeftButton);
    }else if (method=="right")
    {
        m_fakeInput->requestPointerButtonPress(Qt::MouseButton::RightButton);
    }else if (method=="middle")
    {
        m_fakeInput->requestPointerButtonPress(Qt::MouseButton::MiddleButton);
    }
}

void AutoTool::mouseUp(QString method)
{
    if (method=="left")
    {
        m_fakeInput->requestPointerButtonRelease(Qt::MouseButton::LeftButton);
    }else if (method=="right")
    {
        m_fakeInput->requestPointerButtonRelease(Qt::MouseButton::RightButton);
    }else if (method=="middle")
    {
        m_fakeInput->requestPointerButtonRelease(Qt::MouseButton::MiddleButton);
    }
}

void AutoTool::moveTo(int x,int y)
{
    QPoint point(x,y);
    m_fakeInput->requestPointerMoveAbsolute(point);
}

QPointF AutoTool::getPos()
{
    return m_ddePointer->getGlobalPointerPos();
}

QPoint AutoTool::getSize()
{
    int width=QApplication::desktop()->width();
    int height=QApplication::desktop()->height();
    QPoint size(width,height);
    return size;
}

void AutoTool::keyDown(quint32 key)
{
    m_fakeInput->requestKeyboardKeyPress(key);
}

void AutoTool::keyUp(quint32 key)
{
    m_fakeInput->requestKeyboardKeyRelease(key);
}

void AutoTool::press(quint32 key)
{
    this->keyDown(key);
    usleep(10000);
    this->keyUp(key);
}

void AutoTool::vscroll(qreal delta)
{
    m_fakeInput->requestPointerAxis(Qt::Orientation::Vertical,delta);
}

void AutoTool::hscroll(qreal delta)
{
    m_fakeInput->requestPointerAxis(Qt::Orientation::Horizontal,delta);
}

void AutoTool::setText(QString text)
{
    if(m_mimeData==nullptr)
    {
        m_mimeData=new QMimeData();
    }else {
        delete m_mimeData;
        m_mimeData=new QMimeData();
    }
    m_mimeData->setText(text);
    for (const QString &format : m_mimeData->formats()) {
        // 如果是application/x-qt-image类型则需要提供image的全部类型, 比如image/png
        //qDebug()<<format;
        m_dataControlSourceV1->offer(format);
    }
    m_dataControlDeviceV1->setSelection(0, m_dataControlSourceV1);
}

QString AutoTool::getText(){
    qDebug()<<m_mimeDataRead->text();
    return m_mimeDataRead->text();
}


