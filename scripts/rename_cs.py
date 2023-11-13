import numpy as np
import os
import argparse

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--cs_filename', required=True)
    parser.add_argument('--new_particle_path', required=True)
    parser.add_argument('--output_filename', required=True)
    parser.add_argument('--csg_filename', required=True)
    args=parser.parse_args()

    cs_file = np.load(args.cs_filename)
    for i in range(len(cs_file)):
        path = str(cs_file[i][1])
        cs_file[i][1] = args.new_particle_path + path

    np.save(args.output_filename, cs_file)
    os.rename(f'{args.output_filename}.npy', args.output_filename)

    with open(args.csg_filename, 'r+') as file:
        text = file.readlines()
    lines = [8, 12, 16]
    for line in lines:
        text[line] = f"    metafile: '>{args.output_filename}'\n"
    with open(args.csg_filename, 'w') as file:
        file.writelines( text )
