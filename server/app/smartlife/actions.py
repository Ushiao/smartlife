#! /usr/bin/python
# -*- coding:utf-8 -*-

import json
import time
from os import path

strint2bin = lambda i: "%04d"%int(bin(int(i, 10)).replace("0b", ""))
strbin2int = lambda i: int(str(i), 2)

rf_buttons = {"厨房灯": strint2bin("1"),
              "书房灯": strint2bin("2"),
              "电视墙灯": strint2bin("4"),
              "厨房灯开": strint2bin("9"),
              "书房灯开": strint2bin("10"),
              "书房灯关": strint2bin("11"),
              "电视墙灯开": strint2bin("12"),
              "厨房灯关": strint2bin("13"),
              "电视墙灯关": strint2bin("14"),
              "全关": strint2bin("15")}

wifi_buttons = {"餐厅灯开关": (0, None),
                "餐厅灯开": (0, "1"),
                "餐厅灯关": (0, "0"),
                "餐厅射灯开关": (1, None),
                "餐厅射灯开": (1, "1"),
                "餐厅射灯关": (1, "0"),
                "客厅灯开关": (2, None),
                "客厅灯开": (2, "1"),
                "客厅灯关": (2, "0"),
                "客厅射灯开关": (3, None),
                "客厅射灯开": (3, "1"),
                "客厅射灯关": (3, "0")}

modes = {
         "餐厅模式": [["餐厅灯开", "餐厅射灯开", "客厅灯关", "客厅射灯关"],
                 ["电视墙灯关"]],
         "客厅模式": [["餐厅灯关", "餐厅射灯关", "客厅灯开", "客厅射灯开"],
                 ["电视墙灯开", "电视墙灯关","电视墙灯开"]],
         "会客模式": [["餐厅灯开", "餐厅射灯开", "客厅灯开", "客厅射灯开"],
                 ["电视墙灯开", "电视墙灯关","电视墙灯开"]],
         "普通模式": [["餐厅灯开", "餐厅射灯关", "客厅灯开", "客厅射灯关"],
                 ["电视墙灯关"]],
         "观影模式": [["餐厅灯关", "餐厅射灯关", "客厅灯关", "客厅射灯关"],
                 ["电视墙灯开", "电视墙灯关","电视墙灯开"]],
         "餐厅灯": [["餐厅灯开关"], None],
         "餐厅射灯": [["餐厅射灯开关"], None],
         "客厅灯": [["客厅灯开关"], None],
         "客厅射灯": [["客厅射灯开关"], None],
         "电视墙灯": [None, ["电视墙灯"]],
         "书房灯": [None, ["书房灯"]],
         "厨房灯": [None, ["厨房灯"]],
         "全关": [["餐厅灯关", "餐厅射灯关", "客厅灯关", "客厅射灯关"], ["全关"]]}


class Action(object):

    def __init__(self):
        here = path.abspath(path.dirname(__file__))
        self.filepath = path.join(here, "static", "light.html")
        if not path.exists(self.filepath):
            f = open(self.filepath, "w")
            f.write(json.dumps({"rf":[["0000"], 0], "wifi":["0000", 0]}))
            f.close()

    def do(self, mode):
        response = None
        time_now = int(time.time())
        with open(self.filepath, 'r') as inf:
            status = json.load(inf)
        if mode in modes:
            wifi, rf = modes[mode]
            if wifi is not None:
                status_list = [s for s in status['wifi'][0]]
                for btn_name in wifi:
                    btn, value = wifi_buttons[btn_name]
                    status_value = status['wifi'][0][btn]
                    if value is None:
                        status_list[btn] = "0" if status_value == "1" else "1"
                    else:
                        status_list[btn] = value
                status['wifi'][0] = ''.join(status_list)
                status['wifi'][1] = time_now

            if rf is not None:
                btn = [rf_buttons[btn_name] for btn_name in rf]
                status['rf'][0] = btn
                status['rf'][1] = time_now

            response = """{"text":u"LightControl"}"""
            with open(self.filepath, 'w') as outf:
                outf.write(json.dumps(status))
        return response if response is not None else ""

if __name__ == "__main__":
    f = Action()
    print(f.do("会客模式"))
