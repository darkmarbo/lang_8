# -*- coding: utf-8 -*-
import sys
import string
import re

if len(sys.argv)<5:
    print "usage: %s input_file output_file charset up2low "%(sys.argv[0])
    sys.exit(0)

dict_up2low={}
char_list_up=[]
char_list_low=[]
f_in=open(sys.argv[1])
f_out=open(sys.argv[2],'w')
fp_charset = open(sys.argv[3])
fp_up2low = open(sys.argv[4])

dict_in={}
dict_new={}

#### read upper2lower list
for line in fp_up2low:
    line = line[:-1]
    try:
        vec_line = line.decode('utf-8').split('\t');
    except Exception as e:
        print(e);
        continue;

    if len(vec_line) < 3:
        continue;
    word_upp = vec_line[0]
    num = int(vec_line[1])
    word_low = vec_line[2]
    if num == 1:
        dict_up2low[word_upp]=word_low;
print dict_up2low

def upp2low(line):

    line_new = '';
    for ch in line:
        if dict_up2low.has_key(ch):
            line_new += dict_up2low[ch]
        else:
            line_new += ch

    return line_new;
        

#### read charset list
for line in fp_charset:
    try:
        vec_line = line.decode('utf-8').split('\t');
    except Exception as e:
        print(e);
        continue;

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
    
### 查找字符串中 某个子串的个数
def find_str(word,sub_str):
    num = 0;
    ii = -1;
    ii = word.find(sub_str,0);
    while(ii > -1):
        num += 1;
        ii = word.find(sub_str,ii+1);


    return num;

all_line_in=f_in.readlines()
for line in all_line_in:
    #vec_word=re.split(' |\n|,|\r|\.|\$|!|-|\'|%|[0-9]|;',line)
    try:
        line_uni = line.decode('utf-8');
    except Exception as e:
        print(e);
        continue;

    vec_word=re.split(' |\n',line_uni)
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

        num_find = find_str(word,'-');
        if num_find > 2:
            continue;

        num_find = find_str(word,'\'');
        if num_find > 2:
            continue;
            
        if dict_in.has_key(word):
            dict_in[word]=dict_in[word]+1
        else:
            dict_in[word]=1

### lower upper 
for w in dict_in.keys():
    if is_up(w) == 1:
        #print("test:%s"%(w));
        w_low = upp2low(w);
        #w_low = w.lower();
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
    f_out.write("%s\t%d\n"%(w.encode('utf-8'),dict_new[w]))

f_in.close()
f_out.close()
fp_charset.close();
fp_up2low.close();


