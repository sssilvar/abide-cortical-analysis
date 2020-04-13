#!/bin/env python3
import os
from os.path import join
from multiprocessing import cpu_count

DATASET_FOLDERS = ['/user/ssilvari/home/Documents/data/ABIDE/ABIDE-I', '/user/ssilvari/home/Documents/data/ABIDE/ABIDE-II']
SUBJECTS_DIR = '/user/ssilvari/home/Documents/data/ABIDE_FS'


def find_nii_files():
    """ Find NIFTI files inside DATASET_FOLDERS """
    nii_files = []
    for folder in DATASET_FOLDERS:
        for root, dirs, files in os.walk(folder):
            for f in files:
                if f == 'mprage.nii' or f =='anat.nii':
                    nii_path = join(root, f)
                    nii_files.append(nii_path)
    return nii_files

def print_and_exec(cmd):
    """ Prints and executes a command in terminal """
    print(cmd)
    os.system(cmd)


def autorecon_2(file_path):
    """ Performs segmentation pipeline using FreeSurfer (up to autorecon_2) """

    # Check if subject belongs to ABIDE I or II
    if 'ABIDEII' in file_path.upper() or 'ABIDE-II'in file_path.upper():
        sid = file_path.split('/')[-4]
    else:
        sid = file_path.split('/')[-7].split('_')[-1]

    # Create the command and run it.
    # If you have less than 8GB of RAM change /dev/shm to {SUBJECTS_DIR}
    # As we just want to perform Region segmentation (no subcortical reconstruction)
    # we need to run two commands:
    #
    # 1. Normalization + brain extraction (-autorecon1)
    # 2. Segmentation (-autorecon2)
    threads = cpu_count() // 2 # Use half of CPUs

    cmd = f'recon-all -i {file_path} -s {sid} -sd /dev/shm -openmp {threads} -no-isrunning -autorecon1'
    print_and_exec(cmd)

    cmd = f'recon-all -s {sid} -sd /dev/shm -openmp {threads} -no-isrunning -autorecon2'
    print_and_exec(cmd)

    # Remove if previously existed
    cmd = f'rm -rf {SUBJECTS_DIR}/sid'
    print_and_exec(cmd)

    # Move from /dev/shm back to disk
    cmd = f'mv -v /dev/shm/{sid} {SUBJECTS_DIR}'
    print_and_exec(cmd)

    print()


if __name__ == "__main__":
    # Clear screen (just to tide it)
    os.system('clear')

    # Find T1 NIFTI files
    nii_files = find_nii_files()

    # Run the pipeline for each file
    for nii_file in nii_files:
        autorecon_2(nii_file)
    

