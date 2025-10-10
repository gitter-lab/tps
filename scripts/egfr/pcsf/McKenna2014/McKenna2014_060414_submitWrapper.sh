#!/bin/bash
# Submit PCSF runs with different beta, mu, and seeds

# Parameters that do not vary
w=0.1
D=10
r=0.01
g=1e-3


# Parameters that vary
b=0.75
m=0.007

# Create the conf filename
filename=conf/conf_${w}_${b}_${D}_${m}_${r}_${g}.txt

# Submit the job with the configuration file and seed
export conf=$filename
export beta=$b
export mu=$m

for s in {1..100}
do
    export seed=$s
    qsub McKenna2014_060414.sge
done





# Parameters that vary
b=0.15
m=0.003

# Create the conf filename
filename=conf/conf_${w}_${b}_${D}_${m}_${r}_${g}.txt

# Submit the job with the configuration file and seed
export conf=$filename
export beta=$b
export mu=$m

for s in {1..100}
do
    export seed=$s
    qsub McKenna2014_060414.sge
done






# Parameters that vary
b=0.50
m=0.010

# Create the conf filename
filename=conf/conf_${w}_${b}_${D}_${m}_${r}_${g}.txt

# Submit the job with the configuration file and seed
export conf=$filename
export beta=$b
export mu=$m

for s in {1..100}
do
    export seed=$s
    qsub McKenna2014_060414.sge
done
