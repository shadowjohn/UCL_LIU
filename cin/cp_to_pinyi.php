<?php
  //此程式是可以把phone.cin轉成肥米輸入法同音字需要的pinyi.txt
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
    array_push($OUTPUT[$d[0]],$d[1]);   
  } 
  $OUT = "";
  foreach($OUTPUT as $v)
  {
    $OUT.=implode(" ",$v);
    $OUT.="\n";
  }
  $OUT=trim($OUT);
  file_put_contents("pinyi.txt",$OUT);  
