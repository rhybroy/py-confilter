#!/bin/bash 

mkdir ./py-confilter

for i in `ls`
do
    if [ $i == "py-confilter" ]
    then
        continue
    elif [ -d $i ]
    then
        cp -r $i ./py-confilter/
    else
        cp $i ./py-confilter/
    fi
done

cd ./py-confilter

find . -type d -name ".svn" | xargs rm -rf

cd ..

tar zfc py-confilter.tar.gz py-confilter

rm -rf py-confilter
