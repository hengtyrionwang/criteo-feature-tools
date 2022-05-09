
###
 # @Descripttion: 
 # @version: 
 # @Author: Heng Tyrion Wang
 # @Date: 2022-05-08 09:24:23
 # @LastEditors: Heng Tyrion Wang
 # @Email: hengtyrionwang@gmail.com
 # @LastEditTime: 2022-05-09 08:32:25
### 
path=$(pwd)


csv_path=${path}/csv
if [ ! -d ${csv_path} ]; then
    mkdir ${csv_path}
else
    rm -rf ${csv_path}/*
fi

python ${path}/kaggle-2014-criteo/txt2csv.py tr ${path}/dac/train.txt ${csv_path}/train.csv

printf "Format Conversion is finished! \n"

split_path=${path}/split
if [ ! -d ${split_path} ]; then
    mkdir ${split_path}
else
    rm -rf ${split_path}/*
fi

infile="train.csv"

seed=2022

python ${path}/split.py --in_path ${csv_path}/${infile} --out_path ${split_path} --seed ${seed}

printf "Dataset split is finished! \n"

count_file=fc.trva.t10.txt

if [ -f ${count_file} ]; then
    rm -rf ${count_file}
fi

python ${path}/kaggle-2014-criteo/count.py ${split_path}/train.csv > ${count_file}

printf "Feature frequence counting is finished! \n"

ffm_path=${path}/ffm
if [ ! -d ${ffm_path} ]; then
    mkdir ${ffm_path}
else
    rm -rf ${ffm_path}/*
fi

data_type=("train" "test" "valid")

for type in ${data_type[*]}
do
    python ${path}/kaggle-2014-criteo/pre-b.py ${split_path}/${type}.csv ${ffm_path}/${type}.txt
done

rm -rf ${csv_path}
rm -rf ${split_path}
rm -rf ${count_file}

printf "Feature Engineering is finished! \n"
