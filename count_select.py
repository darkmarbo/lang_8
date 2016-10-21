# -*- coding: utf-8 -*-
import os
import sys
import string
import re
import traceback

if len(sys.argv)<4:
	print "usage: %s input_file num_dict charset.txt"%(sys.argv[0])
	print "example: %s dict_all.txt 5 charset.txt"%(sys.argv[0])
	sys.exit(0)

file_name = sys.argv[1];
num_dict = int(sys.argv[2]);
fp_charset = open(sys.argv[3])

file_all_cap = file_name + "_WORD1"
file_stt_cap = file_name + "_Word2"
file_middle_cap = file_name + "_wORd3"
file_err = file_name + "_select_err"
file_ratio = file_name + "_select_rate"

fp_in = open(file_name)
fp_err = open(file_err,"w");
fp_all_cap = open(file_all_cap,"w");
fp_stt_cap = open(file_stt_cap,"w");
fp_middle_cap = open(file_middle_cap,"w");
fp_ratio = open(file_ratio,"w");

max_bili = 0.95;
top_N = 1; ### 前面1000个 最好保留

char_list_up=[]
char_list_low=[]
char_list_yuanyin=[]
char_list_fuyin=[]

#### read charset list
for line in fp_charset:
    try:
        vec_line = line.decode('utf-8').split('\t');
    except Exception as e:
        print(e);
        vec_line=[];
    if len(vec_line) < 3:
        continue;
    word = vec_line[0]
    num = int(vec_line[1])
    num_yy = int(vec_line[2])
    if num == 1:
        char_list_up.append(word);
    elif num == 0:
        char_list_low.append(word);

    if num_yy == 1:
        char_list_yuanyin.append(word);
    elif num_yy == 0:
        char_list_fuyin.append(word);
print("yuanyin:\n");
print(char_list_yuanyin);
print("fuyin:\n");
print(char_list_fuyin);

##### is up?
def is_up(word):

    is_all_cap=1;
    is_stt_cap=0;
    is_cap = 0;

    ii=0;
    for c in word:
        if c in char_list_up:
            is_cap =1;
            if(ii==0):
                is_stt_cap = 1;
        else:
            is_all_cap =0;

        ii += 1;

    if(is_all_cap == 1):
        return(1);
    elif(is_stt_cap == 1):
        return(2);
    elif(is_cap == 1):
        return(3);
    else:
        return(0);

def check_one(list_num):
    flag = 0;
    num_all =0;
    for num in list_num:
        num_all += num;
        if (num == 0):
            flag += 1;

    for num in list_num:
        bili = float(num)/float(num_all);
        if (bili > max_bili):
            flag = -1;

    return (flag);

### 检测词的组成结构
### 全是元音返回1、全是辅音返回2、出现连续3个以上相同字符的返回3
### 其他情况返回 0
def check_word(word):
    flag = 0;
    num_yuanyin =0;
    num_fuyin =0;
    num_all = 0;
    num_same = 1;
    w_old = '';
    if(word[-1] == '\n'):
        word = word[:-1]

    for w in word:
        num_all += 1;
        if w in char_list_yuanyin:
            num_yuanyin += 1;
        elif w in char_list_fuyin:
            num_fuyin += 1;

        if(w == w_old):
            num_same += 1;
        else:
            num_same = 1;
        if(num_same > 2):
            return (3);

        w_old = w;

    #print("%d\t%d\t%d\n"%(num_all,num_yuanyin,num_fuyin));
    if(num_all == num_yuanyin):
        return(1);
    if(num_all == num_fuyin):
        return(2);
        

    return (0);

list_fp = [];
for ii in range(0,num_dict):
    out_name = file_name + "_select_%d"%(ii)
    f_out = open(out_name,'w')
    list_fp.append(f_out);

ii_num = 0;
num_all_count = 0; # 记录输入词典的所有count和
num_err = 0;
list_num_all = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]; ## 记录 _0 _1 ……  每个词典的count和
for line in fp_in:
    ii_num += 1;
    try:
        list_line = line.decode('utf-8').split("\t");
    except Exception as e:
        print(e);
        list_line = [];
    num_temp = len(list_line)-2;
    if(num_temp < 1):
        print("dict format err!");
        continue;
    if(ii_num == 1):
        print("dict_num:%d"%(num_temp));
    if(num_dict != num_temp):
        print("dict format err!");
        continue;


    word = list_line[0];
    num_1 = int(list_line[1]);

    ###  a b c d 
    if (1 == len(word)):
        fp_err.write("%s"%(line));
        continue;

    ### PS MR IT capital 
    is_up_flag = is_up(word);
    if (1 == is_up_flag):
        fp_all_cap.write("%s"%(line));
        continue;
    elif(2 == is_up_flag):
        fp_stt_cap.write("%s"%(line));
        continue;
    elif(3 == is_up_flag):
        fp_middle_cap.write("%s"%(line));
        continue;

    num_all_count += num_1;

    ## error  aaa   bbb  bcd aou
    flag_word = check_word(word);
    ### aaa bbb
    if (3 == flag_word ):
        num_err += num_1;
        fp_err.write("%s"%(line));
        continue;
    ### aou 全是元音
    elif (1 == flag_word and ii_num > top_N):
        num_err += num_1;
        fp_err.write("%s"%(line));
        continue;
    ### aou 全是辅音
    elif (2 == flag_word and ii_num > top_N):
        num_err += num_1;
        fp_err.write("%s"%(line));
        continue;


    list_num = []
    for ii in range(2,num_dict+2):
        num_int = int(list_line[ii])
        list_num.append(num_int);
        

    flag = check_one(list_num);

    for ii in range(0,num_dict):
        if(flag == ii):
            list_fp[ii].write("%s"%(line));
            list_num_all[ii] += num_1;

    ### error
    if (-1 == flag):
        num_err += num_1;
        fp_err.write("%s"%(line));

for ii in range(0,num_dict):
    list_num_all[ii] = float(list_num_all[ii])/float(num_all_count);
    fp_ratio.write("%d dict:%.4f\t\n"%(ii,list_num_all[ii]));

bili_err = float(num_err)/float(num_all_count); 
fp_ratio.write("err dict:%.4f\t\n"%(bili_err));

fp_in.close();
for ii in range(0,num_dict):
    f_out.close();

fp_err.close();
fp_stt_cap.close();
fp_middle_cap.close();
fp_all_cap.close();
fp_ratio.close();

