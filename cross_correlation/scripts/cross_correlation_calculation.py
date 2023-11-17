import mrcfile
import os
import numpy as np
import pandas as pd
import argparse
import json
from determine_contour_levels import *
from get_vesper_output_dict import *

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--cryosparc_directory', required=True)
    parser.add_argument('--path_to_original_maps', required=True)
    parser.add_argument('--outputs_folder', required=True)
    parser.add_argument('--path_to_VESPER', required=True)
    args=parser.parse_args()

    initial_volume_files = []
    volumes = []
    fmn_ct_levels = []
    samiv_ct_levels = []
    
    all_files_folders = os.listdir(f'{args.cryosparc_directory}')
    for job in all_files_folders:
        if job[0] == 'J':
            files = os.listdir(f'{args.cryosparc_directory}/{job}')
            for file in files:
                if file[-16:] == 'final_volume.mrc':
                    initial_volume_files.append(f'{args.cryosparc_directory}/{job}/{file}')
    for volume in initial_volume_files:
        fmn_contour_level = get_contour_level(f'{args.path_to_original_maps}/2yif.mrc', volume)
        samiv_contour_level = get_contour_level(f'{args.path_to_original_maps}/6ues.mrc', volume)
        fmn_ct_levels.append(fmn_contour_level)
        samiv_ct_levels.append(samiv_contour_level)
        volumes.append(f'{volume[len(args.cryosparc_directory)+6:-4]}')
    print('finished one')
    contour_levels_df = pd.DataFrame(zip(initial_volume_files, volumes, fmn_ct_levels, samiv_ct_levels), 
        columns=['path', 'volume', 'fmn_contour_level', 'samiv_contour_level'])
    contour_levels_df.to_csv(f'{args.outputs_folder}/contour_levels.csv')

    os.system(f'mkdir {args.outputs_folder}/vesper_outputs')
    for index,row in contour_levels_df.iterrows():
        path_to_volume = row['path']
        volume = row['volume']
        fmn_ct_level = row['fmn_contour_level']
        samiv_ct_level = row['samiv_contour_level']
        os.system(f'{args.path_to_VESPER} -a {args.path_to_original_maps}/2yif.mrc -b {path_to_volume} -t 0 -T {fmn_ct_level} > {args.outputs_folder}/vesper_outputs/{volume}_FMN')
        os.system(f'{args.path_to_VESPER} -a {args.path_to_original_maps}/6ues.mrc -b {path_to_volume} -t 0 -T {samiv_ct_level} > {args.outputs_folder}/vesper_outputs/{volume}_SAMIV')

    vesper_outputs = os.listdir(f'{args.outputs_folder}/vesper_outputs')
    all_models_dict = {}
    for vesper_output_file in vesper_outputs:
        vesper_output_dict = get_transformation_dict_from_vesper_output(f'{args.outputs_folder}/vesper_outputs/{vesper_output_file}')
        all_models_dict[vesper_output_file] = get_vesper_output_dict

    with open(f'{args.outputs_folder}/vesper_alignement_data.json', 'w') as fp:
        json.dump(all_models_dict, fp)




