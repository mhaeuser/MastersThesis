## @file
# Copyright (c) 2023, Marvin Häuser. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

PROJECT = Emit
PRODUCT = $(PROJECT)$(INFIX)$(SUFFIX)

OBJS  = $(PROJECT).o
OBJS += ImageToolEmit.o \
  Image.o \
  ElfScan32.o \
  ElfScan64.o \
  ElfScanCommon.o \
  UefiImageScan.o \
  UeScan.o \
  UeEmit.o \
  PeScan.o \
  PeEmit32.o \
  PeEmit64.o \
  PeEmitCommon.o \
  BinEmit.o \
  DynamicBuffer.o
OBJS += CommonSupport.o \
	UeSupport.o \
	PeSupport.o \
	UefiImageLib.o
OBJS += UefiImageExtraActionLib.o
OBJS += UeImageLib.o
OBJS += PeCoffDebug.o \
	PeCoffHash.o \
	PeCoffHii.o \
	PeCoffInfo.o \
	PeCoffInit.o \
	PeCoffLoad.o \
	PeCoffRelocate.o

WERROR   = 1
DEBUG    = 1
UDK_PATH = ../audk
OC_USER  = $(UDK_PATH)/OpenCorePkg

VPATH = $(UDK_PATH)/BaseTools/ImageTool:$\
				$(UDK_PATH)/MdePkg/Library/BaseUefiImageLib:$\
				$(UDK_PATH)/MdePkg/Library/BaseUefiImageExtraActionLibNull:$\
				$(UDK_PATH)/MdePkg/Library/BaseUeImageLib:$\
				$(UDK_PATH)/MdePkg/Library/BasePeCoffLib2

LCOV_PREFIX = $(shell dirname $(CURDIR))/audk
LCOV_EXCL = \
  $(LCOV_PREFIX)/BaseTools/ImageTool/BinEmit.c \
  $(LCOV_PREFIX)/BaseTools/ImageTool/Elf\*.c \
	$(LCOV_PREFIX)/BaseTools/ImageTool/PeEmit\*.c \
	$(LCOV_PREFIX)/MdeModulePkg/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BaseDebugPrintErrorLevelLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BaseLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BaseOverflowLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BasePciExpressLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BasePciLibPciExpress/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BasePeCoffLib2/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BasePrintLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BaseSafeIntLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BaseUefiImageExtraActionLibNull/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BaseUefiImageLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/BaseUeImageLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/UefiDebugLibConOut/\* \
	$(LCOV_PREFIX)/MdePkg/Library/UefiDevicePathLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/UefiLib/\* \
  $(LCOV_PREFIX)/OpenCorePkg/\* \
	$(LCOV_PREFIX)/UefiCpuPkg/\*

coverage-ex: $(PRODUCT) FORCE
	$(LCOV) --no-checksum -r COVERAGE/trace.lcov_tmp /usr/include/\* $(LCOV_EXCL) --rc lcov_branch_coverage=1  --rc lcov_excl_br_line='LCOV_EXCL_BR_LINE|ASSERT|DEBUG' --output-file COVERAGE/trace.lcov_info_final || exit 1
	$(GENHTML) --branch-coverage --output-directory COVERAGE COVERAGE/trace.lcov_info_final

include $(OC_USER)/User/Makefile

#
# Disable ELF as the code has not been subject to proper review yet.
# Limit the ImageTool dynamic buffer growth value to 4 bytes to increase the
# allocation failure coverage.
#
CFLAGS += -DUEFI_IMAGE_FORMAT_SUPPORT_SOURCES=0x02 -DIMAGE_TOOL_DISABLE_ELF -DIMAGE_TOOL_DYNAMIC_BUFFER_GROWTH=0x04
