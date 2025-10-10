#!/bin/bash
# Submit PCSF runs with different seeds

for i in {1..100}
do
    export PCSFSEED=$i
    qsub Patil2013_040314.sge
    qsub Patil2013_nokegg_040314.sge
done
