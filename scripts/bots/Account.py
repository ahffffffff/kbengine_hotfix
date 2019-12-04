# -*- coding: utf-8 -*-
import KBEngine
import copy
import KBEDebug

class Account(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		KBEDebug.DEBUG_MSG("Account::__init__:%s." % (self.__dict__))

