# UCL_LIU
利用python+pyhook開發的仿嘸蝦米，肥米輸入法<br>
<br>
<center>
  <img src="http://3wa.tw/uploads/upload/ucl_0.png">
</center>
<center>
<div class="video3wa_class" style="text-align:center;min-width:1px;margin-left:auto;margin-right:auto;">
<script language="javascript" src="http://3wa.tw/inc/javascript/jquery/mediaelement/build/mediaelement-and-player.min.js"></script>
<link rel="stylesheet" href="http://3wa.tw/inc/javascript/jquery/mediaelement/build/mediaelementplayer.min.css"/>
<center>
<source type="video/webm" src="http://3wa.tw/video/users/shadow/20170616_130016.webm" />
<!-- MP4 source must come first for iOS -->
<source type="video/mp4" src="http://3wa.tw/video/users/shadow/20170616_130016.mp4" />
</video>
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
Compiler：<br>
　　pip install pyinstaller<br>
    參考 build.bat 製作單一 exe 方法<br>
<br>  
ToDo：<br>
<ul>
  <li>1、(嚴重)「送出字元」的方法，試了很多send key一直無法解決 send unicode的問題，暫時使用「剪貼簿」的Ctrl+V來實作貼上文字的功能</li>
  <li>2、「英文全形」輸入時，有些組合鍵如 Alt+tab還尚未決定</li>
  <li>(Done)<s>3、py2exe包成一支exe</s>改用pyinstaller代替</li>
  <li>4、尚有些按鍵會讓「英/肥」切來切去，暫未處理</li>
  <li>(Done)<s>5、離開程式的按鈕</s></li>
  <li>6、支援Linux、Mac的研究(下一次吃飽閒閒再說)</li>
</ul>
