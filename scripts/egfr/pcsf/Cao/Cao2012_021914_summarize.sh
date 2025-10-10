#!/bin/bash
# Summarize the seed networks

indir=/nfs/data/agitter/MSG/results/egfr/Cao2012_021914
prefix=Cao2012_slp76plus_q002
pattern=${prefix}*optimalForest.sif

python ../../../src/SummarizeSif.py --indir $indir --pattern $pattern --outfile $indir/${prefix}_100ForestSummary

cd $indir
tar -cvzf ${prefix}_optimalForests.tgz $pattern
