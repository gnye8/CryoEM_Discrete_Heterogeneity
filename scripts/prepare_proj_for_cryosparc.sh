#!/bin/bash

module use /spshared/modulefiles/
BASE_DIR=/data/gnye8/fmn_samiv_simulation/CS-fmn-samiv-simulation/fmn_simulation/08092023_testing
cd $BASE_DIR || exit

pink_noise_values=(0 2 4 6 8 10)
B_values=(60)

for pink_noise in ${pink_noise_values[@]}; do
    for B in ${B_values[@]}; do
        cd "pinknoise${pink_noise}"
        python /data/gnye8/fmn_samiv_simulation/CS-fmn-samiv-simulation/fmn_simulation/rename_cs.py \
            --cs_filename particles.cs \
            --output_filename particles2.cs \
            --csg_filename particles.csg
        cd ../
    done
done
