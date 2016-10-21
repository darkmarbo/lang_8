# -*- coding: utf-8 -*-
import os
import sys
import string
import re

if len(sys.argv)<5:
    print "usage: %s input_dir output_file charset.list up2low "%(sys.argv[0])
    sys.exit(0)

dir_in=sys.argv[1]
f_out=open(sys.argv[2],'w')
fp_charset = open(sys.argv[3])
fp_up2low = open(sys.argv[4])

char_list_up=[]
char_list_low=[]
dict_up2low={}
list_map=[];
map_all={}; 

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


### word upper to lower
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


### main process  : mix dict > out
list_dir=os.listdir(dir_in)
for file in list_dir:

    map_temp={};

    file_path=os.path.join(dir_in,file);
    print(file_path);
    fp = open(file_path);

    for line in fp:
        try:
            list_line = line.decode('utf-8').split('\t');
        except Exception as e:
            print(e);
            continue;

        if len(list_line)<2:
            continue;

        word = list_line[0]
        count = int(list_line[1]);
        #print("%d"%(count));
        if map_temp.has_key(word):
            print("err!");
            continue;
        map_temp[word] = count;

        if map_all.has_key(word):
            map_all[word] += count;
        else:
            map_all[word]=count;

    list_map.append(map_temp);
    fp.close();
    
print("%d len"%(len(map_all.keys())));
for key in map_all.keys():

    #### #####################################
    if is_up(key) == 1:
        w_low = upp2low(key);
        if map_all.has_key(w_low):
            #print key;
            continue;


    f_out.write("%s\t%d"%(key.encode('utf-8'),map_all[key]));
    for mp in list_map:
        if mp.has_key(key): 
            f_out.write("\t%d"%(mp[key]));
        else:
            f_out.write("\t0");
    f_out.write("\n");



f_out.close()
fp_up2low.close();
fp_charset.close();





