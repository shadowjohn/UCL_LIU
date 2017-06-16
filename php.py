# -*- coding: utf-8 -*-
###########################################
#  Auther:FeatherMountain(http://3wa.tw)  #
#  Version: 1.3                           #
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
    def is_str(self,s):
        return isinstance(s, basestring)
    def array_push(self,arr,data):
        return arr.append(data);
    def pwd(self):
        import os;
        return os.getcwd();
    def deltree(self,path):
        import shutil
        shutil.rmtree(path);
    def math_round(self,data,step):
        import decimal
        a = decimal.Decimal(data);
        return round(a,step);
    def array_shuffle(self,arr):  
        import random
        random.shuffle(arr);    
    def is_win(self):
        import sys
        is_windows = hasattr(sys, 'getwindowsversion')
        return is_windows
    def allow_ajax(self):
        self.echo("Access-Control-Allow-Origin: *\n");
        self.echo("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept\n");   
    def server_name(self):
        import socket
        return socket.gethostname()
    def SP(self):        
        if self.is_win():
          return "\\"
        else:
          return "/"        
    def include(self,filename):
        print(self.file_get_contents(filename))
    def mkdir(self,dirname):
        # Create directory
        import os
        if self.is_dir(dirname)==False:
          os.mkdir(dirname)
    def time(self):
        # Return timestamp   
        import time 
        return int(time.time())
    def date(self,*args):
        # Argv(0) for output struct
        # Argv(1) for timestamp
        import datetime
        lens = len(args)        
        nowtime = datetime.datetime.now()
        if lens == 2:
            nowtime = datetime.datetime.fromtimestamp(int(args[1]))
        if lens == 0:
            return nowtime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            if args[0] == "Y-m-d H:i:s":
                return nowtime.strftime("%Y-%m-%d %H:%M:%S")
            elif args[0] == "Y-m-d":
                return nowtime.strftime("%Y-%m-%d")
            elif args[0] == "Y":
                return nowtime.strftime("%Y") 
            elif args[0] == "m":
                return nowtime.strftime("%m")       
            elif args[0] == "d":
                return nowtime.strftime("%d")
            elif args[0] == "H":
                return nowtime.strftime("%H") 
            elif args[0] == "i":
                return nowtime.strftime("%M") 
            elif args[0] == "s":
                return nowtime.strftime("%S")
            elif args[0] == "Y-m-d H:i":
                return nowtime.strftime("%Y-%m-%d %H:%M")
            elif args[0] == "Ymd":
                return nowtime.strftime("%Y%m%d")  
            elif args[0] == "Y/m/d H:i:s":
                return nowtime.strftime("%Y/%m/%d %H:%M:%S")
            elif args[0] == "Y/m/d":
                return nowtime.strftime("%Y/%m/%d")                                                                                                             
            else:
                return nowtime.strftime("%Y-%m-%d %H:%M:%S")  
    def count(self,arr):
        return len(arr)
    
    def strlen(self,x):
        return len(x)   
    def trim(self,input): 
        # Return trim data
        return str(input).strip();
    def ls2l(self,list_string):
        import ast
        return ast.literal_eval(list_string)         
    def str_replace(self,findwords,replace_words,data):
        # Data Replace
        return data.replace(findwords,replace_words)
    def copy(self,source_file,target_file):
        import shutil
        shutil.copy(source_file,target_file)
    def move(self,source_file,target_file):
        import shutil
        shutil.move(source_file,target_file)
    def copy_all(self,source_dir,target_dir):
        import shutil
        shutil.copytree(source_dir,target_dir)
    def utf8tobig5(self,data):
        return data.encode('big5');
    def touch(self,fname, times=None):
        import os        
        with open(fname, 'a'):
          os.utime(fname, times);
    def is_dir(self,pathname):
        import os
        return os.path.isdir(pathname)
    def is_file(self,filename):
        import os
        return os.path.isfile(filename)
    def rand(self,start_int,end_int):
        import random
        return random.randint(start_int,end_int)
    def unlink(self,filename):
        import os
        if self.is_file(filename)==True:
          os.remove(filename)
    def glob(self,pathdata):
        import glob
        return glob.glob(pathdata)
    def base64_encode(self,data):
        import base64
        return base64.encodestring(data)
    def base64_decode(self,data):
        import base64
        return base64.decodestring(data)    
    def file_get_contents(self,data_path):
        if self.strtolower(data_path).find("http:") != -1 or self.strtolower(data_path).find("ftp:") != -1:
            # From web
            if self.python_version()==2:
              import urllib2
              return urllib2.urlopen(data_path).read()
            else:
              import urllib.request
              return urllib.request.urlopen(data_path).read()
        else:
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
    def sleep(self,second):
        import time
        time.sleep(self,second)
    def usleep(self,micro_seconds):
        import time
        time.sleep(micro_seconds / 1000000.0)
    def strtotime(self,datedata):
        import time
        output = 0
        try:
          output = time.strptime(datedata, '%Y-%m-%d %H:%M:%S')
        except:
          output = time.strptime(datedata, '%Y-%m-%d')
        return int(time.mktime(output))
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
    def rmdir(self,dirpath):
        import os
        os.rmdir(dirpath)
    def print_r(self,*args):
        import print_r
        if len(args) == 1:
          print_r.print_r(args[0])
        elif len(args) == 2:
          return print_r.print_r(args[0],output = False)
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
    def xml_decode(self,data):
        import xmltodict
        return xmltodict.parse(data)
    def xml_encode(self,dict_data):
        import xmltodict
        return xmltodict.unparse(dict_data)
    def system(self, cmd):
        import os
        return os.popen(cmd).read()         
    def htmlspecialchars(self, data):
        import cgi
        return cgi.escape(data,True)
    def htmlspecialchars_decode(self,string):
        # For html spacialchars decode
        import re
        pattern = re.compile("&(\w+?);")
        return pattern.sub(self.htmlspecialchars_decode_func, string)    
    def in_array(self, needle,arr):
        return ( needle in arr )
    def file_get_contents_post(self, url , data = None , headers = None , referer = None):
        import requests
        
        _data = "";
        _user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)'
        _headers = { 
            'User-Agent' : _user_agent,
            'Content-type' : 'application/x-www-form-urlencoded' 
        }       
        requests.adapters.DEFAULT_RETRIES = 30
        
        if headers is not None:
          for k in headers:
            _headers[k]=headers[k];
        #print(_headers);        
        if data is None or str(data)=="":
          _data = requests.get(url,headers = _headers, stream=True)         
        else:
          _data = requests.post(url,data = data,headers = _headers, stream=True)
                
        return _data.raw.read()
    def file_get_contents_post_old(self, url , postdata):
        # postdata can only be json 
        import urllib
        import urllib2     
        # url
        # postdata = {}
        # postdata["mode"] = "add_edit"
        # postdata["domode"] = "add"
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)'      
        headers = { 
            'User-Agent' : user_agent,
            'Content-type' : 'application/x-www-form-urlencoded' 
        }      
        # postdata also support :
        #  values = 
        #  {
        #      'name' : 'WHY',    
        #      'location' : 'SDU',    
        #      'language' : 'Python' 
        #  } 
        #
        data = urllib.urlencode(postdata)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()      
        return the_page
    def pre_print_r(self, *argv):
        if len(argv) == 1:
            print("<pre>\n%s\n</pre>" % (self.print_r(argv[0],True)))
        else:
            return "<pre>\n%s\n</pre>" % (self.print_r(argv[0],True))
    def nl2br(self,data):
        return data.replace("\n","<br>")
    def getGET_POST(self, string_fields,method):
        import cgi           
        if self.form_status == False:
          self.form = cgi.FieldStorage();
          self.form_status = True                
        output = {}        
        for k in self.form.keys():
          variable = str(k)
          value = str(self.form.getvalue(variable))
          output[variable] = value
        return output
    def save_uploaded_file (self,form_file, upload_filename):
        #http://www.tutorialspoint.com/python/python_cgi_programming.htm
        import shutil        
        fileitem = form_file
        if not fileitem.file: return
        #outpath = os.path.join(upload_dir, fileitem.filename)
        dn = self.dirname(upload_filename)
        if self.is_dir(dn) == False:
          self.mkdir(dn)
        #self.copy(fileitem.filename,upload_filename)
        open(upload_filename, 'wb').write(fileitem.file.read())    
        #with open(outpath, 'wb') as fout:
        #    shutil.copyfileobj(fileitem.file, fout, 100000)  
#     def getGET_POST(self, string_fields,method):
#         # the data must trim , htmlspecialchars and addslashes        
#         method = self.strtoupper(method)
#         m = self.explode(',',string_fields)
#         output = {}
#         if method == "GET":
#             from django.http import HttpResponse                        
#             for i in request.GET.keys():
#                 if self.in_array(i,m):
#                     output[i] =  request.GET[i]
#             return output
#         elif method == "POST":
#             from django.http import HttpResponse                        
#             for i in request.POST.keys():
#                 if self.in_array(i,m):
#                     output[i] =  request.POST[i]
#             return output
    def url_get_kind(self,url):
        #http or ftp
        import urlparse
        return urlparse.urlsplit(url)[0]            
    def url_get_hostname(self,url):
        import urlparse
        return urlparse.urlsplit(url)[1]
    def url_get_path(self,url):
        import urlparse
        return urlparse.urlsplit(url)[2]
    def dirname(self,path):
        import os
        return os.path.dirname(path)
    def mainname(self,path):
        import os
        return os.path.splitext(path)[0]
    def basename(self,path):
        import os
        _output = "";
        if self.is_file(path):
          _output = os.path.basename(path)
        else:
          m = self.explode(self.SP(),path)
          _output = m[self.count(m)-1]
        return _output    
    def subname(self,path):
        import os
        return os.path.splitext(path)[-1].replace('.','') 
    def natcasesort(self,arr): 
        if isinstance(arr, list): 
          arr = sorted(arr, key=lambda x:str(x).lower()) 
        elif isinstance(arr, dict): 
          arr = sorted(arr.iteritems(), key=lambda x:str(x[0]).lower())
        return arr
    def sort(self,arr):
        return sorted(arr)
    def array_unique(self,arr):
        return list(set(array))
    def array_values(self,dictarr):
        return dictarr.values()
    def is_string_like(self,data,find_string):
        if data.find(find_string) == -1:
          return False
        else:
          return True
    def link_db(self,db_kind,host,user,passwd,db):
        import pdo
        _db_type = ""
        db_kind = self.strtoupper(db_kind)
        if db_kind == "MYSQL":
          db_type = "MySQLdb"
        _link_str = 'Module='+db_type+';Host='+host+';User='+user+';Passwd='+passwd+';DB='+db
        PDO = pdo.connect(_link_str)
        self.execSQL(PDO,"SET NAMES UTF8")           
        return PDO
    def execSQL(self,pdo,SQL): 
        pdo.simpleCMD(SQL);
    def selectSQL_SAFE(self,pdo,SQL,m):
        SQL = self.str_replace("?","%s",SQL)    
        Results = pdo.open(SQL,m)
        output = []
        keys = Results.keys()
        #print(keys)
        while Results.next():
          d = {}
          for k in keys:
            d[k] = str(Results[k].value)                        
          output.append(d)
        return output
        #while Results.next():
        #    print("Name: " + Results['Name'].value)
    def insertSQL(self,pdo,table,keyvalue):
        F = []
        V = []
        Q = []        
        for k in keyvalue:          
          F.append(k)
          V.append(keyvalue[k])
          Q.append("?")                
        FIELDS = self.implode('`,`',F)                
        Q_FIELDS = self.implode(',',Q)        
        
        SQL = "INSERT INTO `"+table+"`(`"+FIELDS+"`)VALUES("+Q_FIELDS+")"
        SQL = self.str_replace("?","%s",SQL)  
        LAST_ID = pdo.execute(SQL,V)
        return LAST_ID.insertid
    def error_report_on(self):
        import cgitb 
        cgitb.enable()
    def strip_tags(self,html_data):
        from bs4 import BeautifulSoup
        bs_html = BeautifulSoup(html_data,'html.parser');
        return bs_html.text
    def myprint(self,data):
        import pprint
        pprint.pprint(data);      
    def header(self,headers = None, memory = False):
        _output = "";
        if headers is None:
          _output+="Content-Type: text/html\n";
        else:
          # Content-Type: application/octet-stream\n
          _output+=str(headers);
        if memory == True:
          None
        else:
          print(_output);
        return _output;
    def filesize(self,filename):
        import os
        return os.path.getsize(filename)
    def download_Header(self,display_filename,filesize=None):                
        _output_filename = self.basename(display_filename);
        _H = "";
        #_H+="Content-Type: text/html\n";
        _H+="Content-Type: application/octet-stream\n";         
        _H+=("Content-Disposition: attachment; filename=\"%s\";\n" % (_output_filename));
        _H+="Content-Transfer-Encoding: binary;\n";
        _H+="Expires: 0;\n";
        _H+="Cache-Control: must-revalidate;\n";
        _H+="Pragma: public;\n";
        if filesize is not None:
          _H+=("Content-Length: %ld;\n" % filesize);        
        self.header(_H);
    def get_between(self,data,start,end):
        result = data[data.find(start)+len(start):data.rfind(end)]
        if data[:-1] == result:
          return "";
        return result
    def get_between_multi(self,data,start,end):
        #prevent search multiple data        
        source=data;
        start_sep=start;
        end_sep=end;
        result=[]
        tmp=source.split(start_sep)
        for par in tmp:
          if end_sep in par:
            result.append(par.split(end_sep)[0])        
        return result 
    def s2b(self,my_str):
        bytes = str.encode(my_str)
        return bytes 
    def convert(self,s):
        try:
            return s.encode('latin1').decode('utf8')
        except:
            return s        
    def ceil(self,data):
        import math
        return math.ceil(data);
    def is_numeric(self,data):
        return data.isnumeric();
    def python_version(self):
        import sys
        if sys.version_info[0] > 2:
          return 3;
        else:
          return 2;        
    def urlencode(self,data):
        if self.python_version() == 3:
          import urllib.parse
          return urllib.parse.quote(data);
        else:
          import urllib
          return urllib.quote(data);