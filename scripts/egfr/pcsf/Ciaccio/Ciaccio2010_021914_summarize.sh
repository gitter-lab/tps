#!/bin/bash
# Summarize the seed networks

indir=/nfs/data/agitter/MSG/results/egfr/Ciaccio2010_021914
pattern=Ciaccio2010_phospho_con200*optimalForest.sif

python ../../../src/SummarizeSif.py --indir $indir --pattern $pattern --outfile /nfs/data/agitter/MSG/results/egfr/Ciaccio2010_021914/Ciaccio2010_phospho_con200_100ForestSummary

cd $indir
tar -cvzf Ciaccio2010_phospho_con200_optimalForests.tgz $pattern
