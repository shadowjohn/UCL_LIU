# -*- coding: utf-8 -*-
###########################################
#  Auther:FeatherMountain(http://3wa.tw)  #
#  Version: 1.3_Custom                    #
#  Date: 2016-09-21                       #
#  License: LGPLv3                        #
###########################################
# # how to :
# import include
# my = include.kit()
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
# import htmlentitydefs
class kit:           
    def __init__(self):
        self.form_status = False;    
    def pwd(self):
        import os;
        return os.getcwd();            
    def is_win(self):
        import sys
        is_windows = hasattr(sys, 'getwindowsversion')
        return is_windows           
    def SP(self):        
        if self.is_win():
          return "\\"
        else:
          return "/"    
    def strlen(self,x):
        return len(x)   
    def trim(self,input): 
        # Return trim data
        return str(input).strip();    
    def str_replace(self,findwords,replace_words,data):
        # Data Replace
        return data.replace(findwords,replace_words)
    def copy(self,source_file,target_file):
        import shutil
        shutil.copy(source_file,target_file) 
    def utf8tobig5(self,data):
        return data.encode('big5');
    def is_dir(self,pathname):
        import os
        return os.path.isdir(pathname)
    def is_file(self,filename):
        import os
        return os.path.isfile(filename)    
    def unlink(self,filename):
        import os
        if self.is_file(filename)==True:
          os.remove(filename)    
    def file_get_contents(self,data_path):        
        try:
          return open(data_path,encoding = 'utf8').read()
        except:
          return open(data_path).read()
    def file_put_contents(self,filename,data,IS_APPEND=False):
        f = "";
        if IS_APPEND==True:
          f = open(filename, 'a');
        else:
          f = open(filename, 'wb');
        f.write(data)
        f.close()
    def exit(self):
        import sys
        sys.exit(0)
    def echo(self,data):
        import sys
        sys.stdout.write( ("%s" % data) ); 
    def strtoupper(self,data):
        return data.upper();
    def strtolower(self,data):
        return data.lower() 
    def explode(self,sep,data):
        return data.split(sep)
    def implode(self,sep,arr):
        return sep.join(arr)
    def json_decode(self,data):
        import json
        return json.loads(data)
    def json_encode(self,dict_data):
        import json
        return json.dumps(dict_data); #, ensure_ascii=False);
    def json_encode_utf8(self,dict_data):
        import json
        return json.dumps(dict_data, ensure_ascii=False)
    def json_format(self,json_data):
        import json
        return json.dumps(self.json_decode(json_data),indent=4, sort_keys=True)
    def json_format_utf8(self,json_data):
        import json
        return json.dumps(self.json_decode(json_data),indent=4, sort_keys=True, ensure_ascii=False)                                      
    def array_unique(self,arr):
        #return list(set(arr))
        out_list = []
        for val in arr:
          if not val in out_list:
            out_list.append(val)
        return out_list
    def is_string_like(self,data,find_string):
        if data.find(find_string) == -1:
          return False
        else:
          return True    
    def python_version(self):
        import sys
        if sys.version_info[0] > 2:
          return 3;
        else:
          return 2;
    def base64_decode(self,data):
        import base64
        return base64.decodestring(data)
    def glob(self,pathdata):
        import glob
        return glob.glob(pathdata)