<?php
  //此程式是可以把phone.cin轉成肥米輸入法同音字需要的pinyi.txt
  function get_between_new($source, $s, $e) {
    /*
      $beginning_pos = strpos($source, $beginning, $init_pos);
      $middle_pos = $beginning_pos + strlen($beginning);
      $ending_pos = strpos($source, $ending, $beginning_pos + 1);
      $middle = substr($source, $middle_pos, $ending_pos - $middle_pos);
      return $middle;
    */
    if(strpos($source, $s) === FALSE) return FALSE;
    if(strpos($source, $e) === FALSE) return FALSE;
    $start = strpos($source, $s) + strlen($s);
    $end = strpos($source, $e, $start);
    $return = substr($source, $start, $end - $start);
    return $return;    
  }
  
  $OUT = ARRAY(); //輸出
  
  $data = file_get_contents("phone.cin");
  $data = trim(str_replace("\r","",$data));
  
  $keyname = trim(get_between_new($data,"%keyname  begin","%keyname  end"));
  $m = explode("\n", $keyname);
  array_push($OUT,"VERSION_0.01");
  $_key = ARRAY();
  $_value = ARRAY();
  foreach($m as $v)
  {
    $d = explode("  ",$v);
    array_push($_key,$d[0]);
    array_push($_value,$d[1]);
  }
  array_push($OUT,implode(" ",$_key));
  array_push($OUT,implode(" ",$_value));
  
  
  $chardef = trim(get_between_new($data,"%chardef  begin","%chardef  end"));
  $m = explode("\n",$chardef);
  $OUTPUT=ARRAY();
  foreach($m as $v)
  {
    $v = trim($v);
    $v = str_replace("\t\t"," ",$v);
    $d = explode(" ",$v);
    if(!isset($OUTPUT[$d[0]]))
    {
      $OUTPUT[$d[0]]=ARRAY();
      array_push($OUTPUT[$d[0]],$d[0]); //First blood
    }
    array_push($OUTPUT[$d[0]],$d[1]);   
  } 
  
  foreach($OUTPUT as $v)
  {
    array_push($OUT,implode(" ",$v));    
  }  
  file_put_contents("pinyi.txt",implode("\n",$OUT));  
