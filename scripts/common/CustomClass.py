# -*- coding: utf-8 -*-

import Hotfix
class CustomClass(Hotfix.Hotfix):
    def __init__(self):
        Hotfix.Hotfix.__init__(self)

    def printf(self):
        return 'vvvvvvvvvvvvvvvvvvvvv'

C = None
def Get():
    global C
    if C is None:
        C = CustomClass()
    return C