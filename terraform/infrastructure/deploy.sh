#!/usr/bin/env bash

set -e

if [[ -z "$1" ]]
  then
    echo "No region supplied, execute as: ./deploy.sh REGION WORKSPACE BUCKET"
    exit 1
fi

if [[ -z "$2" ]]
  then
    echo "No workspace supplied, execute as: ./deploy.sh REGION WORKSPACE BUCKET"
    exit 1
fi

if [[ -z "$3" ]]
  then
    echo "No terraform bucket supplied, execute as: ./deploy.sh REGION WORKSPACE BUCKET"
    exit 1
fi

REGION=$1
WORKSPACE=$2
BUCKET=$3

terraform init -get=true -input=false -backend-config="bucket=${BUCKET}"
terraform workspace new ${WORKSPACE} || terraform workspace select ${WORKSPACE}
terraform apply -auto-approve -input=false -var region=${REGION}
terraform output -json | jq 'with_entries(.value |= .value)' > output.json
