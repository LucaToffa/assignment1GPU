#!bin/bash
module load cuda/12.1
for i in 4 8 16 32
do
    for j in 2 4 8 16
    do
        if((j<=i))
        then
            # call make on marzola
            make transpose-cluster T=$i B=$j
            # call query.sh on edu5
            sbatch ./query.sh $i $j
        fi
    done
done
