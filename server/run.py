# -*- coding:utf-8 -*-

from flask import Flask
from app import create_app

app = create_app(True)

if __name__ == "__main__":
    app.run("0.0.0.0", threaded=True)
    
