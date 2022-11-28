#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "This script uses the masked language model method from BERT to generate euphemisms"
    echo "Specify YEAR and MONTH (e.g. ./gab_month_gen.sh 2018 1)"
    echo "Gab dataset exists from 2016-08 to 2018-10"
    exit 1
fi

echo "YEAR: $1"
echo "MONTH: $2"

python3 ./gab_cleaning.py -y $1 -m $2
python3 ./extract_banned.py -y $1 -m $2
python3 ./bert_prediction.py -y $1 -m $2

echo "Done!"
