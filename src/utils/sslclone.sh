#!/bin/bash
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

CODE_PATH=$1
URL=$2
USER=$3
PASSWORD=$4
BRANCH=$5
DEPTH=$6

if [ "${BRANCH}" != "" ]; then
    BRANCH="-b ${BRANCH}"
fi

if [ "${DEPTH}" != "" ]; then
    DEPTH="--depth ${DEPTH}"
fi

cd ${CODE_PATH}
expect -c "spawn git clone ${URL} ${BRANCH} ${DEPTH}; expect \"*Username*\" { send \"${USER}\n\"; exp_continue } \"*Password*\" { send \"${PASSWORD}\n\" }; interact"