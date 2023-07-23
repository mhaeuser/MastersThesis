# Designing a Secure and Space-Efficient Executable File Format for the Unified Extensible Firmware Interface

<a href="https://scan.coverity.com/projects/mhaeuser-mastersthesis">
  <img alt="Coverity Scan Build Status"
       src="https://scan.coverity.com/projects/28584/badge.svg"/>
</a>

Material for the Master's Thesis 'Designing a Secure and Space-Efficient Executable File Format for the [Unified Extensible Firmware Interface](https://uefi.org)' (UEFI) at the [University of Kaiserslautern-Landau](https://rptu.de) (RPTU).

## Organization

To separate CI and artifact distribution for the different components and stages, this repository consists of multiple branches:

* [audk](https://github.com/mhaeuser/MastersThesis/tree/audk): The main contribution of the thesis. A fork of the [Acidanthera UEFI Development Kit](https://github.com/acidanthera/audk) (AUDK) that adds support for the UEFI Executable File Format (UE).
* [opencore](https://github.com/mhaeuser/MastersThesis/tree/opencore): A fork of the [OpenCore bootloader](https://github.com/acidanthera/OpenCorePkg) (OpenCore) that helps add support for the UEFI Executable File Format (UE) to the [AUDK](https://github.com/mhaeuser/MastersThesis/tree/audk) build system.
* [ocbuild](https://github.com/mhaeuser/MastersThesis/tree/ocbuild) A fork of [ocbuild](https://github.com/acidanthera/ocbuild) to ensure full reproducibility of the build system.
* [qemu_build](https://github.com/mhaeuser/MastersThesis/tree/qemu_build): A semi-reproducible container to build and distribute [QEMU 8.0.2](https://download.qemu.org/qemu-8.0.2.tar.xz) for performing UEFI boot tests.
* [ue_dev_build](https://github.com/mhaeuser/MastersThesis/tree/ue_dev_build): A semi-reproducible container image to build and test [AUDK](https://github.com/mhaeuser/MastersThesis/tree/audk) firmware artifacts.
* [audk_build](https://github.com/mhaeuser/MastersThesis/tree/audk_build): A reproducible environment to build, test, and distribute [AUDK](https://github.com/mhaeuser/MastersThesis/tree/audk) firmware artifacts.
* [ue_test](https://github.com/mhaeuser/MastersThesis/tree/audk_build): The testing environment for UE parsing and generation. This includes [PE](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format)-to-UE conversion tests, static analysis using [Coverity](https://scan.coverity.com), [Clang Static Analyzer](https://clang-analyzer.llvm.org), and [GitHub CodeQL](https://codeql.github.com), as well as fuzz-testing using [libFuzzer](https://llvm.org/docs/LibFuzzer.html).
* [audk_errata](https://github.com/mhaeuser/MastersThesis/tree/audk_errata): Changes to the [audk](https://github.com/mhaeuser/MastersThesis/tree/audk) branch that did not make it in time to meet the deadline.
* [thesis](https://github.com/mhaeuser/MastersThesis/tree/thesis): The LaTeX sources for the thesis document.

## Artifact Evaluation

For artifact evaluation and best-effort reproducibility, the [Releases](https://github.com/mhaeuser/MastersThesis/releases) contain the Docker container image, artifacts, and test results used for this work. Due to limitations with Ubuntu package archiving and dependency chain version-pinning, all container images in this repository are only 'semi-reproducible'.

## Publishing

This work has been published by the Embedded Systems Group at the University of Kaiserslautern-Landau.
[[PDF]](https://es.cs.rptu.de/publications/datarsg/Haeu23.pdf)
[[BibTeX]](https://es.cs.rptu.de/publications/entries/Haeu23.bib)