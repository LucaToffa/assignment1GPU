#!bin/bash

for i in 4 8 16 32
do
    for j in 2 4 8 16
    do
        if((j<=i))
        then
            make --always-make cudarun T=$i B=$j >> all.log
        fi
    done
done
