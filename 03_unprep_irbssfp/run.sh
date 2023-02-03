#!/bin/bash

set -euo pipefail
set -x

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

# Folder for temporary stuff
[ -d tmp ] && rm -r tmp
mkdir tmp

# Folder for results
RESULTS=${REL_PATH}/results
[ -d ${RESULTS} ] && rm -r ${RESULTS}
mkdir ${RESULTS}


TR=0.004
TE=0.002
TRF=0.00001
PREP=${TE}
FA=45
REP=1000
BWTP=4
T1=1.25
T2=0.045
ODE_TOL=1E-6

E=1.005


# Simulation

bart sim --ODE --seq IR-BSSFP,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=0,ppl=${PREP},Trf=${TRF},FA=${FA},BWTP=${BWTP},isp=0 --other ode-tol=${ODE_TOL} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/_s tmp/_d

# Slice out derivatives of each component
bart slice 4 0 tmp/_d ${RESULTS}/sens_R1
bart slice 4 2 tmp/_d ${RESULTS}/sens_R2
bart slice 4 3 tmp/_d ${RESULTS}/sens_B1


# R1

## Simulation without and with small distortion
bart sim --ODE --seq IR-BSSFP,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=0,ppl=${PREP},Trf=${TRF},FA=${FA},BWTP=${BWTP},isp=0 --other ode-tol=${ODE_TOL} -1 $(echo ${T1} ${E} | awk '{printf "%f\n",$1*$2}'):$(echo ${T1} ${E} | awk '{printf "%f\n",$1*$2}'):1 -2 ${T2}:${T2}:1 tmp/_s2


## Estimate difference quotient
bart saxpy -- -1 tmp/_s{2,} tmp/_diff  # f(x1)-f(x2)

DIFF=$(echo ${T1} ${E} | awk '{printf "%f\n", $1*(1-$2)}') # x1-x2

# Devide by x1-x2 to estimate difference quotient
bart scale -- $(echo ${DIFF} | awk '{printf "%f\n",1/$1}') tmp/_diff tmp/_grad

bart scale -- $(echo ${T1} | awk '{printf "%f\n",-($1*$1)}') tmp/_grad ${RESULTS}/grad_R1

# R2

## Simulation without and with small distortion
bart sim --ODE --seq IR-BSSFP,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=0,ppl=${PREP},Trf=${TRF},FA=${FA},BWTP=${BWTP},isp=0 --other ode-tol=${ODE_TOL} -1 ${T1}:${T1}:1 -2 $(echo ${T2} ${E} | awk '{printf "%f\n",$1*$2}'):$(echo ${T2} ${E} | awk '{printf "%f\n",$1*$2}'):1 tmp/_s2

## Estimate difference quotient
bart saxpy -- -1 tmp/_s{2,} tmp/_diff  # f(x1)-f(x2)

DIFF=$(echo ${T2} ${E} | awk '{printf "%f\n", $1*(1-$2)}') # x1-x2

# Devide by x1-x2 to estimate difference quotient
bart scale -- $(echo ${DIFF} | awk '{printf "%f\n",1/$1}') tmp/_diff tmp/_grad



# Scale to compensate for T2 <-> R2 differences
bart scale -- $(echo ${T2} | awk '{printf "%f\n",-($1*$1)}') tmp/_grad ${RESULTS}/grad_R2


# B1

## Simulation without and with small distortion
bart sim --ODE --seq IR-BSSFP,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=0,ppl=${PREP},Trf=${TRF},FA=$(echo ${FA} ${E} | awk '{printf "%f\n",$1*$2}'),BWTP=${BWTP},isp=0 --other ode-tol=${ODE_TOL} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/_s2

## Estimate difference quotient
bart saxpy -- -1 tmp/_s{2,} tmp/_diff  # f(x1)-f(x2)

DIFF=$(echo ${FA} ${E} | awk '{printf "%f\n", $1*(1-$2)}') # x1-x2

bart scale -- $(echo 1 ${DIFF} | awk '{printf "%f\n",$1/$2}') tmp/_diff tmp/_grad

# Scale to convert dFA -> dB1
bart scale -- $(echo 1 ${FA} | awk '{printf "%f\n",1/($1/$2)}') tmp/_grad ${RESULTS}/grad_B1
