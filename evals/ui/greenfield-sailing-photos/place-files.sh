#!/usr/bin/env bash
# Copies the sailing school's photos (with their credits) into the run's working directory.
set -eu
mkdir -p images
cp "$(dirname "$0")/../photos/"* images/
