import numpy as np
import os
import pandas as pd
import mrcfile
#import argparse

def get_mrc_data_headers_and_vs(mrc_filename):
    with mrcfile.open(mrc_filename) as mrc:
        return mrc.data, mrc.header, mrc.voxel_size

def calculate_voxels(data, contour_level):
    threshold = np.mean(data) + (np.std(data)*contour_level)
    contoured_data = np.where(data >= threshold, data, 0)
    return np.count_nonzero(contoured_data)

#if __name__=='__main__':
    #parser=argparse.ArgumentParser()
   # parser.add_argument('--original_map_filename', required=True)
  #  parser.add_argument('--initial_volume_filename', required=True)
 #   args=parser.parse_args()
def get_contour_level(original_map_filename, initial_volume_filename):
    og_data, og_header, og_voxel_size = get_mrc_data_headers_and_vs(original_map_filename)
    iv_data, iv_header, iv_voxel_size = get_mrc_data_headers_and_vs(initial_volume_filename)

    ## now let's check to make sure that grid size, voxel size, and cell size are all perfectly symmetrical 

    if (og_voxel_size.x != og_voxel_size.y) or (og_voxel_size.x != og_voxel_size.z) or (og_voxel_size.y 
                                                                                        != og_voxel_size.z):
        print('original map voxel size is not symmetrical')

    if (iv_voxel_size.x != iv_voxel_size.y) or (iv_voxel_size.x != iv_voxel_size.z) or (iv_voxel_size.y 
                                                                                        != iv_voxel_size.z):
        print('initial volume voxel size is not symmetrical')

    if (og_header.nx != og_header.ny) or (og_header.ny != og_header.nz) or (og_header.nx != og_header.nz):
        print('original map grid size is not symmetrical')

    if (iv_header.nx != iv_header.ny) or (iv_header.ny != iv_header.nz) or (iv_header.nx != iv_header.nz):
        print('initial volume grid size is not symmetrical')

    if (og_header.cella.x != og_header.cella.y) or (og_header.cella.y 
                                                    != og_header.cella.z) or (og_header.cella.x 
                                                                              != og_header.cella.z):
        print('original map cell size is not symmetrical')

    if (iv_header.cella.x != iv_header.cella.y) or (iv_header.cella.y 
                                                    != iv_header.cella.z) or (iv_header.cella.x 
                                                                              != iv_header.cella.z):
        print('initial volume cell size is not symmetrical')

    # now let's check that length of grid points per voxel is equal to 1

    og_grid_pts_pvoxel = (og_header.nx/og_header.cella.x)*og_voxel_size.x
    iv_grid_pts_pvoxel = (iv_header.nx/iv_header.cella.x)*iv_voxel_size.x

    if round(iv_grid_pts_pvoxel, 3) != 1.0 or round(og_grid_pts_pvoxel, 3) != 1.0:
        print('grid points per voxel is off')

    # now let's calculate the number of voxels in the original map 
    og_voxels = calculate_voxels(og_data, contour_level=0)
    #print(og_voxels)

    #now for our first while loop, which will have a coarse search of contour levels 
    iv_contour_level = 0
    iv_voxels = 0
    while iv_voxels != og_voxels:
        iv_voxels = calculate_voxels(iv_data, iv_contour_level)
        if iv_voxels < og_voxels:
            break
        iv_contour_level = iv_contour_level + 0.001

    #now for the second while loop, which will have a finer search of contour levels 
    iv_contour_level = iv_contour_level - 0.001
    while iv_voxels != og_voxels:
        iv_voxels = calculate_voxels(iv_data, iv_contour_level)
        if iv_voxels < og_voxels:
            break
        iv_contour_level = iv_contour_level + 0.000001
        
    og_volume = og_voxels * og_voxel_size.x * og_voxel_size.y * og_voxel_size.z
    iv_voxels_wanted = og_volume / (iv_voxel_size.x*iv_voxel_size.y*iv_voxel_size.z)
    #print(og_volume)
    #print(iv_voxels_wanted)
    #print(round(iv_voxels_wanted, 0))

    iv_contour_level_volume = 0
    while iv_voxels != int(round(iv_voxels_wanted, 0)):
        #print(iv_contour_level_volume)
        iv_voxels = calculate_voxels(iv_data, iv_contour_level_volume)
        #print(iv_voxels)
        if iv_voxels < int(round(iv_voxels_wanted, 0)):
            break
        iv_contour_level_volume += 0.01

    iv_contour_level_volume -= 0.001
    while iv_voxels != int(round(iv_voxels_wanted, 0)):
        iv_voxels = calculate_voxels(iv_data, iv_contour_level_volume)
        if iv_voxels < int(round(iv_voxels_wanted, 0)):
            break
        iv_contour_level_volume += 0.000001

    return iv_contour_level_volume
