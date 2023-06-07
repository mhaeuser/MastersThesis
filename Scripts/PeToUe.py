#
# Copyright (c) 2023, Marvin Häuser. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import os
import itertools
import glob
import pathlib
import subprocess
import sys
import math

def emit_image_file(dest_file, format, src_file):
  status = subprocess.call([
    os.path.join("audk", "BaseTools", "ImageTool", "ImageTool"),
    "GenImage",
    "-b", "0",
    "-c", format,
    "-o", dest_file,
    src_file
    ])
  if status != 0:
    sys.exit(f"Error converting {src_file} to {format} - {str(status)}")

def saving_average(saving, num):
  if num == 0:
    return 0

  return saving / num

if len(sys.argv) != 3:
  sys.exit(f"Usage: {sys.argv[0]} Source Destination")

artifacts_path = sys.argv[1]

conv_platforms     = ["Ovmf", "ArmVirtQemu"]
conv_architectures = {"Ovmf": ["IA32", "X64"], "ArmVirtQemu": ["ARM", "AARCH64"]}
conv_toolchains    = {"Ovmf": ["GCC5", "CLANGDWARF", "CLANGPDB"], "ArmVirtQemu": ["GCC5", "CLANGDWARF"]}
conv_targets       = ["RELEASE", "DEBUG", "NOOPT"]

comp_toolchains = {"Ovmf": ["GCC5", "CLANGDWARF"], "ArmVirtQemu": ["GCC5", "CLANGDWARF"]}

ue_path = os.path.join(sys.argv[2], "UE")
os.makedirs(ue_path, exist_ok=True)

pe_path = os.path.join(sys.argv[2], "PE")
os.makedirs(pe_path, exist_ok=True)

tex_path = os.path.join(sys.argv[2], "TeX")
os.makedirs(tex_path, exist_ok=True)

latex_main_rel = open(os.path.join(tex_path, "main_size_rel.tex"), "w")
latex_main_abs = open(os.path.join(tex_path, "main_size_abs.tex"), "w")
latex_main_tot = open(os.path.join(tex_path, "main_size_tot.tex"), "w")

latex_main_rel.write(
  "\\begin{table}\n" +
  "  \\centering\n" +
  "  \\begin{tabular}{l l l c c c}\n" +
  "    \\toprule\n" +
  "    \\multirow{2}{*}[-2pt]{\\textbf{Platform}} & \\multirow{2}{*}[-2pt]{\\textbf{Arch}} & \\multirow{2}{*}[-2pt]{\\textbf{Toolchain}} & \\multicolumn{3}{c}{\\textbf{Saving} [\%]}\\\\\n" +
  "    \\cmidrule{4-6}\n" +
  "     & & & \\textbf{Min.} & \\textbf{Avg.} & \\textbf{Max.}\\\\\n"
  )
latex_main_abs.write(
  "\\begin{table}\n" +
  "  \\centering\n" +
  "  \\begin{tabular}{l l l c c c}\n" +
  "    \\toprule\n" +
  "    \\multirow{2}{*}[-2pt]{\\textbf{Platform}} & \\multirow{2}{*}[-2pt]{\\textbf{Arch}} & \\multirow{2}{*}[-2pt]{\\textbf{Toolchain}} & \\multicolumn{3}{c}{\\textbf{Saving} [byte]}\\\\\n" +
  "    \\cmidrule{4-6}\n" +
  "     & & & \\textbf{Min.} & \\textbf{Avg.} & \\textbf{Max.}\\\\\n"
  )
latex_main_tot.write(
  "\\begin{table}\n" +
  "  \\centering\n" +
  "  \\begin{tabular}{l l l c c}\n" +
  "    \\toprule\n" +
  "    \\multirow{2}{*}[-2pt]{\\textbf{Platform}} & \\multirow{2}{*}[-2pt]{\\textbf{Arch}} & \\multirow{2}{*}[-2pt]{\\textbf{Toolchain}} & \\multicolumn{2}{c}{\\textbf{Saving}}\\\\\n"
  "    \\cmidrule{4-5}\n" +
  "     & & & [KiB] & [\%]\\\\\n"
  )

size_dict = {}

min_saving_rel = 0.0
avg_saving_rel = 0.0
max_saving_rel = 0.0

min_saving_abs = 0
avg_saving_abs = 0
max_saving_abs = 0

total_saving = 0
total_size   = 0

num_envs = 0

for platform in conv_platforms:
  num_platform_entries = len(conv_architectures[platform]) * len(comp_toolchains[platform])

  num_envs += num_platform_entries

  latex_main_rel.write(
    "    \midrule\n" +
    "    \\multirow{" + str(num_platform_entries) + "}{*}[-2pt]{" + platform + "}"
    )
  latex_main_abs.write(
    "    \midrule\n" +
    "    \\multirow{" + str(num_platform_entries) + "}{*}[-2pt]{" + platform + "}"
    )
  latex_main_tot.write(
    "    \midrule\n" +
    "    \\multirow{" + str(num_platform_entries) + "}{*}[-2pt]{" + platform + "}"
    )

  arch_prefix_rel_abs = ""
  arch_prefix_tot     = ""

  for arch in conv_architectures[platform]:
    latex_main_rel.write(
      arch_prefix_rel_abs + " & \\multirow{" + str(len(conv_architectures[platform])) + "}{*}{" + arch + "}"
      )
    latex_main_abs.write(
      arch_prefix_rel_abs + " & \\multirow{" + str(len(conv_architectures[platform])) + "}{*}{" + arch + "}"
      )
    latex_main_tot.write(
      arch_prefix_tot + " & \\multirow{" + str(len(conv_architectures[platform])) + "}{*}{" + arch + "}"
      )

    toolchain_prefix = ""

    for toolchain in conv_toolchains[platform]:
      entry_min_saving_rel   = float('inf')
      entry_max_saving_rel   = 0.0
      entry_total_saving_rel = 0.0

      entry_min_saving_abs   = math.inf
      entry_max_saving_abs   = 0
      entry_total_saving_abs = 0

      entry_total_size = 0

      entry_num_files = 0

      env = f"{platform} ({arch}, {toolchain})"
      size_dict[env] = {}
      for target in conv_targets:
        path         = os.path.join(artifacts_path, platform, f"{target}_{toolchain}", arch)
        image_files  = glob.glob(os.path.join(path, "*.efi"))
        img_cmp      = target == "RELEASE" and toolchain in comp_toolchains[platform]
        if img_cmp:
          entry_num_files = len(image_files)
        for src_file in image_files:
          base_name        = os.path.splitext(os.path.basename(src_file))[0]
          dest_file_suffix = os.path.join(f"{platform}_{arch}_{toolchain}_{target}_{base_name}")

          ue_dest_file = os.path.join(ue_path, dest_file_suffix + ".ue")
          pe_dest_file = os.path.join(pe_path, dest_file_suffix + ".pe")

          emit_image_file(ue_dest_file, "UE", src_file)
          emit_image_file(pe_dest_file, "PE", src_file)

          if img_cmp:
            ue_file_stats = os.stat(ue_dest_file)
            pe_file_stats = os.stat(pe_dest_file)

            saving_rel = 100 - saving_average(ue_file_stats.st_size * 100, pe_file_stats.st_size)

            entry_min_saving_rel    = min(entry_min_saving_rel, saving_rel)
            entry_max_saving_rel    = max(entry_max_saving_rel, saving_rel)
            entry_total_saving_rel += saving_rel

            saving_abs = pe_file_stats.st_size - ue_file_stats.st_size

            entry_min_saving_abs    = min(entry_min_saving_abs, saving_abs)
            entry_max_saving_abs    = max(entry_max_saving_abs, saving_abs)
            entry_total_saving_abs += saving_abs

            entry_total_size += pe_file_stats.st_size

            cmp_name = base_name
            if cmp_name == "CpuMpPei_EDADEB9D-DDBA-48BD-9D22-C1C169C8C5C6":
              cmp_name = "CpuMpPei"
            elif cmp_name == "CpuMpPei_280251c4-1d09-4035-9062-839acb5f18c1":
              cmp_name = "CpuMpPei (MpInitLibUp)"
            elif cmp_name == "CpuDxe_1A1E4886-9517-440e-9FDE-3BE44CEE2136":
              cmp_name = "CpuDxe"
            elif cmp_name == "CpuDxe_6490f1c5-ebcc-4665-8892-0075b9bb49b7":
              cmp_name = "CpuDxe (MpInitLibUp)"

            size_dict[env][cmp_name] = [pe_file_stats.st_size, ue_file_stats.st_size]

      if entry_num_files != 0:
        entry_avg_saving_rel = entry_total_saving_rel / entry_num_files
        latex_main_rel.write(
          toolchain_prefix + f" & {toolchain} & {entry_min_saving_rel:,.2f} & {entry_avg_saving_rel:,.2f} & {entry_max_saving_rel:,.2f}\\\\\n"
          )
        entry_avg_saving_abs = entry_total_saving_abs / entry_num_files
        latex_main_abs.write(
          toolchain_prefix + f" & {toolchain} & {entry_min_saving_abs:,} & {entry_avg_saving_abs:,.2f} & {entry_max_saving_abs:,}\\\\\n"
          )
        entry_total_savings_rel = saving_average(entry_total_saving_abs * 100, entry_total_size)
        latex_main_tot.write(
          toolchain_prefix + f" & {toolchain} & {(entry_total_saving_abs / 1024):,.2f} & {entry_total_savings_rel:,.2f}\\\\\n"
          )

        min_saving_rel += entry_min_saving_rel
        avg_saving_rel += entry_avg_saving_rel
        max_saving_rel += entry_max_saving_rel

        min_saving_abs += entry_min_saving_abs
        avg_saving_abs += entry_avg_saving_abs
        max_saving_abs += entry_max_saving_abs

        total_saving += entry_total_saving_abs

        total_size += entry_total_size

        size_dict[env] = dict(sorted(size_dict[env].items(), key=lambda item: saving_average(item[1][1], item[1][0])))

      toolchain_prefix = "     &"
    
    arch_prefix_rel_abs = "    \cmidrule{2-6}\n    "
    arch_prefix_tot     = "    \cmidrule{2-5}\n    "

if num_envs != 0:
  min_saving_rel = min_saving_rel / num_envs
  avg_saving_rel = avg_saving_rel / num_envs
  max_saving_rel = max_saving_rel / num_envs

  min_saving_abs = min_saving_abs / num_envs
  avg_saving_abs = avg_saving_abs / num_envs
  max_saving_abs = max_saving_abs / num_envs

  total_saving = total_saving / num_envs

  total_size = total_size / num_envs

latex_main_rel.write(
  "    \\midrule\n" +
  "    \\midrule\n" +
  "    \\textbf{Average} & & & " + f"{min_saving_rel:,.2f}" + " & " + f"{avg_saving_rel:,.2f}" + "&" + f"{max_saving_rel:,.2f}" + "\\\\\n" +
  "    \\bottomrule\n" +
  "  \end{tabular}\n" +
  "  \\caption{Platform Artifact Relative Space Saving Comparison}\n" +
  "\end{table}\n"
  )
latex_main_abs.write(
  "    \\midrule\n" +
  "    \\midrule\n" +
  "    \\textbf{Average} & & & " + f"{min_saving_abs:,}" + " & " + f"{avg_saving_abs:,.2f}" + "&" + f"{max_saving_abs:,}" + "\\\\\n" +
  "    \\bottomrule\n" +
  "  \end{tabular}\n" +
  "  \\caption{Platform Artifact Absolute Space Saving Comparison}\n" +
  "\end{table}\n"
  )
total_savings_rel = saving_average(total_saving * 100, total_size)
latex_main_tot.write(
  "    \\midrule\n" +
  "    \\midrule\n" +
  "    \\textbf{Average} & & & " + f"{(total_saving / 1024):,.2f} & {total_savings_rel:,.2f}" + "\\\\\n" +
  "    \\bottomrule\n" +
  "  \end{tabular}\n" +
  "  \\caption{Platform Space Saving Comparison}\n" +
  "\end{table}\n"
  )

latex_main_tot.close()
latex_main_abs.close()
latex_main_rel.close()

latex_appendix = open(os.path.join(tex_path, "appendix_size.tex"), "w")

table_prefix = ""
for env in size_dict:
  env_num_files = len(size_dict[env])
  if env_num_files == 0:
    continue

  latex_appendix.write(
    table_prefix +
    "\\begin{longtable}{l c c c}\n" +
    "  \\caption{" + f"{env}" + " Artifact Size Comparison}\\\\\\\\\n"
    "  \\toprule\n" +
    "  \\multirow{2}{*}[-2pt]{\\textbf{Module}} & \\multicolumn{2}{c}{\\textbf{Size} [KiB]} & \\multirow{2}{*}[-2pt]{\\textbf{Saving} [\\%]}\\\\\n" +
    "  \\cmidrule{2-3}\n" +
    "  & \\textbf{PE} & \\textbf{UE} &\\\\\n" +
    "  \\midrule\n"
    )

  env_total_pe_size = 0
  env_total_ue_size = 0
  env_total_saving  = 0

  for base_name in size_dict[env]:
    pe_size = size_dict[env][base_name][0]
    ue_size = size_dict[env][base_name][1]

    env_total_pe_size += pe_size
    env_total_ue_size += ue_size

    saving_rel = 100 - saving_average(ue_size * 100, pe_size)

    env_total_saving += saving_rel

    latex_appendix.write(
      f"  {base_name} & {(pe_size / 1024):,.2f} & {(ue_size / 1024):,.2f} & {saving_rel:,.2f}\\\\\n"
      )

  env_total_saving_rel = 100 - saving_average(env_total_ue_size * 100, env_total_pe_size)

  env_total_pe_size = env_total_pe_size / 1024
  env_total_ue_size = env_total_ue_size / 1024

  avg_pe_size      = env_total_pe_size / env_num_files
  avg_ue_size      = env_total_ue_size / env_num_files
  avg_saving_rel   = env_total_saving_rel / env_num_files
  env_total_saving = env_total_saving / env_num_files
  latex_appendix.write(
    "  \\midrule\n" +
    "  \\textbf{Average} & " + f"{avg_pe_size:,.2f} & {avg_ue_size:,.2f} & {env_total_saving:,.2f}" + "\\\\\n"
    "  \\textbf{Total} & " + f"{env_total_pe_size:,.2f} & {env_total_ue_size:,.2f} & {env_total_saving_rel:,.2f}" + "\\\\\n"
    "  \\bottomrule\n" +
    "\end{longtable}\n"
    )
  table_prefix = "\n"

latex_appendix.close()
