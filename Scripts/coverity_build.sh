#!/bin/bash

#
# Copyright (c) 2018 - 2022 vit9696, PMheart. All rights reserved.
# Copyright (c) 2023 Marvin Häuser. All rights reserved.
#

abort() {
  echo "ERROR: $1!"
  exit 1
}

if [ "${COVERITY_RESULTS_DIR}" = "" ]; then
  abort "No COVERITY_RESULTS_DIR provided"
fi

if [ "${ANALYSIS_BUILD_COMMAND}" = "" ]; then
  abort "No ANALYSIS_BUILD_COMMAND provided"
fi

ret=0

# Run Coverity
# shellcheck disable=SC2086
PATH=cov-analysis-linux64/bin/:$PATH cov-build --dir "${COVERITY_RESULTS_DIR}" ${ANALYSIS_BUILD_COMMAND} || ret=$?
if [ $ret -ne 0 ]; then
  abort "Coverity build tool failed with code ${ret}"
fi
