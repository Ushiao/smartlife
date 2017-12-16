# -*- coding:utf-8 -*-

from flask import request, make_response

from . import main
from .actions import Action

action = Action()


@main.route('/', methods = ['POST'])
def web():
    """
    a website api
    """
    # Request Authentication
    if request.method == "POST":
        return action.do(request.form.get('msg'))
    return ""

