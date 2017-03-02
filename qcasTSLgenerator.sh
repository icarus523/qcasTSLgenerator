#!/bin/bash

# Script to use the qcasTSLgenerator awk script. 

# To use: 
# Input Parameter #1 - CSV file to generate TSL Entry
# Input Parameter #2 - Current TSL file
# Input Parameter #3 - Output TSL file

# Command being called: 
# awk -f qcasTSLgenerator.awk 20131205\ Tech\ Services\ Item\ List.csv | cat qcas_2015_05_v01.tsl | sort -k 1,1 -k 3,3 -k 2,2 --field-separator=',' -u > new_tsl_file.tsl

`echo awk -f bin/qcasTSLgenerator.awk $1 | cat $2 | sort -k 1,1 -k 3,3 -k 2,2 --field-separator=',' -u > $3`