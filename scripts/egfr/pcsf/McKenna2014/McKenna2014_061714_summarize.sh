#!/bin/bash
# Summarize the seed networks

########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_061714/firstprev_beta0.55_mu0.008
runname=McKenna2014_agg_repABC_tukey_firstprev_firstProt
pattern=${runname}*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_aggregated_replicateABC_tukey_firstprev_proteinPrizes_firstProtein.txt --outfile ${indir}/${runname}_100ForestSummary

cd $indir
tar -cvzf ${runname}_optimalForests.tgz $pattern
cd ~





########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_061714/first_beta0.55_mu0.008
runname=McKenna2014_agg_repABC_tukey_first_firstProt
pattern=${runname}*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_aggregated_replicateABC_tukey_first_proteinPrizes_firstProtein.txt --outfile ${indir}/${runname}_100ForestSummary

cd $indir
tar -cvzf ${runname}_optimalForests.tgz $pattern
cd ~






########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_061714/prev_beta0.65_mu0.010
runname=McKenna2014_agg_repABC_tukey_prev_firstProt
pattern=${runname}*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_aggregated_replicateABC_tukey_prev_proteinPrizes_firstProtein.txt --outfile ${indir}/${runname}_100ForestSummary

cd $indir
tar -cvzf ${runname}_optimalForests.tgz $pattern
cd ~
