# -*- coding: utf-8 -*-
###########################################
#  Auther:FeatherMountain(https://3wa.tw) #
#  Version: 0.1_Custom                    #
#  Date: 2022-12-02                       #
#  License: MIT                           #
###########################################
# # how to :
# import myi18n
# i18n = myi18n.kit()
# i18n.auto(str) 
# 自動判斷 = locale.getpreferredencoding()
# 如果不是 cp950，切換成英文版
import locale
class kit:           
    LOCALE_ENCODING = ''
    def __init__(self):
        self.LOCALE_ENCODING = locale.getpreferredencoding() 
        #print "myi18n __init__"
        #print self.LOCALE_ENCODING # 這裡正常是 cp950
        pass
    def auto(self,s):
        if self.LOCALE_ENCODING == "cp950":
            return s
        if self.data.has_key(s):
            return self.data[s]
        else:
            return s
    data = {
        "打字音啟動":"Enable Typing Sound",
        "】":"]",
        "【":"[",
        "●":"o",
        "　":" ",
        "7.打字音":"7. Typing sound",
        "肥米輸入法：":"UCLLIU Input Method: ",
        "8.【●】啟動預設為「肥」模式":"8.[o] Boot default to \"UCL\" mode",
        "8.【　】啟動預設為「肥」模式":"8.[ ] Boot default to \"UCL\" mode",
        "9. 離開(Quit)":"9. Quit"        
    }