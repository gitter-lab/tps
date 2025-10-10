#!/bin/bash
# Submit PCSF runs with different seeds

for i in {1..100}
do
    export PCSFSEED=$i
    qsub Patil2013_nodir_042214.sge
done
