#!/bin/bash

#
# Copyright (c) 2018 - 2022 vit9696, PMheart. All rights reserved.
# Copyright (c) 2023 Marvin Häuser. All rights reserved.
#

abort() {
  echo "ERROR: $1!"
  exit 1
}

if [ "${GITHUB_REPOSITORY}" = "" ]; then
  abort "No GITHUB_REPOSITORY provided"
fi

if [ "${COVERITY_SCAN_TOKEN}" = "" ]; then
  abort "No COVERITY_SCAN_TOKEN provided"
fi

if [ "${COVERITY_SCAN_EMAIL}" = "" ]; then
  abort "No COVERITY_SCAN_EMAIL provided"
fi

if [ "${COVERITY_RESULTS_DIR}" = "" ]; then
  abort "No COVERITY_RESULTS_DIR provided"
fi

if [ "${COVERITY_RESULTS_FILE}" = "" ]; then
  abort "No COVERITY_RESULTS_FILE provided"
fi

ret=0

# Upload results
tar czf "${COVERITY_RESULTS_FILE}" -C "${COVERITY_RESULTS_DIR}/.." "$(basename "${COVERITY_RESULTS_DIR}")" || ret=$?
if [ $ret -ne 0 ]; then
  abort "Failed to compress Coverity results dir ${COVERITY_RESULTS_DIR} with code ${ret}"
fi

upload () {
  curl \
    --form project="${GITHUB_REPOSITORY}" \
    --form token="${COVERITY_SCAN_TOKEN}" \
    --form email="${COVERITY_SCAN_EMAIL}" \
    --form file="@${COVERITY_RESULTS_FILE}" \
    --form version="${GITHUB_SHA}" \
    --form description="GitHub Actions build" \
    "https://scan.coverity.com/builds?project=${GITHUB_REPOSITORY}"
  return $?
}

for i in {1..3}
do
  echo "Uploading results... (Trial $i/3)"
  upload && exit 0 || ret=$?
done
abort "Failed to upload Coverity results ${COVERITY_RESULTS_FILE} with code ${ret}"
