#!/bin/bash
# Summarize the seed networks

prizefile=/nfs/data/agitter/MSG/data/terminal/McKenna2014_aggregated_replicateABC_proteinPrizes_firstProtein.txt
basedir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_060414
tgzname=McKenna2014_agg_repABC_firstProt_optimalForests.tgz

########
beta=0.15
mu=0.003

indir=${basedir}/beta${beta}_mu${mu}
pattern=McKenna2014_agg_repABC_firstProt*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile $prizefile --outfile ${indir}/McKenna2014_agg_repABC_firstProt_100ForestSummary

cd $indir
tar -cvzf $tgzname $pattern
cd ~

########
beta=0.50
mu=0.010

indir=${basedir}/beta${beta}_mu${mu}
pattern=McKenna2014_agg_repABC_firstProt*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile $prizefile --outfile ${indir}/McKenna2014_agg_repABC_firstProt_100ForestSummary

cd $indir
tar -cvzf $tgzname $pattern
cd ~


########
beta=0.75
mu=0.007

indir=${basedir}/beta${beta}_mu${mu}
pattern=McKenna2014_agg_repABC_firstProt*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --prizefile $prizefile --outfile ${indir}/McKenna2014_agg_repABC_firstProt_100ForestSummary

cd $indir
tar -cvzf $tgzname $pattern
cd ~
