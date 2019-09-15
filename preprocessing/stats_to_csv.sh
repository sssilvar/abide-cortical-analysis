#!/usr/bin/env bash
export SUBJECTS_DIR='/home/jullygh/ABIDE_II_FS'
echo "Subjects Directory: ${SUBJECTS_DIR}"

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT=$(dirname ${CURRENT_DIR})
DATA_CSV="${ROOT}/data/subjects.csv"

SUBJECTS=` awk -F";" '{ print $1 }' ${DATA_CSV}`
SCRIPT='python2 /usr/local/freesurfer/bin/aparcstats2table'


# Parse stats to csv
# Documentation: https://surfer.nmr.mgh.harvard.edu/fswiki/aparcstats2table
# Example:
#     aparcstats2table --subjects bert ernie fred margaret --hemi rh --meas thickness --tablefile aparc_stats.txt

for hemi in "lh" "rh"
do
    for meas in "thickness" "meancurv"
    do
        FEATURES_FILE="${SUBJECTS_DIR}/cortical_${meas}_${hemi}.csv"
        CMD="
        ${SCRIPT} --subjects ${SUBJECTS}
        --hemi ${hemi}
        --meas ${meas}
        --delimiter comma
        --skip
        --tablefile ${FEATURES_FILE}
        "
        echo ${CMD}
    done
done
