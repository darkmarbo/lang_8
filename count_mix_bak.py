# -*- coding: utf-8 -*-
import os
import sys
import string
import re

if len(sys.argv)<3:
	print "usage: %s input_dir output_file"%(sys.argv[0])
	sys.exit(0)

dir_in=sys.argv[1]
f_out=open(sys.argv[2],'w')

list_map=[];
map_all={}; 
list_dir=os.listdir(dir_in)
for file in list_dir:
    map_temp={};
    file_path=os.path.join(dir_in,file);
    print(file_path);
    fp = open(file_path);
    for line in fp:
        list_line=line.split("\t");
        if len(list_line)<2:
            continue;
        word=list_line[0]
        count=int(list_line[1]);
        #print("%d"%(count));
        if map_temp.has_key(word):
            print("err!");
            continue;
        map_temp[word]=count;

        if map_all.has_key(word):
            map_all[word] += count;
        else:
            map_all[word]=count;

    list_map.append(map_temp);
    fp.close();
    
print("%d len"%(len(map_all.keys())));
for key in map_all.keys():
    f_out.write("%s\t%d"%(key,map_all[key]));
    for mp in list_map:
        if mp.has_key(key): 
            f_out.write("\t%d"%(mp[key]));
        else:
            f_out.write("\t0");
    f_out.write("\n");


#dict_in={}
#all_line_in=f_in.readlines()
#for line in all_line_in:
#	vec_word=re.split(' |\n|,|\r|\.|\$|!|-|\'|%|[0-9]|;',line)
#	for word in vec_word:
#		if word=='':
#			continue
#		if dict_in.has_key(word):
#			dict_in[word]=dict_in[word]+1
#		else:
#			dict_in[word]=1
#
#for w in dict_in.keys():
#	#f_out.write("%d\t%s\n"%(dict_in[w],w))
#	f_out.write("%s\t%d\n"%(w,dict_in[w]))
#
#f_in.close()

f_out.close()
	
