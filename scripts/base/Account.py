# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import Hotfix
import parent.C1
import parent.C2

import CustomClass

class Account(KBEngine.Proxy, Hotfix.Hotfix, parent.C1.C1, parent.C2.C2):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		Hotfix.Hotfix.__init__(self)
		parent.C1.C1.__init__(self)
		parent.C2.C2.__init__(self)
		
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		#KBEDebug.DEBUG_MSG(id, userArg)
		if userArg == Hotfix.TUArg_Hotfix:
			self.Hotfix_Update()
		
	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		KBEDebug.INFO_MSG("account[%i] entities enable. entityCall:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		KBEDebug.INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		KBEDebug.DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()

	def printCustomClass(self):
		KBEDebug.DEBUG_MSG("Account[%i].printCustomClass: %s" % (self.id, CustomClass.Get().printf()))
