#!/bin/bash
# Summarize the seed networks

# The run using the network without directions
indirnd=/nfs/data/agitter/MSG/results/egfr/Patil2013_nodir_042214
prefix=Patil2013_wt
pattern=${prefix}*optimalForest.sif

python ../../../src/SummarizeSif.py --indir $indirnd --pattern $pattern --outfile $indirnd/${prefix}_100ForestSummary

cd $indirnd
tar -cvzf ${prefix}_optimalForests.tgz $pattern
