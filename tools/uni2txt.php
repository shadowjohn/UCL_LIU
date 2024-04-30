<?php
//Author: FeatherMountain (https://3wa.tw)
ini_set("memory_limit",-1);

$filename = $argv[1] ?? 'liu-uni.tab';
$file_content = file_get_contents($filename);
$bytes = array_values(unpack('C*', $file_content)); // 將文件內容轉換為字節的數組

$i1 = getint16(0);
$words = getint16(4);
$i2 = $i1 + getint16(2); // or + ($words*2+7)/8
$i3 = $i2 + getint16(6); // or + ($words*1+7)/8
$i4 = $i3 + getint16(6); // or + ($words*1+7)/8

$rootkey = mb_str_split(" abcdefghijklmnopqrstuvwxyz,.'[]");

$step=0;
for ($i = 0; $i < 1024; $i++) {
  $key[0] = $rootkey[floor($i/32)];
  $key[1] = $rootkey[$i%32];
  if ($key[0] == ' ') continue;

  for ($ci = getint16($i*2); $ci < getint16($i*2+2); $ci++) {
    $bit24 = getbits($i4, 24, $ci);
    $hi = getbits($i1, 2, $ci);
    $lo = $bit24 & 0x3fff;

    $key[2] = $rootkey[$bit24>>19];
	$key[3] = $rootkey[$bit24>>14 & 0x1f];
    $flag_unknown = getbits($i2, 1, $ci);
    $flag_sp = getbits($i3, 1, $ci);
	//$key = str_replace(" ","",$key);
	//if(strlen($key)>4) continue;	
	$key = trim($key[0].$key[1].$key[2].$key[3]);
    echo "[{$key}]" . "\t" . utf8_chr($hi<<14 | $lo) . ($flag_sp ? '' : '') . ($flag_unknown ? '' : '') . "\n";
	$step++;
	//if($step>=10) break;
  }
  //if($step>=10) break;
}

function getint16($addr) {
  global $bytes;
  return $bytes[$addr] | $bytes[$addr+1]<<8;
}

function getbits($start, $nbit, $i) {
  global $bytes;
  if ($nbit==1 || $nbit==2 || $nbit==4) {
    $byte = $bytes[floor($start+$i*$nbit /8)];
    $ovalue = $byte>>(8-$nbit - $i*$nbit %8);
    return $ovalue & ((1<<$nbit)-1);
  } elseif ($nbit>0 && $nbit%8==0) {
    $nbyte = $nbit / 8;
    $value = 0;
    $a = $start + $i * $nbyte;
    while ($nbyte--) {
      $value = $value<<8 | $bytes[$a++];
    }
    return $value;
  } else {
    die();
  }
}

function utf8_chr($ord) {
  return mb_convert_encoding('&#' . intval($ord) . ';', 'UTF-8', 'HTML-ENTITIES');
}