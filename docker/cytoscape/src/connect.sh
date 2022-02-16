#!/bin/bash

if (($# == 0)); then
    exit 0
fi

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -s|--save)
      SAVE="$2"
      shift # past argument
      shift # past value
      ;;
    -y|--style)
      STYLE="$2"
      shift # past argument
      shift # past value
      ;;
    -a|--annot)
      ANNOTATIONS="$2"
      shift # past argument
      shift # past value
      ;;
    -n|--network)
      NETWORK="$2"
      shift # past argument
      shift # past value
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

echo "SAVE FILE         = ${SAVE}"
echo "STYLE FILE        = ${STYLE}"
echo "ANNOTATIONS FILE  = ${ANNOTATIONS}"
echo "NETWORK FILE      = ${NETWORK}"

if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
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

python connect_cytoscape.py --save ${SAVE} --style ${STYLE} --annot ${ANNOTATIONS} --network ${NETWORK}
