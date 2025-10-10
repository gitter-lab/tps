#!/bin/bash
# Summarize the seed networks

# The run using the network with KEGG edges
indir=/nfs/data/agitter/MSG/results/egfr/Patil2013_040214
# The run using the network without KEGG edges
indirnk=/nfs/data/agitter/MSG/results/egfr/Patil2013_nokegg_040214
prefix=Patil2013_wt
pattern=${prefix}*optimalForest.sif

python ../../../src/SummarizeSif.py --indir $indir --pattern $pattern --outfile $indir/${prefix}_100ForestSummary
python ../../../src/SummarizeSif.py --indir $indirnk --pattern $pattern --outfile $indirnk/${prefix}_100ForestSummary

cd $indir
tar -cvzf ${prefix}_optimalForests.tgz $pattern

cd $indirnk
tar -cvzf ${prefix}_optimalForests.tgz $pattern
