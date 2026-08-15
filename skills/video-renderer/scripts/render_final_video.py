#!/usr/bin/env python3
"""
Video Renderer - Pure Fast Video Concatenator
Concatenates per-unit MP4 video slices (which already embed audio and HTML subtitles)
into multi-aspect final videos (e.g. video_16x9.mp4, video_9x16.mp4).
"""

import os
import sys
import glob
import subprocess
import argparse
import re
import shutil


def find_first_existing(project_dir, candidates):
    """Finds the first existing file among candidate paths relative to project_dir."""
    for cand in candidates:
        full = os.path.join(project_dir, cand)
        if os.path.exists(full):
            return full
    return None


def concat_video_files(project_dir, input_files, output_filename, root_output_filename=None, bgm_path=None):
    """Losslessly concatenates input MP4 files using FFmpeg copy mode."""
    if not input_files:
        return None

    concat_txt = os.path.join(project_dir, f"concat_{output_filename}.txt")
    out_path = os.path.join(project_dir, output_filename)

    try:
        with open(concat_txt, 'w', encoding='utf-8') as f:
            for uf in input_files:
                f.write(f"file '{os.path.abspath(uf)}'\n")

        if bgm_path and os.path.exists(bgm_path):
            temp_concat = os.path.join(project_dir, f"temp_{output_filename}")
            concat_cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', concat_txt, '-c', 'copy', temp_concat
            ]
            subprocess.run(concat_cmd, cwd=project_dir, check=True)

            filter_complex = "[0:a]volume=1.0[v_a];[1:a]volume=0.3[bgm_low];[v_a][bgm_low]amix=inputs=2:duration=first[aout]"
            mux_cmd = [
                'ffmpeg', '-y', '-i', temp_concat, '-i', bgm_path,
                '-filter_complex', filter_complex,
                '-map', '0:v', '-map', '[aout]',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
                '-shortest', out_path
            ]
            subprocess.run(mux_cmd, cwd=project_dir, check=True)
            if os.path.exists(temp_concat):
                os.remove(temp_concat)
        else:
            concat_cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', concat_txt, '-c', 'copy', out_path
            ]
            subprocess.run(concat_cmd, cwd=project_dir, check=True)

        print(f"[Success] Concatenated final video: {out_path}")

        # Copy to root directory if project_dir is inside assets/video
        if root_output_filename and 'assets/video' in project_dir:
            root_v = os.path.abspath(os.path.join(project_dir, f'../../{root_output_filename}'))
            try:
                shutil.copyfile(out_path, root_v)
                print(f"[Success] Copied final video to root: {root_v}")
            except Exception as e:
                print(f"[Notice] Failed to copy to root: {e}")

        return out_path
    finally:
        if os.path.exists(concat_txt):
            try:
                os.remove(concat_txt)
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(description="Pure video slice concatenator for HyperFrames units")
    parser.add_argument('--project-dir', required=True, help="Path to the project assets/video directory")
    parser.add_argument('--fast-concat', action='store_true', help="Accepted for backward compatibility")
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    bgm_path = find_first_existing(project_dir, ['bgm.mp3', 'audio/bgm.mp3', 'bgm.wav', 'audio/bgm.wav'])

    processed_any = False

    # 1. Multi-Aspect Mode (e.g. unit_01_16x9.mp4, unit_01_9x16.mp4)
    aspect_files_map = {}
    all_aspect_files = glob.glob(os.path.join(project_dir, 'unit_*', 'unit_*_*x*.mp4'))
    for f in all_aspect_files:
        filename = os.path.basename(f)
        match = re.search(r'unit_\d+_(\d+x\d+)\.mp4$', filename)
        if match:
            aspect = match.group(1)
            aspect_files_map.setdefault(aspect, []).append(f)

    if aspect_files_map:
        print(f"[Video Renderer] Multi-Aspect Mode: Found {len(aspect_files_map)} aspect groups: {list(aspect_files_map.keys())}")
        for aspect, a_files in aspect_files_map.items():
            a_files = sorted(a_files)
            print(f"[Video Renderer] Processing aspect group '{aspect}' ({len(a_files)} files)...")
            concat_video_files(
                project_dir,
                a_files,
                output_filename=f"final_video_{aspect}.mp4",
                root_output_filename=f"video_{aspect}.mp4",
                bgm_path=bgm_path
            )
            processed_any = True

    # 2. Standard Single-Aspect Mode (e.g. unit_01/unit_01.mp4 or unit_01.mp4)
    unit_files = sorted(glob.glob(os.path.join(project_dir, 'unit_*', 'unit_*.mp4')))
    unit_files = [uf for uf in unit_files if not re.search(r'unit_\d+_(\d+x\d+)\.mp4$', os.path.basename(uf))]
    if not unit_files:
        unit_files = sorted(glob.glob(os.path.join(project_dir, 'unit_*.mp4')))
    if not unit_files:
        unit_files = sorted(glob.glob(os.path.join(project_dir, 'scene_*.mp4')))

    if unit_files:
        print(f"[Video Renderer] Standard Mode: Found {len(unit_files)} primary unit MP4 files.")
        concat_video_files(
            project_dir,
            unit_files,
            output_filename="final_video.mp4",
            root_output_filename="video.mp4",
            bgm_path=bgm_path
        )
        processed_any = True

    if not processed_any:
        print(f"[Error] No unit MP4 files found in {project_dir}")
        sys.exit(1)


if __name__ == '__main__':
    main()
