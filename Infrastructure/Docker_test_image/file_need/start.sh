#!/bin/bash
set -e

mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.287.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.287.1/actions-runner-linux-x64-2.287.1.tar.gz
echo "8fa64384d6fdb764797503cf9885e01273179079cf837bfc2b298b1a8fd01d52  actions-runner-linux-x64-2.287.1.tar.gz" | shasum -a 256 -c
tar xzf ./actions-runner-linux-x64-2.287.1.tar.gz
token=$(curl -s -XPOST \
  -H "authorization: token PERSONAL_ACCESS_TOKEN " \
    https://api.github.com/repos/mauricioobgo/runners-test/actions/runners/registration-token |\
    jq -r .token)
./config.sh --url https://github.com/mauricioobgo/runners-test --token  $token --name "my-runners-test" --work CI
./run.sh