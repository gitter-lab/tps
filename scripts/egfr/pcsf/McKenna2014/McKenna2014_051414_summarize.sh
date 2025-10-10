#!/bin/bash
# Summarize the seed networks

########
beta=1.0
mu=0.01

indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_051414/beta${beta}_mu${mu}
pattern=McKenna2014_repC_firstProt*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --outfile /nfs/data/agitter/MSG/results/egfr/McKenna2014_051414/beta${beta}_mu${mu}/McKenna2014_repC_firstProt_100ForestSummary

cd $indir
tar -cvzf McKenna2014_repC_firstProt_optimalForests.tgz $pattern
cd ~

########
beta=1.0
mu=0.05

indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_051414/beta${beta}_mu${mu}
pattern=McKenna2014_repC_firstProt*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --outfile /nfs/data/agitter/MSG/results/egfr/McKenna2014_051414/beta${beta}_mu${mu}/McKenna2014_repC_firstProt_100ForestSummary

cd $indir
tar -cvzf McKenna2014_repC_firstProt_optimalForests.tgz $pattern
cd ~


########
beta=0.1
mu=0.01

indir=/nfs/data/agitter/MSG/results/egfr/McKenna2014_051414/beta${beta}_mu${mu}
pattern=McKenna2014_repC_firstProt*optimalForest.sif

python /nfs/data/agitter/MSG/src/SummarizeSif.py --indir $indir --pattern $pattern --outfile /nfs/data/agitter/MSG/results/egfr/McKenna2014_051414/beta${beta}_mu${mu}/McKenna2014_repC_firstProt_100ForestSummary

cd $indir
tar -cvzf McKenna2014_repC_firstProt_optimalForests.tgz $pattern
cd ~
