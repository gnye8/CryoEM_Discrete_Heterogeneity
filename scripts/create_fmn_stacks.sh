#!/bin/bash
#Description: script for simulating particle stacks with different noise levels and bfactors
module use /spshared/modulefiles/
module load eman2
BASE_DIR=/data/gnye8/fmn_samiv_simulation/CS-fmn-samiv-simulation-1/fmn_simulation/08302023_fmn_stacks
cd $BASE_DIR || exit

pink_noise_values=(2 4 6 8 10)

for pink_noise in ${pink_noise_values[@]}; do
    for i in {1..10}; do
        mkdir "pinknoise${pink_noise}_${i}"
        cd "pinknoise${pink_noise}_${i}"
        ln -s /data/gnye8/fmn_samiv_simulation/CS-fmn-samiv-simulation-1/fmn_simulation/08152023_fmn_stacks/pinknoise0/projections .
        cd ../
        python3 /data/gnye8/internal_EM_scripts/simulate/cryo_simulate_particle_stack.py \
            --input /data/gnye8/fmn_samiv_simulation/CS-fmn-samiv-simulation-1/fmn_simulation/2yif.pdb \
            --out_dir "pinknoise${pink_noise}_${i}" \
            --res 2.5 \
            --particles_per_stack 10000 \
            --number_particles 100000 \
            --box_size 200 \
            --apix 0.86 \
            --num_projections 99998 \
            --orientgen opt:inc_mirror=1 \
            --random_move 0 \
            --defocus_start 1.2 \
            --defocus_end 2.2 \
            --pink_noise "${pink_noise}" \
            --bfactor 60 \
            --project_exists
    done
done