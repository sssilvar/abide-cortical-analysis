#!/bin/env python3
import os
from os.path import join, normpath, isfile
from multiprocessing import Pool, cpu_count

import pandas as pd
from os.path import dirname, realpath, join

root = dirname(dirname(realpath(__file__)))


def get_subject_nii_file(s):
    nii_path = join(s['DATA_FOLDER'],
                    s['CENTRE'],
                    str(s['SUBJECT_ID']),
                    'session_1',
                    'anat_1',
                    'anat.nii')
    return nii_path


def process_subject(subject_series):
    nii_file = get_subject_nii_file(subject_series)
    sid = subject_series['SUBJECT_ID']

    if isfile(nii_file):
        cmd = f'recon-all -i {nii_file} ' \
              f'-s {sid} ' \
              f'-sd {subjects_dir} ' \
              f'-all'
        print(cmd)


if __name__ == '__main__':
    # Dataset folder
    data_folder = normpath('/data/ABIDE-II/ABIDEII/Dataset')
    subjects_dir = normpath('/home/jullygh/ABIDE_II_FS')
    n_cores = cpu_count() // 1.25 if cpu_count() > 1 else cpu_count()

    # Data files
    subjects_csv = join(root, 'data/subjects.csv')
    df = pd.read_csv(subjects_csv, sep=';')
    df['DATA_FOLDER'] = data_folder
    print(f'Number of subjects: {df.shape[0]}')
    print(f'Number of CPUs: {n_cores}')

    subj_series = df.iterrows()
    for cell in subj_series:
        print(cell[1])
    # process_subject(subj_series)
