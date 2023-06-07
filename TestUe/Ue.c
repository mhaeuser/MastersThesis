/** @file
  Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
  SPDX-License-Identifier: BSD-2-Clause-Patent
**/

#include <Base.h>

#include <Library/PcdLib.h>
#include <Library/UefiImageLib.h>

#include "../TestUefiImage/UefiImage.h"

VOID
FormatLoadConfig (
  IN     CONST UINT8  *Data,
  IN     UINTN        Size,
  IN OUT UINT32       *ConfigSize
  )
{
  PcdGet8 (PcdUefiImageFormatSupportNonFv) = 1U << UefiImageFormatUe;
  PcdGet8 (PcdUefiImageFormatSupportFv)    = 1U << UefiImageFormatUe;
}
