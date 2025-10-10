#!/bin/bash
# Summarize the seed networks

########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_061614/firstprev
runname=McKenna2014_agg_repABC_tukey_firstprev_firstProt
pattern=${runname}*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_aggregated_replicateABC_tukey_firstprev_proteinPrizes_firstProtein.txt --outfile ${indir}/${runname}_100ForestSummary

cd $indir
tar -cvzf ${runname}_optimalForests.tgz $pattern
cd ~





########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_061614/first
runname=McKenna2014_agg_repABC_tukey_first_firstProt
pattern=${runname}*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_aggregated_replicateABC_tukey_first_proteinPrizes_firstProtein.txt --outfile ${indir}/${runname}_100ForestSummary

cd $indir
tar -cvzf ${runname}_optimalForests.tgz $pattern
cd ~






########
indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_061614/prev
runname=McKenna2014_agg_repABC_tukey_prev_firstProt
pattern=${runname}*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile /nfs/data/agitter/MSG/data/terminal/McKenna2014_aggregated_replicateABC_tukey_prev_proteinPrizes_firstProtein.txt --outfile ${indir}/${runname}_100ForestSummary

cd $indir
tar -cvzf ${runname}_optimalForests.tgz $pattern
cd ~
