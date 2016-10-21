# -*- coding: utf-8 -*-
import sys
import string
import re

if len(sys.argv)<4:
    print "usage: %s 参考文本 input_file output_file "%(sys.argv[0])
    sys.exit(0)

fp_in_cankao=open(sys.argv[1])
fp_in=open(sys.argv[2])
fp_out = open(sys.argv[3],"w")

dict_in={}
ii =0;
all_line_in=fp_in.readlines()
for line in all_line_in:
    ii += 1;
    if ('\n' == line[-1] ):
        line = line[:-1]

    line = line.lower();
    dict_in[line] = 1;
    if(ii%10000 == 0):
        print("add to dict %d "%(ii));


list_top_num = [0.0,0.0,0.0,0.0,0.0]; ##  前面 5000/1w/2w/3w/4w
#for ii in range(0,30):
#    cc = 1000*(ii+1)
#    list_top_num[ii] = 0.0;

num_all = 0;
num_all_cankao = 0;
ii=0;
for line in fp_in_cankao:
    ii += 1;
    if (ii%10000 == 0):
        print("load map :%d"%(ii));
    vec_line = line.split('\t');
    if len(vec_line) < 2:
        print("cankao format err");
        continue;
    word = vec_line[0]
    word = word.lower();
    num = int(vec_line[1])
    if (1 == num):
        print("cankao count==1");
        break;
    
    num_all_cankao += num;
    if(dict_in.has_key(word)):
        num_all += num;
        #print("ttt:%d"%(ii));
        if (ii<5000):
            list_top_num[0] += 1;
        if (ii<10000):
            list_top_num[1] += 1;
        if (ii<20000):
            list_top_num[2] += 1;
        if (ii<30000):
            list_top_num[3] += 1;
        if (ii<40000):
            list_top_num[4] += 1;
    elif (ii<20000):
        fp_out.write("%s\n"%(word))


list_top_num[0] = list_top_num[0]/5000.0;
list_top_num[1] = list_top_num[1]/10000.0;
list_top_num[2] = list_top_num[2]/20000.0;
list_top_num[3] = list_top_num[3]/30000.0;
list_top_num[4] = list_top_num[4]/40000.0;


ratio = float(num_all)/float(num_all_cankao);
fp_out.write("ratio:%.4f\n"%(ratio))
fp_out.write("top 5000 ratio:%.4f\n"%(list_top_num[0]))
fp_out.write("top 10000 ratio:%.4f\n"%(list_top_num[1]))
fp_out.write("top 20000 ratio:%.4f\n"%(list_top_num[2]))
fp_out.write("top 30000 ratio:%.4f\n"%(list_top_num[3]))
fp_out.write("top 40000 ratio:%.4f\n"%(list_top_num[4]))
 


fp_in.close()
fp_out.close()
fp_in_cankao.close();


