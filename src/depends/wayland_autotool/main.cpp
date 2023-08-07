
// SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

// SPDX-License-Identifier: GPL-2.0-only

#include "autotool.h"
#include <QApplication>
#include <QDBusConnection>
#include <QDBusError>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    //建立到session bus的连接
    QDBusConnection connection = QDBusConnection::sessionBus();
    //在session bus上注册名为com.deepin.Autotool的服务
    if(!connection.registerService("com.deepin.Autotool"))
    {
        qDebug() << "error:" << connection.lastError().message();
        exit(-1);
    }

    AutoTool w;

    //注册名为/test/objects的对象，把类Object所有槽函数导出为object的method
    connection.registerObject("/com/deepin/Autotool", &w,QDBusConnection::ExportAllSlots);
    return a.exec();
}
