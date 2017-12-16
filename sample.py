#! /usr/bin/python
# -*- coding:utf-8 -*-

import requests as req

data = {"msg": "客厅模式"}
res = req.post("http://127.0.0.1:5000/smartlife/", data=data)
print(res.text)
