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
    if [ "$arch" = "Ia32" ]; then
      WINPE_FILENAME=winpe_IA32.iso
    elif [ "$arch" = "X64" ] || [ "$arch" = "3264" ]; then
      WINPE_FILENAME=winpe_X64.iso
    elif [ "$arch" = "ARM" ]; then
      continue
    elif [ "$arch" = "AARCH64" ]; then
      WINPE_FILENAME=winpe_AARCH64.iso
    fi
    echo Checking "$PACKAGE""$arch" "$target"_"$TOOLCHAIN"
    python3 ocbuild/test_qemu_fw.py ./firmware_artifacts/"$PACKAGE"/"$arch"/"$target"_"$TOOLCHAIN"/FW.fd --test-winpe --test-winpe-path "$WINPE_FILENAME" --fw-arch "$arch"
  done
done
