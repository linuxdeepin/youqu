
// SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

// SPDX-License-Identifier: GPL-2.0-only

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMap>
#include <QString>
#include <KWayland/Client/registry.h>
#include <KWayland/Client/connection_thread.h>
#include <KWayland/Client/plasmawindowmanagement.h>
#include <KWayland/Client/ddeseat.h>
#include <KWayland/Client/textinput.h>
#include <KWayland/Client/datadevice.h>
#include <KWayland/Client/datadevicemanager.h>
#include <KWayland/Client/datacontrolsource.h>
#include <KWayland/Client/datacontroldevice.h>
#include <KWayland/Client/datacontroldevicemanager.h>
#include <KWayland/Client/datacontroloffer.h>
#include <QMimeData>
//#include <linux/input-event-codes.h>

class AutoTool : public QObject
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "com.deepin.Autotool")


public slots:
    //鼠标点击分为左、中、右键点击
    void click(QString method);
    //鼠标按键按下分为左、中、右键按下
    void mouseDown(QString method);
    //鼠标按键抬起分为左、中、右键抬起
    void mouseUp(QString method);
    //移动鼠标至绝对坐标x，y屏幕左上角为原点，向右为X正轴，向下为Y正轴
    void moveTo(int x,int y);
    //获取鼠标当前位置的绝对坐标
    QPointF getPos();
    //获取屏幕分辨率
    QPoint getSize();

    //按键按下 key为/usr/include/linux/input-event-codes.h定义值
    void keyDown(quint32 key);
    //按键抬起 key为/usr/include/linux/input-event-codes.h定义值
    void keyUp(quint32 key);
    //按键按下抬起 key为/usr/include/linux/input-event-codes.h定义值
    void press(quint32 key);
    //垂直滚动条滚动
    void vscroll(qreal delta);
    //水平滚动条滚动
    void hscroll(qreal delta);
    //向剪贴板写入文字，目前写入的文字可用于Ctrl+V粘贴，但剪贴板中并不会显示
    void setText(QString text);
    //从剪贴板获取文字
    QString getText();

    void init();
    //void exit();


public:
    AutoTool(QObject *parent = nullptr);
    ~AutoTool();
    KWayland::Client::Registry * m_registry = Q_NULLPTR;
    //kwayland键鼠操控类
    KWayland::Client::FakeInput *m_fakeInput = Q_NULLPTR;
    KWayland::Client::DDESeat *m_ddeSeat = Q_NULLPTR;
    KWayland::Client::Seat *m_seat = Q_NULLPTR;
    //光标位置获取相关类
    KWayland::Client::DDEPointer *m_ddePointer= Q_NULLPTR;
    //剪贴板数据相关类
    KWayland::Client::DataControlDeviceV1 *m_dataControlDeviceV1=Q_NULLPTR;
    KWayland::Client::DataControlSourceV1 *m_dataControlSourceV1=Q_NULLPTR;
    //KWayland::Client::DataControlOfferV1 *m_dataControlOfferV1=Q_NULLPTR;

    QMimeData *m_mimeData=Q_NULLPTR;
    QMimeData *m_mimeDataRead=Q_NULLPTR;
    KWayland::Client::DataControlDeviceManager *m_dataControlDeviceManager = Q_NULLPTR;
};

#endif // MAINWINDOW_H
