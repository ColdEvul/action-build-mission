#!/bin/sh

if [ "$#" -ne "3" ]; then
	echo "Usage: $0 missions_directory version_tag"
	exit 1
fi

MISSIONS_DIR=$GITHUB_WORKSPACE/$1
VERSION_TAG=$2
RELEASE_DIR=$GITHUB_WORKSPACE/$3

echo "gh workspace: $GITHUB_WORKSPACE"

if [ ! -d "$MISSIONS_DIR" ]; then
	echo "Missions directory not found"
	exit 2
fi

if [ -z "$VERSION_TAG" ]; then
	echo "No version tag set"
	exit 2
fi

if [ ! -d "$RELEASE_DIR" ]; then
	echo "Release directory not found"
	exit 2
fi

echo "Generating Missions"
python3 tools/make.py --version $VERSION_TAG --release $RELEASE_DIR