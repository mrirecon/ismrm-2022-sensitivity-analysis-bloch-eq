#!/bin/bash

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

# IR bSSFP
python3 ${REL_PATH}/plot_derivatives.py ${REL_PATH}/figure_02 ${REL_PATH}/results/h.txt ${REL_PATH}/results/{sens,grad}_R1 ${REL_PATH}/results/{sens,grad}_R2 ${REL_PATH}/results/{sens,grad}_B1
