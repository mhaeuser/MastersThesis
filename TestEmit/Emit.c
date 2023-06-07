/** @file
  Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
  SPDX-License-Identifier: BSD-2-Clause-Patent
**/

#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include <Base.h>

#include <Library/DebugLib.h>
#include <Library/MemoryAllocationLib.h>
#include <Library/UefiImageLib.h>

#include <UserFile.h>
#include <UserMemory.h>

#include "../audk/BaseTools/ImageTool/ImageToolEmit.h"

typedef struct {
  uint8_t  BaseAddress[8];
  uint8_t  SymbolsPath[255];
  uint8_t  Flags;
  uint8_t  Memory[16];
  uint8_t  PeConfig[9];
} image_tool_fuzz_config_t;

STATIC_ASSERT (
  ALIGNOF (image_tool_fuzz_config_t) == 1,
  "image_tool_fuzz_config_t must be packed."
  );

STATIC_ASSERT (
  sizeof (image_tool_fuzz_config_t) == 289,
  "CorpusExtendConfig.py needs to be executed with the new delta."
  );

STATIC
VOID
ConfigurePe (
  IN     CONST UINT8  *Data,
  IN     UINTN        Size,
  IN OUT UINT32       *ConfigSize
  )
{
  UINT32  LastByte;

  *ConfigSize += sizeof (UINT8);
  LastByte     = Data[Size - *ConfigSize];

  PcdGetBool (PcdImageLoaderRtRelocAllowTargetMismatch) = (LastByte & 1U) != 0;
  PcdGetBool (PcdImageLoaderHashProhibitOverlap)        = (LastByte & 2U) != 0;
  PcdGetBool (PcdImageLoaderLoadHeader)                 = (LastByte & 4U) != 0;
  PcdGetBool (PcdImageLoaderDebugSupport)               = (LastByte & 8U) != 0;
  PcdGetBool (PcdImageLoaderAllowMisalignedOffset)      = 0; //(LastByte & 16U) != 0
  PcdGetBool (PcdImageLoaderRemoveXForWX)               = (LastByte & 32U) != 0;

  *ConfigSize += sizeof (UINT32);
  memmove (&LastByte, &Data[Size - *ConfigSize], sizeof (UINT32));

  PcdGet32 (PcdImageLoaderAlignmentPolicy) = LastByte;

  *ConfigSize += sizeof (UINT32);
  memmove (&LastByte, &Data[Size - *ConfigSize], sizeof (UINT32));

  PcdGet32 (PcdImageLoaderRelocTypePolicy) = LastByte;
}

int
LLVMFuzzerTestOneInput (
  const uint8_t  *Data,
  size_t         Size
  )
{
  void                            *OutputFile;
  uint32_t                        OutputFileSize;
  const image_tool_fuzz_config_t  *Config;
  uint32_t                        ConfigSize;
  //int8_t                          Format;
  int32_t                         Type;
  bool                            Relocate;
  uint64_t                        BaseAddress;
  char                            SymbolsPath[256];
  //bool                            Xip;
  bool                            Strip;
  bool                            FixedAddress;

  PcdGet8 (PcdDebugRaisePropertyMask) = 0;

  // LCOV_EXCL_START
  if (Size < sizeof (image_tool_fuzz_config_t)) {
    return -1;
  }
  // LCOV_EXCL_STOP

  Size  -= sizeof (image_tool_fuzz_config_t);
  Config = (const image_tool_fuzz_config_t *)(Data + Size);

  STATIC_ASSERT (
    UefiImageFormatMax == 2,
    "The code below needs to be updated to consider new formats."
    );

  memmove (&BaseAddress, Config->BaseAddress, sizeof (UINT64));
  //
  // UE images cannot be aligned at less than 4 KiB boundaries.
  //
  BaseAddress = ALIGN_VALUE (BaseAddress, BASE_4KB);

  memmove (SymbolsPath, Config->SymbolsPath, sizeof (SymbolsPath) - 1);
  SymbolsPath[sizeof (SymbolsPath) - 1] = 0;

  ConfigSize = 0;
  ConfigureMemoryAllocations (
    Config->Memory,
    sizeof (Config->Memory),
    &ConfigSize
    );

  ConfigSize = 0;
  ConfigurePe (Config->PeConfig, sizeof (Config->PeConfig), &ConfigSize);

  //
  // Test only UE due to time constraints.
  //
  //Format       = Config->Flags & 0x01U;
  Type         = ((Config->Flags & 0x0EU) >> 1U) + 10U;
  Relocate     = (Config->Flags & 0x10U) != 0;
  //
  // Do not test XIP, as the current UE implementation does not support it
  // anyway.
  //
  //Xip          = (Config->Flags & 0x10U) == 0;
  Strip        = (Config->Flags & 0x40U) == 0;
  FixedAddress = (Config->Flags & 0x80U) != 0;

  OutputFile = ToolImageEmit (
                 &OutputFileSize,
                 Data,
                 (uint32_t)Size,
                 UefiImageFormatUe,
                 Type,
                 Relocate,
                 BaseAddress,
                 SymbolsPath,
                 false, //Xip
                 Strip,
                 FixedAddress
                 );
  if (OutputFile != NULL) {
    free (OutputFile);
  }

#if 0
  printf("Total number of pool allocs: %d\n", GetNumPoolAllocations ());
#endif


  return 0;
}

int
ENTRY_POINT (
  int   argc,
  char  *argv[]
  )
{
  int       Status;
  void      *Image;
  uint32_t  ImageSize;

  // LCOV_EXCL_START
  if (argc < 2) {
    DEBUG ((DEBUG_ERROR, "Please provide a valid UEFI image path\n"));
    return -1;
  }

  PcdGet32 (PcdFixedDebugPrintErrorLevel) |= DEBUG_INFO;
  PcdGet32 (PcdDebugPrintErrorLevel)      |= DEBUG_INFO;

  if ((Image = UserReadFile (argv[1], &ImageSize)) == NULL) {
    DEBUG ((DEBUG_ERROR, "Read fail\n"));
    return 1;
  }

  Status = LLVMFuzzerTestOneInput (Image, ImageSize);

  FreePool (Image);

  return Status;
  // LCOV_EXCL_STOP
}
