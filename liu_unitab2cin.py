# -*- coding: utf-8 -*-
# Copyright (C) 2017 Hong Jen Yee (PCMan) <pcman.tw@gmail.com>
# Copyright (C) 2017 Ho Chung Han (3WA羽山) <linainverseshadow@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import sys
import struct
import math
import codecs
#from builtins import chr
# reference: https://www.ptt.cc/bbs/Liu/M.1164374563.A.41C.html
# ftp://mail.im.tku.edu.tw/%A7U%B1%D0/bearhero/prog/%A8%E4%A5%A6/JavaWorld/%E5F%BD%BC%A6%CC5.6/SUPPORT/README.TXT
reload(sys)
sys.setdefaultencoding('UTF-8')

cin_head = '''%gen_inp 
%ename liu
%cname 嘸蝦米
%encoding UTF-8 
%selkey 0123456789 
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
'''

cin_tail = "%chardef end"

# Add By 3WA FeatherMountain
def bits(st):    
    b=''.join(format(ord(i),'b').zfill(8) for i in st)
    return b
def fun(i):
    return ('{0:>8s}'.format(i))
            
def convert_liu_unitab(tab_filename, out_filename):
    idx_to_key = " abcdefghijklmnopqrstuvwxyz,.'[]"
    with codecs.open(tab_filename, "rb") as f:
        # read 32x32 uint16 2-d array index table
        key_table = struct.unpack("1024H", f.read(1024 * 2))
        n_words = key_table[-1]  # read uint16 word_count
        
        # read 2 x word_count bits
        # Fix By FeatherMountain 2017/07/06
        #f.read(8)
        
        #high_bits = f.read(int(math.ceil((n_words * 2+8  )/8)))
        high_bits = f.read(int(math.ceil((n_words * 2+7  )/8))+8)
        
        #high_bits = f.read()
        #print
        #print(bits(high_bits));
        #print("\n")
        # read word_count bits
        # Fix By FeatherMountain 2017/07/06
        unknown_bits = f.read(int(math.ceil((n_words   ) / 8)))
                                                     
        # read word_count bits
        # Fix By FeatherMountain 2017/07/06
        is_simple_bits = f.read(int(math.ceil((n_words ) / 8)))
        hb = bits(high_bits);
        # read words
        words = []
        #print(n_words)  
        start_bit=0      
        for i in range(n_words):
            

            # convert bytes to binary strings for ease of handling
            # Fix By FeatherMountain 2017/07/06
            # https://stackoverflow.com/questions/33080011/convert-8-bits-to-byte-array-in-python-2-7
            #word_data = f.read(3)        
            #bin_word = "".join(["{:08b}".format(w) for w in word_data])
                        
            #bin_word=""
            #[]
            #for k in range(0,3):            
            #  word_data = f.read(1)              
              #bin_word.append( bits(word_data)[::-1] )
            #  bin_word = "%s%s" % (bits(word_data),bin_word)
              #print(bin_word)
            #tmp=bin_word[2]
            #bin_word[2]=bin_word[0]
            #bin_word[0]=tmp
            #bin_word="".join(bin_word)
            #bin_word=bin_word[::-1]            
            
            word_data = f.read(3)
            #print("3:%s" % (word_data))        
            #bin_word = "".join(["{:>8s}".format(bits(w)) for w in word_data])
            bin_word = "%s" % (bits(word_data))
            
            #bin_word = bin_word
            #print(bin_word)
            #continue;
            #bin_word = "".join( [fun(bits(w)) for w in word_data])
            
            
            key3 = int(bin_word[0:5], 2) # 0 5
            
            key4 = int(bin_word[5:10], 2) # 5: 10

            # get low bits                                         #10:24
            bin_low_word = bin_word[10:24]

            # get high bits
            #i_byte, start_bit = divmod(i * 2, 8)  # 2 bits per word
            #print("i:%s" % i)
            #print("i_byte:%s" % i_byte)
            #print("start_bit:%s" % start_bit)
            #bin_high_word = "{:08b}".format(high_bits[i_byte])[start_bit: start_bit + 2]
            #print("%d",i_byte);
            
            #bin_high_word = bits(high_bits[i_byte])[start_bit: start_bit + 2 ]
            
            bin_high_word = "%s%s" % (hb[i*2+16],hb[i*2+1+16])
            #start_bit=start_bit + 2 
            
            
            #bin_high_word = bits(high_bits[i])[0:2]
            #bin_high_word = bits(high_bits[i_byte])[0:2]
            #[start_bit:start_bit + 2])
            #print(bin_high_word)
            
            #sys.exit()
            #start_bit = start_bit + 2
            # concate the high and low bits and generate the unicode value
            #bin_word = "00%s" % (bin_low_word)
            #bin_real = "%s%s" % (bin_high_word , bin_low_word)
            #bin_word1 = "01%s" % (bin_low_word)
            #bin_word2 = "10%s" % (bin_low_word)
            #bin_word3 = "11%s" % (bin_low_word)
            #bin_word4 = "%s00" % (bin_low_word)
            #bin_word5 = "%s01" % (bin_low_word)
            #bin_word6 = "%s10" % (bin_low_word)
            #bin_word7 = "%s11" % (bin_low_word)
            bin_real = ""
            '''
            try:              
              print("bin_word1 {}\n".format(chr(int(bin_word1,2))))
              print("bin_word2 {}\n".format(chr(int(bin_word2,2))))
              print("bin_word3 {}\n".format(chr(int(bin_word3,2))))
              print("bin_word4 {}\n".format(chr(int(bin_word4,2))))
              print("bin_word5 {}\n".format(chr(int(bin_word5,2))))
              print("bin_word6 {}\n".format(chr(int(bin_word6,2))))
              print("bin_word7 {}\n".format(chr(int(bin_word7,2))))
              
            except Exception as e:
              pass
            '''
            #word_val = int(bin_word, 2)           
            #word=""
            word = ""
            try:                
                #word = unichr(word_val)
                bin_real = "%s%s" % (bin_high_word , bin_low_word)
                word = unichr(int(bin_real,2))
            except Exception as e:
                print(e)
            #words.append((key3, key4, word, unichr(int(bin_real,2)), unichr(int(bin_word1,2)),unichr(int(bin_word2,2)),unichr(int(bin_word3,2)),unichr(int(bin_word4,2)),unichr(int(bin_word5,2)),unichr(int(bin_word6,2)),unichr(int(bin_word7,2))    ))
            words.append((key3, key4, word))
                    
        words.append((0, 0, None))  # add a mark for end of list

    # According to some users, there might be some variations in the format of liu tabs among versions.
	# We do some simple checks to ensure that we correctly read from the head of the table
    n_skip=0
    #for n_skip in range(0, 32):
    #    word = words[n_skip][2]
    #    if word in ["對","夺","对","対"]: # the first word in liu should be one of these four characters
    #        break
    if n_skip:
        words = words[n_skip:]

    # generate output
    with codecs.open(out_filename, "w", encoding="utf-8") as out:
        out.write(cin_head)
        # entries 0 - 31 of key table are useless, skip them
        for i_key in range(32, len(key_table) - 1):
            key1, key2 = divmod(i_key, 32)
            # enumerate words starts with (key1, key2)
            i_start_word = key_table[i_key]
            i_next_word = key_table[i_key + 1]
            #print("GG",i_start_word, i_next_word)
            for i in range(i_start_word, i_next_word):
                #(key3, key4, word,real,w1,w2,w3,w4,w5,w6,w7) = words[i]
                (key3, key4, word) = words[i]
                if not word:
                    continue
                # convert keys from indices to ASCII codes (skip 0:space).
                keys = [idx_to_key[k] for k in (key1, key2, key3, key4) if k != 0]
                try:                    
                    #print("---------{} {} {} {} {} {} {} {} {} {}\n".format("".join(keys),real, word ,w1,w2,w3,w4,w5,w6,w7))
                    #sys.exit()
                    out.write("{} {}\n".format("".join(keys), word))
                except Exception as e:
                    print(e)
        out.write(cin_tail)


#def main():
#    if len(sys.argv) < 3:
#        print("liu_unitab2cin.py <liu-uni.tab file> <out *.cin file>")
#        return
#    tab_filename = sys.argv[1]
#    out_filename = sys.argv[2]
#convert_liu_unitab(tab_filename, out_filename)