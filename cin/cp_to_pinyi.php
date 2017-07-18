<?php
  //此程式是可以把cnsphonetic2017-02.cin轉成肥米輸入法同音字需要的pinyi.txt
  //判斷字串是否為utf8
  function  is_utf8($str)  {
    $i=0;
    $len  =  strlen($str);

    for($i=0;$i<$len;$i++)  {
        $sbit  =  ord(substr($str,$i,1));
        if($sbit  <  128)  {
            //本字節為英文字符，不與理會
        }elseif($sbit  >  191  &&  $sbit  <  224)  {
            //第一字節為落於192~223的utf8的中文字(表示該中文為由2個字節所組成utf8中文字)，找下一個中文字
            $i++;
            return 0;
        }elseif($sbit  >  223  &&  $sbit  <  240)  {
            //第一字節為落於223~239的utf8的中文字(表示該中文為由3個字節所組成的utf8中文字)，找下一個中文字
            $i+=2;        
        }elseif($sbit  >  239  &&  $sbit  <  248)  {
            //第一字節為落於240~247的utf8的中文字(表示該中文為由4個字節所組成的utf8中文字)，找下一個中文字
            $i+=3;
            //return  0;
        }else{
            //第一字節為非的utf8的中文字
            return  0;
        }
    }
    //檢查完整個字串都沒問體，代表這個字串是utf8中文字
    return  1;
  }   
  $data = file_get_contents("phone.cin");
  $m = end(explode("%chardef  begin",$data));
  $m = current(explode("%chardef  end",$m));
  $m = trim($m);

  $m = explode("\n",$m);
  $OUTPUT=ARRAY();
  foreach($m as $v)
  {
    $v = trim($v);
    $v = str_replace("\t\t"," ",$v);
    $d = explode(" ",$v);
    if(!isset($OUTPUT[$d[0]]))
    {
      $OUTPUT[$d[0]]=ARRAY();
    }
    //if(is_utf8($d[1]))
    {      
      array_push($OUTPUT[$d[0]],$d[1]);   
    }
  } 
  $OUT = "";
  foreach($OUTPUT as $v)
  {
    $OUT.=implode(" ",$v);
    $OUT.="\n";
  }
  $OUT=trim($OUT);
  file_put_contents("pinyi.txt",$OUT);  