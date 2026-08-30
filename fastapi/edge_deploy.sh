#! /bin/bash
username=$1
organization=$2
application=$3
version=$4
docker build -t docker.mobiledgex.net/$organization/images/$application:$version .
docker login -u $username docker.mobiledgex.net
docker push docker.mobiledgex.net/$organization/images/$application:$version
docker logout docker.mobiledgex.net
