#
# Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import sys
import os

if len(sys.argv) != 3 or not sys.argv[2].isnumeric:
  sys.exit(f"Usage: {sys.argv[0]} Corpus ExtensionSize")

corpus_path = sys.argv[1]
ext_size    = int(sys.argv[2])
append_arr  = bytearray([0xFF] * ext_size)

for name in os.listdir(corpus_path):
  file_path = os.path.join(corpus_path, name)
  if not os.path.isfile(file_path):
    continue

  with open(file_path, 'ab') as file:
    file.write(append_arr)
