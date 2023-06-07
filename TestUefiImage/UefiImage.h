/** @file
  Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
  SPDX-License-Identifier: BSD-2-Clause-Patent
**/

#ifndef UEFI_IMAGE_H
#define UEFI_IMAGE_H

VOID
FormatLoadConfig (
  IN     CONST UINT8  *Data,
  IN     UINTN        Size,
  IN OUT UINT32       *ConfigSize
  );

#endif // UEFI_IMAGE_H
