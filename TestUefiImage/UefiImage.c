/** @file
  Copyright (c) 2018, vit9696. All rights reserved.
  Copyright (c) 2023, Marvin Häuser. All rights reserved.
  SPDX-License-Identifier: BSD-3-Clause
**/

#include <Uefi.h>

#include <Library/BaseMemoryLib.h>
#include <Library/BaseOverflowLib.h>
#include <Library/MemoryAllocationLib.h>
#include <Library/UefiImageLib.h>
#include <Library/DebugLib.h>
#include <Library/UefiBootServicesTableLib.h>

#include <stdio.h>
#include <string.h>

#include <UserFile.h>
#include <UserMemory.h>

#include "UefiImage.h"

typedef struct {
  uint8_t  BootAddress[8];
  uint8_t  RtAddress[8];
  uint8_t  Memory[16];
  uint8_t  HashesMask[8];
} uefi_image_fuzz_config_t;

STATIC_ASSERT (
  ALIGNOF (uefi_image_fuzz_config_t) == 1,
  "uefi_image_fuzz_config_t must be packed."
  );

STATIC_ASSERT (
  sizeof (uefi_image_fuzz_config_t) == 40,
  "CorpusExtendConfig.py needs to be executed with the new delta."
  );

STATIC UINT64  mHashesMask     = MAX_UINT64;
STATIC UINTN   mHashIndex      = 0;
STATIC UINTN   mHashDependency = 0;

STATIC
BOOLEAN
HashUpdate (
  IN OUT  VOID        *HashContext,
  IN      CONST VOID  *Data,
  IN      UINTN       DataLength
  )
{
  CONST UINT8  *D;
  BOOLEAN      P;

  (VOID)HashContext;

  D = (CONST UINT8 *)Data;

  for (UINTN i = 0; i < DataLength; i++) {
    mHashDependency += D[i];
  }

  P = (mHashesMask & (1ULL << mHashIndex)) != 0;

  ++mHashIndex;
  mHashIndex &= 63U;

  return P;
}

STATIC
RETURN_STATUS
UefiImageTestLoad (
  IN OUT  UEFI_IMAGE_LOADER_IMAGE_CONTEXT  *Context,
  OUT     VOID                             *Destination,
  IN      UINT32                           DestinationSize,
  IN      UINT64                           BootAddress,
  IN      UINT64                           RtAddress
  )
{
  RETURN_STATUS  Status;
  CONST CHAR8    *SymbolsPath;
  UINT32         SymbolsPathSize;
  VOID           *RtCtx;
  UINT32         RtCtxSize;

  Status = UefiImageLoadImage (Context, Destination, DestinationSize);
  // LCOV_EXCL_START
  if (RETURN_ERROR (Status)) {
    return Status;
  }
  // LCOV_EXCL_STOP

  Status = UefiImageGetSymbolsPath (
             Context,
             &SymbolsPath,
             &SymbolsPathSize
             );
  if (!RETURN_ERROR (Status)) {
    ASSERT (SymbolsPath[SymbolsPathSize - 1] == 0);
  }

  if (!UefiImageGetRelocsStripped (Context)) {
    RtCtx     = NULL;
    RtCtxSize = 0;
    if (UefiImageGetSubsystem (Context) == EFI_IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER) {
      Status = UefiImageLoaderGetRuntimeContextSize (Context, &RtCtxSize);
      // LCOV_EXCL_START
      if (RETURN_ERROR (Status)) {
        return Status;
      }
      // LCOV_EXCL_STOP

      RtCtx = AllocatePool (RtCtxSize);
      if (RtCtx == NULL) {
        return RETURN_OUT_OF_RESOURCES;
      }
    }

    Status = UefiImageRelocateImage (Context, BootAddress, RtCtx, RtCtxSize);

    if (UefiImageGetSubsystem (Context) == EFI_IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER) {
      if (!RETURN_ERROR (Status)) {
        Status = UefiImageRuntimeRelocateImage (
                   (VOID *)UefiImageLoaderGetImageAddress (Context),
                   UefiImageGetImageSize (Context),
                   RtAddress,
                   RtCtx
                   );
      }

      FreePool (RtCtx);
    }

    if (RETURN_ERROR (Status)) {
      return Status;
    }
  }

  UefiImageDiscardSegments (Context);

  return RETURN_SUCCESS;
}

STATIC
RETURN_STATUS
UefiImageTestLoadFull (
  IN CONST VOID  *FileBuffer,
  IN UINT32      FileSize,
  IN UINT64      BootAddress,
  IN UINT64      RtAddress
  )
{
  RETURN_STATUS                    Status;
  BOOLEAN                          Result;
  UEFI_IMAGE_LOADER_IMAGE_CONTEXT  Context;
  VOID                             *Destination;
  UINT32                           ImageSize;
  UINT32                           DestinationSize;
  UINT32                           DestinationPages;
  UINT32                           DestinationAlignment;
  UINT8                            HashContext;
  CHAR8                            ModuleName[32];
  UEFI_IMAGE_RECORD                *ImageRecord;
  volatile UINT64                  ReadValue;

  Status = UefiImageInitializeContext (
             &Context,
             FileBuffer,
             FileSize,
             UEFI_IMAGE_SOURCE_FV
             );
  if (RETURN_ERROR (Status)) {
    return Status;
  }

  Result = UefiImageHashImageDefault (
             &Context,
             &HashContext,
             HashUpdate
             );
  if (!Result) {
    return RETURN_UNSUPPORTED;
  }

  ImageSize            = UefiImageGetImageSize (&Context);
  // LCOV_EXCL_START
  DestinationPages     = EFI_SIZE_TO_PAGES (ImageSize);
  // LCOV_EXCL_STOP
  DestinationSize      = EFI_PAGES_TO_SIZE (DestinationPages);
  DestinationAlignment = UefiImageGetSegmentAlignment (&Context);

  if (DestinationSize >= BASE_16MB) {
    return RETURN_UNSUPPORTED;
  }

  Destination = AllocateAlignedCodePages (
                  DestinationPages,
                  DestinationAlignment
                  );
  if (Destination == NULL) {
    return RETURN_OUT_OF_RESOURCES;
  }

  BootAddress = ALIGN_VALUE (BootAddress, DestinationAlignment);
  RtAddress   = ALIGN_VALUE (BootAddress, DestinationAlignment);

  Status = UefiImageTestLoad (
             &Context,
             Destination,
             DestinationSize,
             BootAddress,
             RtAddress
             );

  UefiImageDebugPrintSegments (&Context);

  ImageRecord = UefiImageLoaderGetImageRecord (&Context);
  if (ImageRecord != NULL) {
    UefiImageDebugPrintImageRecord (ImageRecord);
    FreePool (ImageRecord);
  }

  UINT64  FixedAddress;

  ReadValue  = UefiImageGetFormat (&Context);
  ReadValue += UefiImageGetMachine (&Context);

  UefiImageGetFixedAddress (&Context, &FixedAddress);
  ReadValue += FixedAddress;

  ReadValue += UefiImageGetBaseAddress (&Context);
  ReadValue += UefiImageLoaderGetImageEntryPoint (&Context);
  ReadValue += UefiImageLoaderGetDebugAddress (&Context);

  Status = UefiImageGetModuleNameFromSymbolsPath (
             &Context,
             ModuleName,
             sizeof (ModuleName)
             );
  if (!RETURN_ERROR (Status)) {
    ReadValue += AsciiStrLen (ModuleName);
  }

  FreeAlignedPages (Destination, DestinationPages);

  return Status;
}

int
LLVMFuzzerTestOneInput (
  const uint8_t  *Data,
  UINTN          Size
  )
{
  const uefi_image_fuzz_config_t  *Config;
  uint32_t                        ConfigSize;
  uint64_t                        BootAddress;
  uint64_t                        RtAddress;

  PcdGet8 (PcdDebugRaisePropertyMask) = 0;

  // LCOV_EXCL_START
  if (Size < sizeof (uefi_image_fuzz_config_t)) {
    return -1;
  }
  // LCOV_EXCL_STOP

  Size  -= sizeof (uefi_image_fuzz_config_t);
  Config = (const uefi_image_fuzz_config_t *)(Data + Size);

  memmove (&BootAddress, Config->BootAddress, sizeof (BootAddress));
  memmove (&RtAddress, Config->RtAddress, sizeof (RtAddress));

  ConfigSize = 0;
  FormatLoadConfig (NULL, 0, &ConfigSize);

  ConfigSize = 0;
  ConfigureMemoryAllocations (
    Config->Memory,
    sizeof (Config->Memory),
    &ConfigSize
    );

  memmove (&mHashesMask, Config->HashesMask, sizeof (mHashesMask));

  UefiImageTestLoadFull (Data, Size, BootAddress, RtAddress);

  return 0;
}

int
ENTRY_POINT (
  int   argc,
  char  *argv[]
  )
{
  UINT8   *Image;
  UINT32  ImageSize;
  int     Result;

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

  Result = LLVMFuzzerTestOneInput (Image, ImageSize);

  FreePool (Image);

  return Result;
  // LCOV_EXCL_STOP
}
