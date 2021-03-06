#!/bin/bash
# Run PCSF multiple times using the parameters set in the wrapper
# on a randomized network, summarize the PCSF output, and run TPS

echo _CONDOR_JOB_IWD $_CONDOR_JOB_IWD
echo Cluster $cluster
echo Process $process
echo RunningOn $runningon
echo

# The randomized network index is 1-based but the process id is 0-based
index=$((process+1))
edgefile=${networkprefix}${index}.txt

# Create an output subdirectory for each randomized network
subdirpath=${outpath}/randomized${index}
mkdir -p $subdirpath

# Use different seeds for each run, which will control the random edge noise
# Create a family of the requested number of forests
for seed in $(seq 1 $forests)
do
	outlabel=${prizename}_beta${beta}_mu${mu}_omega${omega}_seed${seed}

	# Create the Forest command
	# Do not run with noisy edges because the r parameter in the configuration
	# file is already being used to add edge noisy with msgsteiner
	CMD="python $oipath/scripts/forest.py \
		-p $prizefile \
		-e $edgefile \
		-c $conf \
		-d $sources \
		--msgpath=$msgsteinerpath \
		--outpath=$subdirpath \
		--outlabel=$outlabel \
		--cyto30 \
		--noisyEdges=0 \
		-s $seed"

	echo
	echo "********** PCSF run ${seed} **********"
	echo $CMD
	$CMD
done

# The filename pattern is used to collect all of the PCSF output files
pattern=${prizename}_beta${beta}_mu${mu}_omega${omega}

CMD="python pcsf/summarize_sif.py --indir ${subdirpath} \
	--pattern ${pattern}*optimalForest.sif \
	--prizefile $prizefile \
	--outfile ${subdirpath}/${pattern}_summary"

echo
echo $CMD
$CMD

# Run TPS on the input data provided in the wrapper file and the
# summarized PCSF forests
## Format the list of sources from the sources file provided to PCSF
sourcearg=""
while read -r line || [[ -n "$line" ]]; do
	sourcearg+="--source $line "
done < $sources
## Strip undesired whitespace and convert to a single space
sourcearg=`echo ${sourcearg} | tr -s [:space:] " "`

network=${subdirpath}/${pattern}_summary_union.tsv
tpspartialmodel=${tpspartialmodelprefix}${index}.sif

## Use the randomized network-derived partial model and the PCSF summary
## created above
CMD="scripts/run \
	--network $network \
	--timeseries $tpstimeseries \
	--firstscores $tpsfirstscores \
	--prevscores $tpsprevscores \
	--partialmodel $tpspartialmodel \
	--peptidemap $tpspeptidemap \
	$sourcearg \
	--threshold $tpsthreshold \
	--outfolder $subdirpath \
	--outlabel tps"

echo
echo $CMD
$CMD

# Track which version of TPS was run
echo
echo "TPS version:"
scripts/run --version

# Track which version of Omics Integrator was run
echo
echo "Omics Integrator version:"
cd $oipath
python setup.py --version
