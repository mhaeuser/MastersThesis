#
# Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import os
import subprocess
import sys

if len(sys.argv) != 2:
  sys.exit(f"Usage: {sys.argv[0]} Corpus")

corpus_path = sys.argv[1]

for name in os.listdir(corpus_path):
  if not ((name.startswith("Ovmf_") or name.startswith("ArmVirtQemu_")) and name.endswith(".pe")):
    continue

  stdout = str(subprocess.check_output([os.path.join("TestEmit", "Emit"), os.path.join(corpus_path, name)]))
  index  = str(stdout).find("Total number of pool allocs: ")
  num_allocs = 0
  if index != -1:
    index += len("Total number of pool allocs: ")
    end_index = index
    while stdout[end_index].isdigit():
      end_index += 1
    num_allocs = int(str(stdout)[index:end_index])
  print(name, num_allocs)
