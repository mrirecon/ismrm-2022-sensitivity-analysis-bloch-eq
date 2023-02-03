#!/bin/bash

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

# Unprep. IR bSSFP
python3 ${REL_PATH}/plot_derivatives.py ${REL_PATH}/figure_03 results/{sens,grad}_R1 results/{sens,grad}_R2 results/{sens,grad}_B1