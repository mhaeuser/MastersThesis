#
# Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import sys
import os

if len(sys.argv) != 2:
  sys.exit(f"Usage: {sys.argv[0]} Corpus")

corpus_path = sys.argv[1]

for name in os.listdir(corpus_path):
  file_path = os.path.join(corpus_path, name)
  if not os.path.isfile(file_path):
    continue

  if name.startswith("Ovmf_") or name.startswith("ArmVirtQemu_") or name.startswith("FABRICATED_") or name.startswith("edk2-stable202305-4K_"):
    continue

  with open(file_path, 'r+b') as file:
    file.seek(0, os.SEEK_END)
    size = file.tell()

    file.seek(size - 26)
    flags = file.read(1)[0]

    subs  = (flags & 0x0C) >> 2
    flags = flags & 0xF1
    flags = flags | (subs << 1)

    file.seek(size - 26)
    file.write(bytes([flags]))
