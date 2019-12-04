# -*- coding: utf-8 -*-

#########################################################
# 所有要使用热更功能的 .py 文件，暂时在文件内只允许定义一个 class
#########################################################

import KBEngine
import KBEDebug
import sys
import inspect
import importlib

# 需要 skip 的引擎类
_skip_class = {
    'Proxy',
    'Entity',
    'object',
    # 'Hotfix' # 允许自己更新自己 
}

TUArg_Hotfix = 999  # Hotfix ##### 热更期间不要改这个值

def getHotfixList(component = KBEngine.component):
    hotdata = None
    if component == 'baseapp':
        hotdata = KBEngine.globalData.get('Base_HotfixList', None)
    elif component == 'cellapp':
        hotdata = KBEngine.globalData.get('Cell_HotfixList', None)
    elif component == 'common':
        hotdata = KBEngine.globalData.get('Common_HotfixList', None)
    return hotdata

def setHotfixList(component, val):
    '''
    component : baseapp
                cellapp
                common
    '''
    if component == 'baseapp':
        KBEngine.globalData['Base_HotfixList'] = val
    elif component == 'cellapp':
        KBEngine.globalData['Cell_HotfixList'] = val
    elif component == 'common':
        KBEngine.globalData['Common_HotfixList'] = val        

class Hotfix:
    def __init__(self):
        #KBEDebug.ERROR_MSG("Hotfix.__init__")
        #KBEDebug.ERROR_MSG("Hotfix.__init__ %s" % (self.__class__.mro()))

        self.var = 0
        self.selfClass = sys.modules[self.__module__]
        self.parentClass = {}

        bEntity = False
        for c in self.__class__.mro():
            if c.__name__ == 'Entity':
                bEntity = True
            if c.__name__ in _skip_class or c.__name__ == self.__class__.__name__:
                continue
            self.parentClass[c.__module__] = { 'var' : 0, 'module' : sys.modules[c.__module__] }

        if bEntity == True:
            self. tid = self.addTimer(1, 1, TUArg_Hotfix)

        #KBEDebug.ERROR_MSG("Hotfix.__init__.hotlist %s" % (self.parentClass))

    def Hotfix_Update(self):
        self.__hot_common()
        
        hdataList = getHotfixList()
        if hdataList is None:
            return

        bNeedHot = False

        for k, v in self.parentClass.items():
            hdata = hdataList.get(k, None)
            if hdata is not None and hdata['var'] > v['var']:
                if hdata['local_import'] == False:
                    try:
                        v['module'] = importlib.reload(v['module'])
                        hdata['local_import'] = True
                        v['var'] = hdata['var']
                        bNeedHot = True
                    except ImportError as e:
                        KBEDebug.ERROR_MSG("%s Hotfix.update parentClass ImportError:%s" % (self.__module__, e))
                        continue
                else:
                    v['var'] = hdata['var']
                    bNeedHot = True

        # do something 可以优化 只 reload 一次
        if bNeedHot == True:
            self.selfClass = importlib.reload(self.selfClass)

        hdata = hdataList.get(self.__module__, None)
        if hdata is not None and hdata['var'] > self.var:
            if hdata['local_import'] == False:
                try:
                    self.selfClass = importlib.reload(self.selfClass)
                    hdata['local_import'] = True
                    self.var = hdata['var']
                    bNeedHot = True
                except ImportError as e:
                    KBEDebug.ERROR_MSG("%s Hotfix.update selfClass ImportError:%s" % (self.__module__, e))
            else:
               self.var = hdata['var']
               bNeedHot = True

        if bNeedHot:                
            self.__hot()

    def __hot(self):
        for name, obj in inspect.getmembers(self.selfClass):
            if inspect.isclass(obj) and name == self.__class__.__name__:
                self.__class__ = obj
                KBEDebug.INFO_MSG("%s hotfix done" % (self.__module__))
                break

    def __hot_common(self):
        '''
        Hot 公用类的文件
        '''
        hdataList = getHotfixList('common')
        if hdataList is None:
            return

        for filename, hdata in hdataList.items():
            if hdata['local_import'] == True:
                continue
            hdata['local_import'] = True
            mod = sys.modules.get(filename, None)
            if mod is not None:
                sys.modules[filename] = importlib.reload(mod)
            KBEDebug.INFO_MSG("%s hotfix done" % (filename))