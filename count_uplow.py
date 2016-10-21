# -*- coding: utf-8 -*-
import sys
import string
import re

if len(sys.argv)<3:
    print "usage: %s input_file output_file"%(sys.argv[0])
    sys.exit(0)

char_list_up="QWERTYUIOPLKJHGFDSAZXCVBNM"
f_in=open(sys.argv[1])
f_out=open(sys.argv[2],'w')
dict_in={}
dict_new={}

def is_up(word):
    for c in word:
        if c in char_list_up:
            return(1);
    return(0);
    

all_line_in=f_in.readlines()
for line in all_line_in:
    #vec_word=re.split(' |\n|,|\r|\.|\$|!|-|\'|%|[0-9]|;',line)
    vec_word=re.split(' |\n|,|\r|\.|\$|!|;',line)
    for word in vec_word:

        if word=='' or len(word)>30:
            continue
        if word[-1] in "-\'":
            word=word[:-1]
        if word=='':
            continue
        if (word[0] in "-\'"):
            word=word[1:]
        if word=='':
            continue
            
        if dict_in.has_key(word):
            dict_in[word]=dict_in[word]+1
        else:
            dict_in[word]=1

### lower upper 
for w in dict_in.keys():
    if is_up(w) == 1:
        #print("%s"%(w));
        w_low = w.lower();
        if dict_in.has_key(w_low):
            #print("up:%s\tlow:%s"%(w,w_low));
            if dict_new.has_key(w_low):
                dict_new[w_low] = dict_in[w]+dict_new[w_low];
            else:
                dict_new[w_low] = dict_in[w]+dict_in[w_low];
        else:
            dict_new[w] = dict_in[w];
    else:
        if not dict_new.has_key(w):
            dict_new[w] = dict_in[w];
        #else:
        #    print("ttttt:%s"%(w));
    

for w in dict_new.keys():
    f_out.write("%s\t%d\n"%(w,dict_new[w]))

f_in.close()
f_out.close()


