#!/bin/bash

if (($# == 0)); then
    echo "usage: bash workflow.sh --config [config.yml] --execute [all|annotations|tps]"
    exit 0
fi

POSITIONAL_ARGS=()
HELP_MSG=NO

while [[ $# -gt 0 ]]; do
  case $1 in
    -c|--config)
      CONFIG="$2"
      shift # past argument
      shift # past value
      ;;
    -e|--execute)
      EXECUTE="$2"
      shift # past argument
      shift # past value
      ;;
    --help)
      HELP_MSG=YES
      shift # past argument with no value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done
set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

if [ ${HELP_MSG} == YES ]; then
	echo "usage: bash workflow.sh --config [config.yml] --execute [all|annotations|tps]"
	exit 0
fi

echo "CONFIG FILE           = ${CONFIG}"
echo "EXECUTION SETTING     = ${EXECUTE}"

if [[ -n $1 ]]; then
  echo "error: invalid arguments"
	echo "usage: bash workflow.sh --config [config.yml] --execute [all|annotations|tps]"
  exit 0
fi

echo "activate TPS environment"
eval "$(conda shell.bash hook)"
conda activate tps_workflow

if [ $? -ne 0 ]; then
   	echo "environment does not exist"
	echo "creating TPS environment"
	conda env create -f workflow/minimal_env.yml
	conda activate tps_workflow
fi
echo "environment activated"
 
python tps_runner.py --config ${CONFIG} --execute ${EXECUTE} 
