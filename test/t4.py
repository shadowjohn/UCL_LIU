# -*- coding: utf-8 -*-
#import SendKeys
import php
import sys
#import SendKeysCtypes
my = php.kit()
reload(sys)

a = "a,b,c,dea,a, ,, , ,, ,asdf, a kasdf ak  ksdk , , ,d , ,"
b = my.explode(",",a);
print b

b = [x.strip(' ') for x in b]
b = filter(str.strip, b)
print b
#b = ' '.join(b).split()
#print b
