## @file
# Copyright (c) 2023, Marvin Häuser. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

PROJECT = Ue
PRODUCT = $(PROJECT)$(INFIX)$(SUFFIX)
OBJS    = $(PROJECT).o

WERROR   = 1
DEBUG    = 1
UDK_PATH = ../audk
OC_USER  = $(UDK_PATH)/OpenCorePkg

LCOV_PREFIX = $(shell dirname $(CURDIR))/audk
LCOV_EXCL = \
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
	$(LCOV_PREFIX)/MdePkg/Library/BaseUefiImageLib/PeSupport.c \
	$(LCOV_PREFIX)/MdePkg/Library/BaseUefiImageLib/UefiImageLib.c \
	$(LCOV_PREFIX)/MdePkg/Library/UefiDebugLibConOut/\* \
	$(LCOV_PREFIX)/MdePkg/Library/UefiDevicePathLib/\* \
	$(LCOV_PREFIX)/MdePkg/Library/UefiLib/\* \
  $(LCOV_PREFIX)/OpenCorePkg/\* \
	$(LCOV_PREFIX)/UefiCpuPkg/\*

include ../TestUefiImage/Makefile
include $(OC_USER)/User/Makefile

CFLAGS += -DUEFI_IMAGE_FORMAT_SUPPORT_SOURCES=0x02
