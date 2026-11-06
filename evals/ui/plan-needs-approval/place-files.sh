#!/usr/bin/env bash
# Copies the shared Ledgerly fixture into the run's working directory.
set -eu
cp -R "$(dirname "$0")/../fixture/." .
