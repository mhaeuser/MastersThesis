#!/bin/bash

#
# Copyright (c) 2023 Marvin Häuser. All rights reserved.
#

./codeql/codeql github upload-results \
    --repository=${GITHUB_REPOSITORY} \
    --ref=${GITHUB_REF} --commit=${GITHUB_SHA} \
    --sarif=./codeql-sarifs/ImageTool-latest.sarif
