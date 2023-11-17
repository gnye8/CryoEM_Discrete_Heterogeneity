#ChimeraX 'runscript chimerax_axis_flip.py cryosparc_directory' 
#note this will find all initial volumes that were generated within a particular cryosparc directory

import os
import sys 
from chimerax.core.commands import run

initial_volumes = []
flipped_volumes = []

all_folders_files = os.listdir(f'{sys.argv[1]}')
for job in all_folders_files:
    if job[0] == 'J':
        files = os.listdir(f'{sys.argv[1]}/{job}')
        for file in files:
            if file[-16:] == 'final_volume.mrc':
                initial_volumes.append(f'{sys.argv[1]}/{job}/{file}')
                flipped = file[:-16] + 'axis_flipped_' + file[-16:]
                flipped_volumes.append(f'{sys.argv[1]}/{job}/{flipped}')
#print(initial_volumes)
counter = 0
for idx in range(1,len(initial_volumes)*2,2):
    print(idx)
    print(idx+1)
    print(counter)
    print(initial_volumes[counter])
    print(flipped_volumes[counter])
    run(session, f"open {initial_volumes[counter]}")
    run(session, f"vop flip #{idx} axis z") 
    run(session, f"save {flipped_volumes[counter]} #{idx+1}")
    counter += 1
run(session, "exit")
