#!/bin/bash
# Summarize the seed networks

########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_052214/beta0.5_mu0.009
pattern=McKenna2014_repC_firstProt*optimalForest.sif

# Now provide the prize file that was used to learn all of the forests
python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_replicate_C_proteinPrizes_firstProtein.txt --outfile ${indir}/McKenna2014_repC_firstProt_100ForestSummary

cd $indir
tar -cvzf McKenna2014_repC_firstProt_optimalForests.tgz $pattern
cd ~
