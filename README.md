# 这是一个 [KBEngine](#https://github.com/kbengine/kbengine) 脚本热更新方案

完全足够用到官方热更方案出来，相信我你根本用不上 def 和 协议 的热更新。

只要进程 `baseapp、cellapp` 上有活跃`Entity` 时才进行热更。

热更时自动处理继承关系，只需要依据继承关系调用。

新创建实体也会自动热更到最新版本。

## 使用方法
1. 改写所有 `from xxx import xxx` 方式 为 `import`
```python
from xxx import xxx
# 改为
import xxx
```
2. 创建加载 `Hotfix_Ent` 实体

3. 需要热更的类或实体继承 `Hotfix.Hotfix` 并增加 `onTimer` 回调。 公用类型的类不需要回调，只需要继承 `Hotfix.Hotfix`。
```python
import Hotfix
class YouEntity(KBEngine.Entity, Hotfix.Hotfix):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		Hotfix.Hotfix.__init__(self)

	def onTimer(self, id, userArg):
		if userArg == GDefine.TUArg_Hotfix:
            self.Hotfix_Update()
```

4. 使用 `Hotfix_Ent` 实体调用热更
```python
'''
def B_Hotfix_Hotfile(componentType, hotFilenameList)
	componentType:  1 = baseapp
					2 = cellapp
					3 = common
'''

hot = KBEngine.globalData['Hotfix_Ent']
hot.B_Hotfix_Hotfile(1, ['Account', 'parent.C1'])  # 更新 BaseApp Account.py、parent.C1.py 文件
hot.B_Hotfix_Hotfile(1, ['parent.C1'])             # 更新 BaseApp parent.C1.py 文件
hot.B_Hotfix_Hotfile(2, ['Account'])               # 更新 CellApp Account.py 文件
hot.B_Hotfix_Hotfile(3, ['CustomClass'])           # 更新 BaseApp与CellApp 的 CustomClass.py 文件
```
