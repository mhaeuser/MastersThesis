#
# Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import sys
import os

output_dir = "FABRICATED"
os.makedirs(output_dir, exist_ok=True)

source_name = os.path.join("TestEmit", "FUZZDICT", "Ovmf_IA32_CLANGDWARF_DEBUG_DisplayEngine.pe")
with open(source_name, 'r+b') as source_file:
  source_data   = source_file.read()
  alloc_mod_off = len(source_data) - 17
  for i in range(1, 2675):
    with open(os.path.join(output_dir, f"FABRICATED_DisplayEngine-{i}.pe"), 'wb') as fabr_file:
      fabr_file.write(source_data)
      fabr_file.seek(alloc_mod_off)
      fabr_file.write(i.to_bytes(4, byteorder='little'))
