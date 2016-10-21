#!/bin/sh -x

if(($#<4));then
    echo "usage: $0 text_dir charset_list dict_num up2low.map "
    echo "example: $0 text en-gb.list 3 ru-ru.chaset.up "
    exit 
fi

###################### 变量创建 #####################################
### 目录：里面存放每种语料的文件夹
text_dir=$1
### 字符集：第二列对应大小写、第三类对应元音和辅音
charset_list=$2
### 类别个数
dict_num=$3
up2low_file=$4

tmp="temp"
### 去标点、非字符集、换行等操作后 
out_dir=${text_dir}_pro
### 按照切分出的行来进行去重
out_dir_sort=${text_dir}_pro_sort
### 最终生成的每类文本对应的词典
out_dir_dict=${text_dir}_dict

####################### 删除历史数据 ########################### 

rm -rf  $out_dir && mkdir -p $out_dir 
rm -rf  $out_dir_sort && mkdir -p $out_dir_sort 
rm -rf $tmp && mkdir -p $tmp
rm -rf  $out_dir_dict && mkdir -p $out_dir_dict 

####################### 处理语料 #############################
####### 生成 test_pro_sort 中对应目录
ls -1 $text_dir|while read sub_dir
do
    echo "process $text_dir/$sub_dir ..."

    ### 1111 处理目录 将目录中的所有文件 断句
    python handleCorpus.py $text_dir/$sub_dir $charset_list 
    rm -rf $out_dir/${sub_dir} && mkdir -p $out_dir/${sub_dir}
    mv $text_dir/$sub_dir/*.ok  $out_dir/$sub_dir/
    rm -rf $text_dir/$sub_dir/*.del
    
    ### 222 将处理过的文本去重
    mkdir -p $out_dir_sort/$sub_dir
    ls -1 $out_dir/$sub_dir/ |while read file
    do
        echo "sort uniq $out_dir/$sub_dir/$file ..."
        #### 去掉重复的句子 
        sort $out_dir/$sub_dir/$file |uniq > $out_dir_sort/$sub_dir/${file}.sort
        
    done

done


######################## 统计每类对应的词典  #############################
ls -1 $out_dir_sort|while read sub_dir
do
    echo "count $out_dir_sort/$sub_dir ..."

    #### 333 将每个目录下的所有文件  统计频次 相当于一个词典（uniq后 的）
    tmp_all=$tmp/${sub_dir}.all
    tmp_count=$tmp/${sub_dir}.all.count
    tmp_sort=$tmp/${sub_dir}.all.count.sort
    tmp_num=$tmp/${sub_dir}.all.count.sort.num

    cat  $out_dir_sort/$sub_dir/* > $tmp_all
    python count.py $tmp_all $tmp_count $charset_list $up2low_file 
    if(($? != 0));then
        echo "count.py err!"
        exit
    fi

    sort -n -r -k2 ${tmp_count} > ${tmp_sort}
    ###rm -rf ${tmp_all} ${tmp_count} 

    ### 444 从统计出的总词频结果中  按照97%的比例提取出最终结果
    python count_top.py  ${tmp_sort}  ${tmp_num} 
    if(($? != 0));then
        echo "count_top.py err!"
        exit
    fi
    num_line=`tail -1 ${tmp_num}|awk '{print $1}' `
    echo "最终词个数 $num_line"
    head -$num_line ${tmp_sort} > ${out_dir_dict}/${sub_dir}.${num_line}
    ###rm -rf  ${tmp_num} ${tmp_sort}

done

#################### 词典 进行合并   ############################### 
python count_mix.py $out_dir_dict ${out_dir_dict}.all $charset_list $up2low_file 
if(($? != 0));then
    echo "count_mix.py err!"
    exit
fi

### 最终排序后的词典 
sort -n -r -k2 ${out_dir_dict}.all > ${out_dir_dict}.all.sort

### 按照每类中出现的频次进行分类 
python count_select.py ${out_dir_dict}.all.sort $dict_num $charset_list
if(($? != 0));then
    echo "count_mix.py err!"
    exit
fi


#################### 生成 all word 列表 ############################ 
rm -rf temp_dict && mkdir temp_dict
cp -r temp/*.sort temp_dict
python count_mix.py temp_dict ${text_dir}.allword ${charset_list} ${up2low_file}
if(($? != 0));then
    echo "count_mix.py_2 err!"
    exit
fi

sort -n -r -k2 ${text_dir}.allword > ${text_dir}.allword.sort



