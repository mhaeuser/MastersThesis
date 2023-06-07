#!/bin/bash

#
# Copyright (c) 2023 Savva Mitrofanov. All rights reserved.<BR>
# Copyright (c) 2023 Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

IFS=', ' read -r -a TARGETS <<< "$TARGETS"
IFS=', ' read -r -a ARCHS <<< "$ARCHS"
for target in "${TARGETS[@]}"; do
  for arch in "${ARCHS[@]}"; do
    echo Checking "$PACKAGE""$arch" "$target"_"$TOOLCHAIN"
    python3 ocbuild/test_qemu_fw.py ./firmware_artifacts/"$PACKAGE"/"$arch"/"$target"_"$TOOLCHAIN"/FW.fd --test-linux --fw-arch "$arch"
  done
done
