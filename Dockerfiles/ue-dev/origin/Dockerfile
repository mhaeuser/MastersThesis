#
# Copyright (c) 2023 Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

FROM --platform=linux/amd64 ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

SHELL [ "/bin/bash", "-c" ]

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        wget \
        software-properties-common \
        gnupg \
        xz-utils && \
    wget -O qemu-8.0.2-bin.tar.xz https://github.com/mhaeuser/MastersThesis/releases/download/qemu-release/qemu-8.0.2-bin.tar.xz && \
    wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc && \
    add-apt-repository 'deb http://apt.llvm.org/jammy/ llvm-toolchain-jammy-16 main' && \
    add-apt-repository 'deb-src http://apt.llvm.org/jammy/ llvm-toolchain-jammy-16 main' && \
    apt-get update && \
    tar -C /opt/ -xJf qemu-8.0.2-bin.tar.xz && \
    apt-get purge --auto-remove -y wget software-properties-common gnupg xz-utils && \
    rm -f qemu-8.0.2-bin.tar.xz \
    apt-get install -y \
        build-essential \
        gcc-arm-linux-gnueabi \
        gcc-aarch64-linux-gnu \
        gcc-11-multilib \
        clang-16 \
        clang-tools-16 \
        lld-16 \
        libssl-dev \
        libx11-dev \
        libxext-dev \
        uuid-dev \
        lcov \
        nasm \
        acpica-tools \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install \
        requests \
        PyYAML \
        GitPython \
        pexpect \
        argparse \
        prospector

ENV PATH="$PATH:/usr/lib/llvm-16/bin/:/opt/qemu-8.0.2/bin/"
ENV GCC5_ARM_PREFIX="arm-linux-gnueabi-"
ENV GCC5_AARCH64_PREFIX="aarch64-linux-gnu-"
