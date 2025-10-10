#!/bin/bash
# Summarize the seed networks

########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_052114
pattern=McKenna2014_repC_firstProt*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_replicate_C_proteinPrizes_firstProtein.txt --outfile /nfs/data/agitter/MSG/results/egfr/McKenna2014_052114/McKenna2014_repC_firstProt_100ForestSummary

cd $indir
tar -cvzf McKenna2014_repC_firstProt_optimalForests.tgz $pattern
cd ~
