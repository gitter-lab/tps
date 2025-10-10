#!/bin/bash
# Summarize the seed networks

########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_060314
pattern=McKenna2014_agg_repABC_firstProt*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_aggregated_replicateABC_proteinPrizes_firstProtein.txt --outfile /nfs/data/agitter/MSG/results/egfr/McKenna2014_060314/McKenna2014_agg_repABC_firstProt_100ForestSummary

cd $indir
tar -cvzf McKenna2014_agg_repABC_firstProt_optimalForests.tgz $pattern
cd ~
