#!/bin/bash
# Submit PCSF runs with different seeds

for i in {1..100}
do
    export PCSFSEED=$i
    qsub McKenna2014_051414_b1.0_m0.01.sge
    qsub McKenna2014_051414_b1.0_m0.05.sge
    qsub McKenna2014_051414_b0.1_m0.01.sge
done
