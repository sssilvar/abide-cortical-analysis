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
                    'anat.nii.gz')
    return nii_path


def process_subject(row):
    subject_series = row[1]  # Iterrows returns a tuple (idx, row)
    nii_file = get_subject_nii_file(subject_series)
    sid = subject_series['SUBJECT_ID']
    subj_ram = '/dev/shm'

    if isfile(nii_file):
        # FreeSurfer Command (fast and furious)
        cmd = f'recon-all -i {nii_file} ' \
              f'-s {sid} ' \
              f'-sd {subj_ram} ' \
              f'-all'

        # Move folder to disk command
        mv_cmd = f'mv -v {join(subj_ram, str(sid))} {subjects_dir}'

        # Execute commands
        print(cmd)
        os.system(cmd)  # Freesurfer
        print(mv_cmd)
        os.system(mv_cmd)   # Move folder


if __name__ == '__main__':
    # Dataset folder
    data_folder = normpath('/data/ABIDE-II/ABIDEII/Dataset')
    subjects_dir = normpath('/home/jullygh/ABIDE_II_FS')
    n_cores = int(cpu_count() * 0.75) if cpu_count() > 1 else cpu_count()

    # Data files
    subjects_csv = join(root, 'data/subjects.csv')
    done_subjects_csv = join(root, 'data/done.csv')

    df = pd.read_csv(subjects_csv)
    df['DATA_FOLDER'] = data_folder

    # Check if done subjects
    if isfile(done_subjects_csv):
        done_df = pd.read_csv(done_subjects_csv, index_col=0)
        for ix in done_df.index:
            row_index = df[df['SUBJECT_ID'] == ix].index
            df.drop(row_index, axis='rows', inplace=True)

    print(f'Number of subjects: {df.shape[0]}')
    print(f'Number of CPUs: {n_cores}')

    # Iter over rows
    subj_series = df.iterrows()

    # Create a pool
    pool = Pool(n_cores)
    pool.map(process_subject, subj_series)
    pool.close()
