# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import Hotfix
import time


class Hotfix_Ent(KBEngine.Entity, Hotfix.Hotfix):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        Hotfix.Hotfix.__init__(self)

        KBEngine.globalData[self.__class__.__name__] = self
        
    def onTimer(self, id, userArg):
        """
        KBEngine method.
        使用addTimer后， 当时间到达则该接口被调用
        @param id		: addTimer 的返回值ID
        @param userArg	: addTimer 最后一个参数所给入的数据
        """
        if userArg == Hotfix.TUArg_Hotfix:
            self.Hotfix_Update()

    def B_Hotfix_Hotfile(self, componentType, hotFilenameList):
        '''热更新文件
            参数： 组件类型
                    1 = baseapp
                    2 = cellapp
                    3 = common
			参数： 要热更的文件列表

            Ps. 以下目录会自动映射成根目录
                server_common
                common
                base
                base\interfaces
                cell
                cell\interfaces
                data
            调用示例： 
                .B_Hotfix_Hotfile(1, ['Account'])               更新 BaseApp Account.py 文件
                .B_Hotfix_Hotfile(1, ['parent.C1'])             更新 BaseApp parent.C1.py 文件
                .B_Hotfix_Hotfile(2, ['Account'])               更新 CellApp Account.py 文件
                .B_Hotfix_Hotfile(3, ['CustomClass'])           更新 BaseApp与CellApp 的 CustomClass.py 文件
        '''
        component = None
        if componentType == 1:
            component = 'baseapp'
        elif componentType == 2:
            component = 'cellapp'
        elif componentType == 3:
            component = 'common'            
        else:
            KBEDebug.ERROR_MSG("Hotfix_Ent.B_Hotfix_Hotfile. component(%i) illegal" % (component))
            return

        nowtime = int(time.time())

        oldHData = Hotfix.getHotfixList(component)
        if oldHData is None:
            oldHData = {}

        for filename in hotFilenameList:
            classData = oldHData.get(filename, None)
            newClassData = None
            if classData is None:
                newClassData = {'var' : 1, 'local_import' : False, 'hotime' : nowtime}
            else:
                newClassData = {'var' : classData['var'] + 1, 'local_import' : False, 'hotime' : nowtime}
            oldHData[filename] = newClassData

        Hotfix.setHotfixList(component, oldHData)
        KBEDebug.ERROR_MSG("Hotfix_Ent.B_Hotfix_Hotfile. broadcast done")