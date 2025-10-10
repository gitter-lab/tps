#!/bin/bash
# Submit PCSF runs with different seeds

for i in {1..100}
do
    export PCSFSEED=$i
    qsub McKenna2014_051414_b0.5_m0.009.sge
done
