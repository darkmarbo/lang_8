# -*- coding: utf-8 -*-
import sys
import string
import re

if len(sys.argv)<5:
    print "usage: %s 参考发音词典 input_file output_file top_num"%(sys.argv[0])
    print "usage: %s th-th_sampa_100k.lex so_wordfreq.txt_del_cons so_wordfreq.txt_del_cons.10000 10000"%(sys.argv[0])
    sys.exit(0)

fp_in_cankao = open(sys.argv[1])
fp_in = open(sys.argv[2])
fp_out = open(sys.argv[3],"w")
top_num = int(sys.argv[4])

dict_cankao = {};
for line in fp_in_cankao:
    line = line[:-1]
    line = line.lower();
    list_line = line.split("\t");
    if len(list_line)<2:
        continue;
    word = list_line[0]
    ttt = list_line[1]
    dict_cankao[word] = ttt;
    #fp_out.write("%s\t%s\n"%(word, ttt))


num_all = 0;
num_ok = 0;
count_all = 0;
count_ok = 0;
ii =0;

###  word(html) count(1000)
for line in fp_in:
    line = line[:-1];
    lint = line.lower();
    list_line = line.split("\t");
    if len(list_line)<2:
        continue;
    word = list_line[0]
    ccc = int(list_line[1])

    #### 前面top_num个词的情况
    if num_all < top_num:
        num_all += 1;
        count_ok += ccc; 

        if dict_cankao.has_key(word):
            num_ok += 1;
        else:
            fp_out.write("%s\t%d\n"%(word, ccc))

    count_all += ccc;
    

fp_out.write("统计词数=%d\t词典覆盖词数=%d\t占比=%.4f\n"%(num_all,num_ok,float(num_ok)/float(num_all)))
fp_out.write("累计频次=%d\t总词频数=%d\t占比=%.4f\n"%(count_ok, count_all, float(count_ok)/float(count_all)))



fp_in.close()
fp_out.close()
fp_in_cankao.close();


