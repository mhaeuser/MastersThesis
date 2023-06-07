## @file
# Copyright (c) 2023, Marvin Häuser. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

OBJS += UefiImage.o
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
VPATH += $(UDK_PATH)/../TestUefiImage/:$\
			 	 $(UDK_PATH)/MdePkg/Library/BaseUefiImageLib:$\
				 $(UDK_PATH)/MdePkg/Library/BaseUefiImageExtraActionLibNull:$\
				 $(UDK_PATH)/MdePkg/Library/BaseUeImageLib:$\
				 $(UDK_PATH)/MdePkg/Library/BasePeCoffLib2
