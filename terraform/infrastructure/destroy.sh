#!/usr/bin/env bash

set -e

if [[ -z "$1" ]]
  then
    echo "No region supplied, execute as: ./destroy.sh REGION WORKSPACE"
    exit 1
fi

if [[ -z "$2" ]]
  then
    echo "No workspace supplied, execute as: ./destroy.sh REGION WORKSPACE"
    exit 1
fi

REGION=$1
WORKSPACE=$2

terraform workspace select ${WORKSPACE}
terraform destroy -auto-approve -input=false -var region="$REGION"
