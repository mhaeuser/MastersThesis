#
# Copyright (c) 2023 Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

FROM --platform=linux/amd64 ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

SHELL [ "/bin/bash", "-c" ]

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget && \
    wget https://download.qemu.org/qemu-8.0.2.tar.xz && \
    apt-get purge --auto-remove -y wget && \
    apt-get install -y build-essential \
        libglib2.0-dev \
        libfdt-dev \
        libpixman-1-dev \
        zlib1g-dev \
        ninja-build \
        flex \
        bison && \
    rm -rf /var/lib/apt/lists/* && \
    tar -xJf qemu-8.0.2.tar.xz && \
    rm -f qemu-8.0.2.tar.xz && \
    cd qemu-8.0.2/ && \
    ./configure --prefix=/opt/qemu-8.0.2/ --target-list=aarch64-softmmu,arm-softmmu,x86_64-softmmu --static --disable-gio --disable-tools --disable-docs && \
    make -j && \
    make install && \
    cd .. && \
    rm -rf qemu-8.0.2/ && \
    tar -C /opt/ -cJf qemu-8.0.2-bin.tar.xz qemu-8.0.2/ && \
    rm -rf /opt/qemu-8.0.2/
