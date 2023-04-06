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
    def microtime(self):
        import time
        return round(time.time() * 1000)   
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
        if type(find_string) == list:          
          for i in range(0,len(find_string)-1):
            if data.find(find_string[i]) != -1:
              return True
          return False
        else:
          # 原來的 string
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
    def array_remove_empty_and_trim(self,arr):
        arr = [x.strip(' ') for x in arr];
        o = [];
        for i in range(0,len(arr)):
            if arr[i].strip()!='':
                o.append(arr[i]); 
        return o;
    def basename(self,path):
        import os
        _output = "";
        if self.is_file(path):
          _output = os.path.basename(path)
        else:
          m = self.explode(self.SP(),path)
          _output = m[len(m)-1]
        return _output            
    def mainname(self,path):
        import os
        return os.path.splitext(self.basename(path))[0]    
    def in_array(self, needle,arr):
        return ( needle in arr )
    def rand(self,start_int,end_int):
        import random
        return random.randint(start_int,end_int)
    def system(self,cmd):
        #From : https://stackoverflow.com/questions/43593348/winerror-6-the-handle-is-invalid-from-python-check-output-spawn-in-electron-app/43606682#43606682
        import os
        try:
            from subprocess import DEVNULL
        except ImportError:
            DEVNULL = os.open(os.devnull, os.O_RDWR)
        import subprocess
        #openai 教的，這招可以隱藏視窗
        #Issue 178、隱藏查找 windows 版本時，外部指令顯示視窗問題
        startupinfo = subprocess.STARTUPINFO() 
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        returned_output = subprocess.check_output(cmd, stdin=DEVNULL, stderr=DEVNULL, startupinfo=startupinfo)
        return returned_output        
    def getFileProperties(self,fname):
        import win32api
        """
        From : https://stackoverflow.com/questions/580924/how-to-access-a-files-properties-on-windows
        Read all properties of the given file return them as a dictionary.
        """
        propNames = ('Comments', 'InternalName', 'ProductName',
            'CompanyName', 'LegalCopyright', 'ProductVersion',
            'FileDescription', 'LegalTrademarks', 'PrivateBuild',
            'FileVersion', 'OriginalFilename', 'SpecialBuild')

        props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

        try:
            # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
            fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
            props['FixedFileInfo'] = fixedInfo
            props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                    fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                    fixedInfo['FileVersionLS'] % 65536)

            # \VarFileInfo\Translation returns list of available (language, codepage)
            # pairs that can be used to retreive string info. We are using only the first pair.
            lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

            # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
            # two are language/codepage pair returned from above

            strInfo = {}
            for propName in propNames:
                strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
                ## print str_info
                strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

            props['StringFileInfo'] = strInfo
        except:
            pass

        return props