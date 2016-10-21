# -*- coding: utf-8 -*-
import sys
import string
import re

if len(sys.argv)<4:
    print "usage: %s input_file output_file charset "%(sys.argv[0])
    sys.exit(0)

char_list_up=[]
char_list_low=[]
f_in=open(sys.argv[1])
f_out=open(sys.argv[2],'w')
fp_charset = open(sys.argv[3])

dict_in={}
dict_new={}

#### read charset list
for line in fp_charset:
    vec_line = line.split('\t');
    if len(vec_line) < 2:
        continue;
    word = vec_line[0]
    num = int(vec_line[1])
    if num == 1:
        char_list_up.append(word);
    elif num == 0:
        char_list_low.append(word);

##### is up?
def is_up(word):
    for c in word:
        if c in char_list_up:
            return(1);
    return(0);
    
print("charset_up_list:\n");
print(char_list_up);

num_up = 0;
num_all = 0;
all_line_in=f_in.readlines()
for line in all_line_in:
    vec_word=re.split('\t',line)
    if (len(vec_word) < 2):
        continue;
    word = vec_word[0];
    num = vec_word[1];
    num_all += 1;
    flag = is_up(word);
    if (1 == flag):
        num_up += 1;
        f_out.write("%s"%(line))

f_out.write("num_all:%d\nnum_up:%d\n"%(num_all,num_up))
    


f_in.close()
f_out.close()
fp_charset.close();


