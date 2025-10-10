#!/bin/bash
# Submit PCSF runs with different seeds

for i in {1..100}
do
    export PCSFSEED=$i
    qsub Cao2012_021914.sge
done
