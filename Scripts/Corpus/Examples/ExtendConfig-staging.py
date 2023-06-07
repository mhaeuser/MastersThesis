#
# Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import os
import sys

if 6 > len(sys.argv) or len(sys.argv) > 7:
  sys.exit(f"Usage: {sys.argv[0]} Corpus ConfigSig ConfigSize ExtendOffset ExtendSize [ExtendByte]")

if not sys.argv[3].isnumeric:
  sys.exit(f"ConfigSize {sys.argv[3]} must be an integer.")

corpus_path = sys.argv[1]
if not os.path.exists(corpus_path):
  sys.exit(f"Corpus {corpus_path} does not exist.")

config_sig  = sys.argv[2]
if len(config_sig) != 4:
  sys.exit(f"ConfigSig {config_sig} must be exactly four characters.")

try:
  config_size = int(sys.argv[3])
except:
  sys.exit(f"ConfigSig {sys.argv[3]} must be an integer.")
if config_size < 0:
  sys.exit(f"ConfigSize {config_size} must be non-negative.")

try:
  ext_off = int(sys.argv[4])
except:
  sys.exit(f"ExtendOffset {sys.argv[4]} must be an integer.")
if ext_off < 0:
  sys.exit(f"ExtendOffset {ext_off} must be non-negative.")
if ext_off > config_size:
  sys.exit(f"ExtendOffset {ext_off} must not exceed ConfigSize {config_size}.")

try:
  ext_size = int(sys.argv[5])
except:
  sys.exit(f"ExtendSize {sys.argv[5]} must be an integer.")
if ext_size == 0:
  sys.exit(f"ExtendSize {sys.argv[5]} must not be 0.")
if ext_size < 0 and ext_off + ext_size < 0:
  sys.exit(f"ExtendSize {sys.argv[5]} + ExtendOffset {ext_off} must be non-negative.")

byte = 0xFF
if len(sys.argv) > 6:
  try:
    byte = int(sys.argv[6], 0)
  except:
    sys.exit(f"ExtendByte {sys.argv[6]} must be an integer.")
  if 0 > byte or byte > 0xFF:
    sys.exit(f"ExtendByte {sys.argv[6]} must be a byte.")

append_arr = bytearray([byte] * ext_size)

for name in os.listdir(corpus_path):
  file_path = os.path.join(corpus_path, name)
  if not os.path.isfile(file_path):
    continue

  with open(file_path, 'r+b') as file:
    # Retrieve the file size.
    file.seek(0, os.SEEK_END)
    size = file.tell()
    # If no config data is in the file yet, append the signature.
    full_sig   = bytearray("FUZZ" + config_sig, 'utf-8')
    config_off = size - config_size
    if config_size == 0 and ext_size > 0:
      file.write(full_sig)
      config_off = size + 8
    # Verify the operation can be applied to the file.
    elif config_off < 8:
      sys.exit(f"{file_path}: ConfigSize {config_size} + 8 may not exceed the file size {size}.")
    # Verify the signature is correct.
    else:
      file.seek(config_off - 8)
      sig = file.read(8)
      if sig != full_sig:
        sys.exit(f"{file_path}: Signature {full_sig} does not match {sig}.")
    # Move the data past the (positive or negative) extension.
    config_ext = config_off + ext_off
    file.seek(config_ext)
    data = file.read()
    file.seek(config_ext + ext_size)
    file.write(data)
    # (Positively or negatively) Extend the data.
    file.seek(config_ext)
    file.write(append_arr)
    # If ext_size is negative, this will truncate the leftover trailer.
    if ext_size < 0:
      file.truncate(size + ext_size)
