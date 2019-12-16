#!/bin/bash
python3 vowpal_generate.py
vw -d learn_data.txt -f model.vw
vw -d dev_data.txt -i model.vw -p dev_preds.txt
python3 evaluate.py dev_data_actual.txt dev_preds.txt > dev_rmse.txt
vw -d test_data.txt -i model.vw -p test_preds.txt
python3 evaluate.py test_data_actual.txt test_preds.txt > test_rmse.txt
echo "Dev\n"
cat dev_rmse.txt
echo "Test\n"
cat test_rmse.txt
mkdir $1
mv dev_* learn_* test_* model.vw $1
