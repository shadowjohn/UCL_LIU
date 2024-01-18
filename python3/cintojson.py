# -*- coding: utf-8 -*-
#import sys
import json        
class CinToJson(object):
  def __init__(self):
    pass
  def CinToJson(self):
    return self
  #def _file_get_contents(self,filename):
  #  return open(filename).read()
  def _find_between(self, s, first, last ):
    start = s.index( first ) + len( first )
    end = s.index( last, start )
    return s[start:end]
  def run(self,outputfile_mainname,source_file,donothing):
    output = {}
    output["chardefs"] = {}
    data = open(source_file).read()
    char_default_data = self._find_between(data,"%chardef begin","%chardef end")
    char_default_data = str(char_default_data).strip()
    m = char_default_data.split("\n")
    for k in m:
      value = str(k).strip()
      if value =="":
        continue
      d = value.split(" ")
      # 2019-04-13 �Y�� cin �̬O�Ĥ@�Ӧr�O����A���s��2�B3�B4�B5�r�@�_�A�ҥH�o�����w���O������2�N���L
      if len(d) < 2:
        continue
      d[0] = d[0].strip()
      for kk in range(1,len(d)):            
        #print(d)      
        #print(d[0])        
        d[1] = d[kk].strip()             
        if output["chardefs"].has_key(d[0])==False:      
          output["chardefs"][d[0]] = []
        output["chardefs"][d[0]].append(d[1])
      #sys.exit()
    data = json.dumps(output,indent=4, sort_keys=True, ensure_ascii=False)
    #print(data)
    #sys.exit()
    #write file       
    f = open(outputfile_mainname+".json", 'wb')
    f.write(data)