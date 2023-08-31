# coding=utf-8
# Name:         uos_pdu
# Description:  
# Author:       Xietian
# Date:         2023/8/31
import requests
from auto_uos.basic_functions import json_to_dict
import json

class Pdu():
    def __init__(self, ip):
        self.ip = ip

    def _login(self):
        r = requests.post(f'http://{self.ip}/login.json', json={"login":255,"userName":"YWRtaW4=","password":"YWRtaW4="})
        assert r.status_code == 200
        print(r.content.decode('u8'))

    def _logout(self):
        r = requests.post(f'http://{self.ip}/body_head.json', json={"logout":1})
        assert r.status_code == 200
        print(r.content.decode('u8'))

    def __enter__(self):
        self._login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._logout()

    def switch_state_get(self):
        """
        查询当前插口上电状态
        :return: list 0-断电 1-上电  顺序从离显示屏远的插口开始
        """
        r = requests.post(f'http://{self.ip}/home-page.json', json={"get" : 255})
        ret = json.loads(s=r.content.decode('u8'))
        print('插口1-4状态为', ret['socket'])
        return ret['socket']

    def switch_state_change(self, index, state):
        """
        改变某一个插口的上电状态
        :param index: 1，2，3，4
        :param state: 0-断电 1-上电
        :return:
        """
        r = requests.post(f'http://{self.ip}/home-page.json', json={"ctlbtn":index-1,"sta":state})
        ret = json.loads(s=r.content.decode('u8'))
        print(f'插口{index}状态改为{"上电" if state==1 else "断电"}')
        return ret['socket']

    def switch_all_off(self):
        """
        将所有插口断电
        :return:
        """
        r = requests.post(f'http://{self.ip}/home-page.json', json={"ctlbtn":255,"sta":0})
        assert r.status_code == 200

    def switch_all_on(self):
        """
        将所有插口上电
        :return:
        """
        r = requests.post(f'http://{self.ip}/home-page.json', json={"ctlbtn":255,"sta":1})
        assert r.status_code == 200


if __name__ == '__main__':
    with Pdu('10.20.52.176') as api:
        # 查看插口当前上电状态
        # api.switch_state_get()
        # 改变某一个插口的上电状态
        # api.switch_state_change(1, 0)
        # 将所有插口断电
        # api.switch_all_off()
        # 将所有插口上电
        # api.switch_all_on()
        pass
