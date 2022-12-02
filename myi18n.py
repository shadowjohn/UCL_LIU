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
        "正常出字模式":"Normal Mode",
        "BIG5模式":"BIG5 Mode",
        "複製貼上模式":"Copy/Paste Mode",
        "1.關於肥米輸入法":"1. About UCLLIU Input Method",
        "2.切換至「遊戲模式」":"2. Switch to \"Game Mode\"",
        "2.切換至「正常模式」":"2. Switch to \"Normal Mode\"",        
        "3.選擇出字模式":"3. Sendkeys Mode",
        "【●】短版模式":"[o] UI/UX Short",
        "【　】短版模式":"[ ] UI/UX Short",
        "【,,,+】畫面加大":"[,,,+] UI/UX Increase",
        "【,,,-】畫面縮小":"[,,,-] UI/UX Minify",
        "英數時透明度":"En Mode Transparency",
        "肥模式透明度":"UCL Mode Transparency",
        "4.畫面調整":"4. UI Adjustment",
        "5.【●】使用 CTRL+SPACE 切換輸入法":"5. [o] Switch Input Method By CTRL+SPACE",
        "5.【　】使用 CTRL+SPACE 切換輸入法":"5. [ ] Switch Input Method By CTRL+SPACE",
        "6.【✔】顯示短根":"6. [o] Diplay [SP] Shortest Character",
        "6.【　】顯示短根":"6. [ ] Diplay [SP] Shortest Character",
        "】":"]",
        "【":"[",
        "●":"✔",
        "　":" ",
        "7.打字音":"7. Typing sound",
        "肥米輸入法：":"UCLLIU Input Method: ",
        "8.【●】啟動預設為「肥」模式":"8.[o] Boot default to \"UCL\" mode",
        "8.【　】啟動預設為「肥」模式":"8.[ ] Boot default to \"UCL\" mode",
        "9. 離開(Quit)":"9. Quit"        
    }