# -*- coding: utf-8 -*-
import SendKeys
import php
import sys
import SendKeysCtypes
my = php.kit()
reload(sys)

#sys.setdefaultencoding("windows-1252")
sys.setdefaultencoding("CP950")
#SendKeys.playkeys([{"vk":5,"arg":True}],pause=0);

SendKeysCtypes.SendKeys("·F".decode("BIG5"),0);