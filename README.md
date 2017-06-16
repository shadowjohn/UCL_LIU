# UCL_LIU
利用python+pyhook開發的仿嘸蝦米，肥米輸入法<br>
<br>
<center>
  <img src="http://3wa.tw/uploads/upload/ucl_0.png">
</center>
<br>
版本： V0.1<br>
<br>
開發動機：<br>
　　吃飽閒閒覺得人生就是該自己寫一套輸入法，然後就開始寫了。<br>
<br>
開發工具：<br>
  <ul>
  <li>Python 27 (32BIT)</li>
  <li>pyhook</li>
  <li>pygtk</li>
  <li>pywin32</li>
  <li>字碼表參考PIME裡的liu.json</li>
</ul>
<br>  
ToDo：<br>
<ul>
  <li>１、(嚴重)「送出字元」的方法，試了很多send key一直無法解決 send unicode的問題，暫時使用「剪貼簿」的Ctrl+V來實作貼上文字的功能</li>
  <li>2、「英文全形」輸入時，有些組合鍵如 Alt+tab還尚未決定</li>
  <li>3、py2exe包成一支exe</li>
  <li>4、尚有些按鍵會讓「英/肥」切來切去，暫未處理</li>
  <li>5、支援Linux、Mac的研究(下一次吃飽閒閒再說)</li>
</ul>
