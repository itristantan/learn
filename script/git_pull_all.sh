#!/bin/bash

dname=`pwd`
projects_name=(leopard notebook samples learn project)

for var in ${projects_name[@]}
do
    echo cd $dname/$var
    cd $dname/$var

    echo git pull
    git pull

done