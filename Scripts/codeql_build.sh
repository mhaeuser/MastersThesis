#!/bin/bash

#
# Copyright (c) 2023 Marvin Häuser. All rights reserved.
#

mkdir ./codeql-dbs/
mkdir ./codeql-sarifs/

./codeql/codeql database create ./codeql-dbs/ImageTool \
  --command "${ANALYSIS_BUILD_COMMAND}" --language=cpp --source-root ./audk/ \
  --codescanning-config ./.github/codeql/codeql-config.yml

./codeql/codeql database analyze ./codeql-dbs/ImageTool --format=sarif-latest \
  --output=./codeql-sarifs/ImageTool-latest.sarif --threads 0
