#!/bin/bash
# Submit PCSF runs with different beta and mu

# Parameters that do not vary
w=0.1
D=10
r=0
g=1e-3

# Loop over the different submission scripts
for sgefile in McKenna2014_061614_*_sweep.sge
do
	echo "Submitting $sgefile"
	for b in $(seq 0.05 0.05 1.0)
	do
		for m in $(seq 0 0.001 0.01)
		do
		# Create the conf file
		filename=conf/conf_${w}_${b}_${D}_${m}_${r}_${g}.txt
		touch $filename
		printf "w = ${w}\n" >> $filename
		printf "b = ${b}\n" >> $filename
		printf "D = ${D}\n" >> $filename
		printf "mu = ${m}\n" >> $filename
		printf "r = ${r}\n" >> $filename
		printf "g = ${g}\n" >> $filename

		# Submit the job with the configuration file
		export conf=$filename
		export beta=$b
		export mu=$m
		qsub $sgefile
		done
	done
done
