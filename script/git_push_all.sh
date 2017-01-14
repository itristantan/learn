#!/bin/bash

IFS=","
dname=`pwd`
dts=`date +'%Y-%m-%d %H:%M:%S'`

projects_name=(leopard notebook samples learn)

for var in ${projects_name[@]}
do
    echo cd $dname/$var
    cd $dname/$var

    echo "git add ."
    git add .

    echo "git commit -m $dts"
    git commit -m "$dts"

    echo "git push"
    git push

done
