#!/bin/bash
# Submit PCSF runs with different prizes and seeds

# Parameters that do not vary
w=0.1
D=10
r=0.01
g=1e-3


# Parameters that vary
b=0.55
m=0.008
prizes=first

# Create the conf file
filename=conf/conf_${w}_${b}_${D}_${m}_${r}_${g}.txt
touch $filename
printf "w = ${w}\n" >> $filename
printf "b = ${b}\n" >> $filename
printf "D = ${D}\n" >> $filename
printf "mu = ${m}\n" >> $filename
printf "r = ${r}\n" >> $filename
printf "g = ${g}\n" >> $filename

# Submit the job with the configuration file and seed
export conf=$filename
export beta=$b
export mu=$m
export prizetype=$prizes

for s in {1..100}
do
    export seed=$s
    qsub McKenna2014_061714.sge
done





# Parameters that vary
b=0.55
m=0.008
prizes=firstprev

# Create the conf file
filename=conf/conf_${w}_${b}_${D}_${m}_${r}_${g}.txt
touch $filename
printf "w = ${w}\n" >> $filename
printf "b = ${b}\n" >> $filename
printf "D = ${D}\n" >> $filename
printf "mu = ${m}\n" >> $filename
printf "r = ${r}\n" >> $filename
printf "g = ${g}\n" >> $filename

# Submit the job with the configuration file and seed
export conf=$filename
export beta=$b
export mu=$m
export prizetype=$prizes

for s in {1..100}
do
    export seed=$s
    qsub McKenna2014_061714.sge
done






# Parameters that vary
b=0.65
m=0.010
prizes=prev

# Create the conf file
filename=conf/conf_${w}_${b}_${D}_${m}_${r}_${g}.txt
touch $filename
printf "w = ${w}\n" >> $filename
printf "b = ${b}\n" >> $filename
printf "D = ${D}\n" >> $filename
printf "mu = ${m}\n" >> $filename
printf "r = ${r}\n" >> $filename
printf "g = ${g}\n" >> $filename

# Submit the job with the configuration file and seed
export conf=$filename
export beta=$b
export mu=$m
export prizetype=$prizes

for s in {1..100}
do
    export seed=$s
    qsub McKenna2014_061714.sge
done
