import os
import sys
import glob
import subprocess
import argparse
import json
import re

def concat_mp3_files(unit_files, full_mp3_path):
    """Concatenates individual unit MP3 files into a single full voiceover MP3 using FFmpeg re-encoding."""
    existing = [f for f in unit_files if os.path.exists(f)]
    if not existing:
        return
    list_txt = full_mp3_path + ".concat.txt"
    try:
        with open(list_txt, 'w', encoding='utf-8') as f:
            for fname in existing:
                f.write(f"file '{os.path.abspath(fname)}'\n")
        cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', list_txt,
            '-c:a', 'libmp3lame', '-b:a', '192k', '-ar', '44100',
            full_mp3_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except Exception as e:
        print(f"[Notice] FFmpeg MP3 concat: {e}, falling back to binary copy", file=sys.stderr)
        with open(full_mp3_path, 'wb') as outfile:
            for fname in existing:
                with open(fname, 'rb') as infile:
                    outfile.write(infile.read())
    finally:
        if os.path.exists(list_txt):
            try:
                os.remove(list_txt)
            except Exception:
                pass

def get_media_duration(file_path, fallback=1.0):
    """Uses ffprobe to get exact media duration in seconds"""
    if not os.path.exists(file_path):
        return fallback
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', file_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(json.loads(res.stdout)['format']['duration'])
    except Exception:
        return fallback

def clean_sub_text(text):
    """Strips trailing sentence-ending punctuation."""
    t = re.sub(r'[。！？!？；;]+$', '', text.strip())
    return t

def format_ass_timestamp(seconds):
    """Converts seconds into ASS timestamp format H:MM:SS.cc"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis >= 100:
        secs += 1
        centis -= 100
    return f"{hrs}:{mins:02d}:{secs:02d}.{centis:02d}"

def find_first_existing(project_dir, candidates):
    """Finds the first existing file among candidate paths relative to project_dir"""
    for cand in candidates:
        full = os.path.join(project_dir, cand)
        if os.path.exists(full):
            return full
    return None

def has_audio_track(file_path):
    """Uses ffprobe to check if media file contains an audio stream."""
    if not os.path.exists(file_path):
        return False
    try:
        cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of', 'json', file_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        streams = json.loads(res.stdout).get('streams', [])
        return len(streams) > 0
    except Exception:
        return False

def get_best_h264_encoder():
    """Detects if macOS h264_videotoolbox hardware encoder is available, falls back to libx264."""
    try:
        res = subprocess.run(['ffmpeg', '-encoders'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if 'h264_videotoolbox' in res.stdout:
            print("[Video Renderer] Detected macOS Hardware Acceleration (h264_videotoolbox). Enabling VideoToolbox GPU Encoder!")
            return ['-c:v', 'h264_videotoolbox', '-b:v', '6000k', '-pix_fmt', 'yuv420p', '-r', '30']
    except Exception:
        pass
    print("[Video Renderer] Using libx264 CPU Encoder.")
    return ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'fast', '-r', '30']

def main():
    parser = argparse.ArgumentParser(description="Concat scenes and mux audio via FFmpeg")
    parser.add_argument('--project-dir', required=True, help="Path to the project assets/video directory")
    parser.add_argument('--fast-concat', action='store_true', help="Fast direct concat (preserve unit embedded audio & HTML subtitles without re-encoding)")
    parser.add_argument('--skip-subtitles', action='store_true', help="Skip burning ASS subtitles")
    parser.add_argument('--skip-audio-remux', action='store_true', help="Skip re-multiplexing external voiceover MP3")
    parser.add_argument('--force-remux', action='store_true', help="Force re-multiplexing voiceover and burning ASS subtitles even if units have embedded audio")
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    
    # 1. Find aspect ratio groups (e.g., unit_01_9x16.mp4, unit_01_16x9.mp4)
    aspect_files_map = {}
    all_aspect_files = glob.glob(os.path.join(project_dir, 'unit_*', 'unit_*_*x*.mp4'))
    for f in all_aspect_files:
        filename = os.path.basename(f)
        match = re.search(r'unit_\d+_(\d+x\d+)\.mp4$', filename)
        if match:
            aspect = match.group(1)
            aspect_files_map.setdefault(aspect, []).append(f)

    for aspect in aspect_files_map:
        aspect_files_map[aspect] = sorted(aspect_files_map[aspect])

    if aspect_files_map:
        print(f"[Video Renderer] Multi-Aspect Mode: Found {len(aspect_files_map)} aspect ratio groups: {list(aspect_files_map.keys())}")
        for aspect, a_files in aspect_files_map.items():
            print(f"[Video Renderer] Processing aspect group '{aspect}' ({len(a_files)} files)...")
            concat_txt = os.path.join(project_dir, f'concat_{aspect}.txt')
            concat_v = os.path.join(project_dir, f'concatenated_{aspect}.mp4')
            out_v = os.path.join(project_dir, f'final_video_{aspect}.mp4')
            with open(concat_txt, 'w', encoding='utf-8') as f:
                for uf in a_files:
                    f.write(f"file '{os.path.abspath(uf)}'\n")
            
            bgm_path = find_first_existing(project_dir, ['bgm.mp3', 'audio/bgm.mp3', 'bgm.wav', 'audio/bgm.wav'])
            if bgm_path:
                filter_complex = "[0:a]volume=1.0[v_a];[1:a]volume=0.3[bgm_low];[v_a][bgm_low]amix=inputs=2:duration=first[aout]"
                concat_cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_txt, '-c', 'copy', concat_v]
                subprocess.run(concat_cmd, cwd=project_dir, check=True)
                mux_cmd = ['ffmpeg', '-y', '-i', concat_v, '-i', bgm_path, '-filter_complex', filter_complex, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', '-shortest', out_v]
                subprocess.run(mux_cmd, cwd=project_dir, check=True)
                if os.path.exists(concat_v): os.remove(concat_v)
            else:
                concat_cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_txt, '-c', 'copy', out_v]
                subprocess.run(concat_cmd, cwd=project_dir, check=True)
            
            if os.path.exists(concat_txt): os.remove(concat_txt)
            print(f"[Success] Generated multi-aspect final video: {out_v}")
            if 'assets/video' in project_dir:
                root_v = os.path.abspath(os.path.join(project_dir, f'../../video_{aspect}.mp4'))
                try:
                    import shutil
                    shutil.copyfile(out_v, root_v)
                    print(f"[Success] Copied multi-aspect video to root: {root_v}")
                except Exception as e:
                    print(f"[Notice] Copy multi-aspect video error: {e}")

    # Standard primary unit files search
    unit_files = sorted(glob.glob(os.path.join(project_dir, 'unit_*', 'unit_*.mp4')))
    unit_files = [uf for uf in unit_files if not re.search(r'unit_\d+_(\d+x\d+)\.mp4$', os.path.basename(uf))]
    if not unit_files:
        unit_files = sorted(glob.glob(os.path.join(project_dir, 'unit_*.mp4')))
    if not unit_files:
        unit_files = sorted(glob.glob(os.path.join(project_dir, 'scene_*.mp4')))
    if not unit_files:
        unit_files = sorted(glob.glob(os.path.join(project_dir, 'renders', '*.mp4')))
    if not unit_files:
        unit_files = sorted(glob.glob(os.path.join(project_dir, 'compositions', 'frames', '*.mp4')))

    if not unit_files:
        if aspect_files_map:
            print(f"[Video Renderer] Multi-Aspect Batch Concat completed successfully.")
            return
        print(f"[Error] No unit MP4 files found in {project_dir}")
        sys.exit(1)

    print(f"[Video Renderer] Found {len(unit_files)} primary unit MP4 files.")
    
    # Detect if units already contain embedded audio tracks
    units_have_audio = all(has_audio_track(uf) for uf in unit_files)
    fast_concat_mode = (args.fast_concat or units_have_audio) and units_have_audio and not args.force_remux

    if fast_concat_mode:
        print(f"[Video Renderer] Fast Concat Mode enabled (Units already contain audio/subtitles). Preserving embedded audio and HTML subtitles without re-encoding.")
    elif not units_have_audio:
        print(f"[Video Renderer] Notice: Unit MP4 files do NOT contain embedded audio streams. Falling back to Voiceover multiplexing mode.")

    
    # 2. Perform Per-Unit Audio & Video Sync Alignment
    audio_dir = os.path.join(project_dir, 'audio')
    timestamps_json_path = os.path.join(audio_dir, 'timestamps.json')
    aligned_vo_path = None
    aligned_ass_path = None

    unit_audio_files = sorted(glob.glob(os.path.join(audio_dir, 'unit_*.mp3')))
    unit_speed_ratios = []
    unit_v_durs = [get_media_duration(uf) for uf in unit_files]
    final_video_unit_files = []
    temp_trimmed_videos = []

    if len(unit_audio_files) == len(unit_files):
        print(f"[Video Renderer] Dynamically aligning video unit durations and audio speed...")
        fitted_mp3_paths = []
        eff_v_durs = []
        for idx, (ap, vp, v_dur) in enumerate(zip(unit_audio_files, unit_files, unit_v_durs)):
            a_dur = get_media_duration(ap)
            fitted_mp3 = os.path.join(audio_dir, f"unit_{idx+1:02d}_fitted.mp3")
            
            # If audio is significantly shorter than video (>0.4s), trim video unit to match audio + 0.28s pause
            if a_dur < v_dur and (v_dur - a_dur) > 0.4:
                target_v_dur = round(a_dur + 0.28, 3)
                trimmed_vp = os.path.join(project_dir, f"unit_{idx+1:02d}_trimmed.mp4")
                trim_v_cmd = [
                    'ffmpeg', '-y', '-ss', '0', '-i', vp,
                    '-to', f"{target_v_dur:.3f}", '-c', 'copy',
                    trimmed_vp
                ]
                subprocess.run(trim_v_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                final_video_unit_files.append(trimmed_vp)
                temp_trimmed_videos.append(trimmed_vp)
                eff_v_durs.append(target_v_dur)

                unit_speed_ratios.append(1.0)
                pad_cmd = [
                    'ffmpeg', '-y', '-i', ap,
                    '-af', f"apad=whole_dur={target_v_dur:.3f}",
                    fitted_mp3
                ]
                subprocess.run(pad_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                fitted_mp3_paths.append(fitted_mp3)

            elif a_dur > v_dur:
                speed_ratio = a_dur / v_dur
                unit_speed_ratios.append(speed_ratio)
                eff_v_durs.append(v_dur)
                final_video_unit_files.append(vp)

                tempo_cmd = [
                    'ffmpeg', '-y', '-i', ap,
                    '-af', f"atempo={speed_ratio:.5f}",
                    fitted_mp3
                ]
                subprocess.run(tempo_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                fitted_mp3_paths.append(fitted_mp3)
            else:
                unit_speed_ratios.append(1.0)
                eff_v_durs.append(v_dur)
                final_video_unit_files.append(vp)
                fitted_mp3_paths.append(ap)

        unit_v_durs = eff_v_durs

        aligned_vo_path = os.path.join(audio_dir, 'aligned_voiceover.mp3')
        # Concat fitted audio files using FFmpeg re-encoding
        concat_mp3_files(fitted_mp3_paths, aligned_vo_path)
        
        # Clean temp fitted files
        for fmp3 in fitted_mp3_paths:
            if '_fitted.mp3' in fmp3 and os.path.exists(fmp3):
                os.remove(fmp3)
    else:
        final_video_unit_files = unit_files
        unit_speed_ratios = [1.0] * len(unit_files)

    # Compute video unit start offsets
    unit_v_starts = []
    curr_t = 0.0
    for dur in unit_v_durs:
        unit_v_starts.append(curr_t)
        curr_t += dur
    print(f"[Video Renderer] Unit video start offsets: {[round(s, 2) for s in unit_v_starts]}")

    # 3. Create concat.txt & Fast concat video
    concat_txt_path = os.path.join(project_dir, 'concat.txt')
    with open(concat_txt_path, 'w', encoding='utf-8') as f:
        for uf in final_video_unit_files:
            f.write(f"file '{uf}'\n")

    concat_video_path = os.path.join(project_dir, 'concatenated_scenes.mp4')
    concat_cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', 
        '-i', concat_txt_path, 
        '-c', 'copy', concat_video_path
    ]
    print(f"[Video Renderer] Concatenating scenes losslessly...")
    subprocess.run(concat_cmd, cwd=project_dir, check=True)

    # Clean temp trimmed videos
    for tvp in temp_trimmed_videos:
        if os.path.exists(tvp):
            os.remove(tvp)

    # Build aligned ASS subtitles using timestamps.json
    if os.path.exists(timestamps_json_path):
        try:
            with open(timestamps_json_path, 'r', encoding='utf-8') as f:
                ts_data = json.load(f)
            timeline = ts_data.get('timeline', [])
            if len(timeline) == len(unit_files):
                print(f"[Video Renderer] Generating video-synced ASS subtitles with WrapStyle=2...")
                ass_header = """[Script Info]
Title: Explainer Video Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,PingFang SC,44,&H00FFFFFF,&H00000000,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,3,0,2,120,120,54,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
                ass_events = []
                for idx, (item, u_start, s_ratio) in enumerate(zip(timeline, unit_v_starts, unit_speed_ratios)):
                    sub_list = item.get('subtitles', [])
                    unit_a_start = item.get('start_seconds', 0.0)
                    for sub in sub_list:
                        sub_text = clean_sub_text(sub.get('text', ''))
                        if not sub_text:
                            continue
                        rel_start = (sub.get('start', 0.0) - unit_a_start) / s_ratio
                        rel_end = (sub.get('end', 0.0) - unit_a_start) / s_ratio
                        
                        g_start = u_start + rel_start
                        g_end = u_start + rel_end
                        st = format_ass_timestamp(g_start)
                        et = format_ass_timestamp(g_end)
                        ass_events.append(f"Dialogue: 0,{st},{et},Default,,0,0,0,,{{\\an8\\pos(960,960)}}{sub_text}")
                
                aligned_ass_path = os.path.join(audio_dir, 'aligned_subtitles.ass')
                with open(aligned_ass_path, 'w', encoding='utf-8') as f:
                    f.write(ass_header + "\n".join(ass_events) + "\n")
        except Exception as e:
            print(f"[Notice] Failed to generate aligned ASS: {e}")

    # Fallbacks & Flags
    vo_path = None
    sub_path = None

    if not fast_concat_mode and not args.skip_audio_remux:
        vo_path = aligned_vo_path or find_first_existing(project_dir, [
            'full_voiceover.mp3', 'audio/voiceover.mp3', 'voiceover.mp3',
            'voiceover.wav', 'audio/voiceover.wav'
        ])

    if not fast_concat_mode and not args.skip_subtitles:
        sub_path = aligned_ass_path or find_first_existing(project_dir, [
            'subtitles.ass', 'audio/subtitles.ass', 'subtitles.srt', 'audio/subtitles.srt'
        ])

    bgm_path = find_first_existing(project_dir, [
        'bgm.mp3', 'audio/bgm.mp3', 'bgm.wav', 'audio/bgm.wav'
    ])
    
    final_output = os.path.join(project_dir, 'final_video.mp4')

    # Fast Concat path (No external voiceover remux & no ASS subtitle burning)
    if fast_concat_mode:
        if bgm_path:
            print(f"[Video Renderer] Fast Concat: Losslessly copying video & mixing BGM ({os.path.basename(bgm_path)})...")
            filter_complex = (
                "[0:a]volume=1.0[v_a];"
                "[1:a]volume=0.3[bgm_low];"
                "[v_a][bgm_low]amix=inputs=2:duration=first[aout]"
            )
            mux_cmd = [
                'ffmpeg', '-y',
                '-i', concat_video_path,
                '-i', bgm_path,
                '-filter_complex', filter_complex,
                '-map', '0:v',
                '-map', '[aout]',
                '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
                '-shortest',
                final_output
            ]
            subprocess.run(mux_cmd, cwd=project_dir, check=True)
        else:
            print(f"[Video Renderer] Fast Concat: Pure lossless concatenation to final video.")
            if os.path.exists(final_output):
                os.remove(final_output)
            import shutil
            shutil.copyfile(concat_video_path, final_output)
    else:
        # Standard multiplexing path (Legacy / Force remux)
        vcodec_args = []
        vf_args = []
        if sub_path:
            sub_rel = os.path.relpath(sub_path, project_dir)
            if sub_rel.endswith('.ass'):
                sub_filter = f"ass={sub_rel}"
            else:
                sub_filter = f"subtitles=filename={sub_rel}:force_style='PlayResX=1920,PlayResY=1080,FontSize=36,FontName=PingFang SC,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,MarginV=54,MarginL=120,MarginR=120,WrapStyle=0'"
            print(f"[Video Renderer] Burning subtitles from {sub_rel}...")
            vcodec_args = get_best_h264_encoder()
            vf_args = ['-vf', sub_filter]
        else:
            vcodec_args = ['-c:v', 'copy']

        if vo_path and bgm_path:
            print(f"[Video Renderer] Multiplexing Voiceover ({os.path.basename(vo_path)}) & BGM ({os.path.basename(bgm_path)}) via Sidechain Ducking...")
            filter_complex = (
                "[1:a]volume=0.3[bgm_low];"
                "[2:a]asplit[vo_out][vo_side];"
                "[bgm_low][vo_side]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=300[bgm_ducked];"
                "[vo_out][bgm_ducked]amix=inputs=2:duration=first[aout]"
            )
            mux_cmd = [
                'ffmpeg', '-y',
                '-i', concat_video_path,
                '-i', bgm_path,
                '-i', vo_path,
            ] + vf_args + [
                '-filter_complex', filter_complex,
                '-map', '0:v',
                '-map', '[aout]',
            ] + vcodec_args + [
                '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
                '-shortest',
                final_output
            ]
            subprocess.run(mux_cmd, cwd=project_dir, check=True)
        elif vo_path:
            print(f"[Video Renderer] Multiplexing Voiceover ({os.path.basename(vo_path)}) only...")
            mux_cmd = [
                'ffmpeg', '-y',
                '-i', concat_video_path,
                '-i', vo_path,
            ] + vf_args + [
                '-map', '0:v',
                '-map', '1:a',
            ] + vcodec_args + [
                '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
                '-shortest',
                final_output
            ]
            subprocess.run(mux_cmd, cwd=project_dir, check=True)
        else:
            print(f"[Video Renderer] No external audio tracks found.")
            if sub_path:
                mux_cmd = [
                    'ffmpeg', '-y',
                    '-i', concat_video_path,
                ] + vf_args + vcodec_args + [
                    final_output
                ]
                subprocess.run(mux_cmd, cwd=project_dir, check=True)
            else:
                if os.path.exists(final_output):
                    os.remove(final_output)
                import shutil
                shutil.copyfile(concat_video_path, final_output)

    # Cleanup temp files
    if os.path.exists(concat_txt_path):
        os.remove(concat_txt_path)
    if os.path.exists(concat_video_path):
        os.remove(concat_video_path)

    # Also copy to root project directory if inside assets/video
    if 'assets/video' in project_dir:
        root_video_path = os.path.abspath(os.path.join(project_dir, '../../video.mp4'))
        try:
            import shutil
            shutil.copyfile(final_output, root_video_path)
            print(f"[Success] Copied final video to root: {root_video_path}")
        except Exception as e:
            print(f"[Notice] Root video copy: {e}")

    print(f"[Success] Generated final video: {final_output}")

if __name__ == '__main__':
    main()

