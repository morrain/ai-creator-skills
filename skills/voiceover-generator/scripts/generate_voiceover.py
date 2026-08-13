#!/usr/bin/env python3
"""
Voiceover Generator & Subtitle Timestamp Extractor
Generates MP3 audio files and aligned SRT/JSON subtitle timestamps from video_script.json.
Uses scene-by-scene Edge-TTS generation with exponential retry and audio concatenation.
"""

import sys
import json
import os
import re
import argparse
import asyncio
import time
import subprocess

def get_audio_duration(audio_path, fallback_duration=1.0):
    """Uses ffprobe to obtain exact audio duration in seconds, falling back to fallback_duration."""
    if not os.path.exists(audio_path):
        return fallback_duration
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        dur = float(res.stdout.strip())
        if dur > 0:
            return dur
    except Exception:
        pass
    return fallback_duration


def format_srt_timestamp(seconds):
    """Converts seconds into SRT timestamp format HH:MM:SS,mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


def strip_ssml(text):
    """Strips SSML/XML tags from text, returning plain text for subtitles and JSON output.

    When voiceover fields contain SSML markup for polyphone disambiguation (e.g.,
    <phoneme alphabet='sapi' ph='hang2'>行</phoneme>), the raw SSML must be passed
    to TTS but must NOT appear in subtitle files or timeline JSON.
    Edge-TTS SentenceBoundary events already return clean text, so this function is
    mainly needed for the fallback path and for the `text` fields in output JSON.
    """
    return re.sub(r'<[^>]+>', '', text).strip()


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

def generate_ass_file(entries, ass_path):
    header = """[Script Info]
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
    events = []
    for sub in entries:
        st = format_ass_timestamp(sub['start'])
        et = format_ass_timestamp(sub['end'])
        txt = sub['text']
        events.append(f"Dialogue: 0,{st},{et},Default,,0,0,0,,{{\\an8\\pos(960,960)}}{txt}")
        
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(header + "\n".join(events) + "\n")

def clean_sub_text(text):
    """Strips trailing sentence-ending punctuation."""
    t = re.sub(r'[。！？!？；;]+$', '', text.strip())
    return t

def split_long_sentence(text, start_s, end_s, max_len=15):
    """Splits a long sentence into shorter sub-clauses by punctuation if length exceeds max_len."""
    clean_full = clean_sub_text(text)
    if len(clean_full) <= max_len:
        return [{"text": clean_full, "start": start_s, "end": end_s}]
    
    tokens = re.split(r'([，,；;。！？!？])', text)
    merged = []
    curr = ''
    for i in range(0, len(tokens)-1, 2):
        chunk = tokens[i] + tokens[i+1]
        if len(curr) + len(chunk) <= max_len:
            curr += chunk
        else:
            if curr:
                merged.append(curr)
            curr = chunk
    if len(tokens) % 2 != 0 and tokens[-1]:
        curr += tokens[-1]
    if curr:
        merged.append(curr)
    if not merged:
        merged = [text]
        
    total_chars = sum(len(c) for c in merged)
    dur = end_s - start_s
    
    res = []
    curr_t = start_s
    for idx, c in enumerate(merged):
        c_dur = (len(c) / total_chars) * dur if total_chars > 0 else dur / len(merged)
        c_end = curr_t + c_dur if idx < len(merged) - 1 else end_s
        c_text = clean_sub_text(c)
        if c_text:
            res.append({
                "text": c_text,
                "start": round(curr_t, 3),
                "end": round(c_end, 3)
            })
        curr_t = c_end
    return res

async def generate_single_unit_tts(text, output_mp3_path, voice="zh-CN-YunxiNeural", max_retries=2):
    """Generates audio for a single video unit with retry logic and captures sentence boundaries"""
    try:
        import edge_tts
    except ImportError:
        print("ERROR: 'edge-tts' module is not installed! Please install it with 'pip install edge-tts'.", file=sys.stderr)
        return False, []

    async def _do_tts():
        communicate = edge_tts.Communicate(text, voice)
        boundaries = []
        with open(output_mp3_path, 'wb') as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    off_s = chunk["offset"] / 10000000.0
                    dur_s = chunk["duration"] / 10000000.0
                    boundaries.append((off_s, off_s + dur_s, chunk["text"].strip()))
        return boundaries

    for attempt in range(max_retries):
        try:
            boundaries = await asyncio.wait_for(_do_tts(), timeout=15.0)
            if os.path.exists(output_mp3_path) and os.path.getsize(output_mp3_path) > 1000:
                return True, boundaries
        except Exception as e:
            print(f"EdgeTTS Notice (Attempt {attempt+1}/{max_retries}): {e}")
            await asyncio.sleep(0.2)
            
    return False, []

def create_mock_mp3(output_mp3_path, duration_seconds=1.0):
    """Fallback silent MP3 generator for offline unit test environments"""
    silent_mp3_frame = b'\xff\xfb\x90\xc4' + b'\x00' * 413
    with open(output_mp3_path, 'wb') as f:
        frames = max(1, int(duration_seconds * 38))
        f.write(silent_mp3_frame * frames)

def concat_mp3_files(unit_files, full_mp3_path):
    """Concatenates individual unit MP3 files into a single full voiceover MP3"""
    with open(full_mp3_path, 'wb') as outfile:
        for fname in unit_files:
            if os.path.exists(fname):
                with open(fname, 'rb') as infile:
                    outfile.write(infile.read())

def process_voiceover(script_path, output_dir, voice="zh-CN-YunxiNeural", provider="edge_tts"):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(script_path, 'r', encoding='utf-8') as f:
        script_data = json.load(f)
        
    units = script_data.get("units", [])
    if not units:
        raise ValueError("No 'units' array found in video_script.json!")

    timeline = []
    all_srt_entries = []
    unit_audio_files = []
    current_time = 0.0
    all_tts_passed = True

    for idx, unit in enumerate(units):
        unit_id = unit.get("unit_id", f"Unit {idx+1:02d}")
        # tts_text: raw voiceover (may contain SSML tags for polyphone disambiguation)
        # plain_text: SSML-stripped version used for subtitles and JSON output
        tts_text = unit.get("voiceover", "").strip()
        plain_text = strip_ssml(tts_text)
        desired_dur = float(unit.get("duration_seconds", 5))
        
        unit_mp3_filename = f"unit_{idx+1:02d}.mp3"
        unit_mp3_path = os.path.join(output_dir, unit_mp3_filename)
        
        # Try generating real TTS for unit
        success = False
        boundaries = []
        if provider == "edge_tts" and tts_text:
            try:
                success, boundaries = asyncio.run(generate_single_unit_tts(tts_text, unit_mp3_path, voice))
                time.sleep(0.5) # Gentle pause between websocket connections
            except Exception as e:
                print(f"Unit {idx+1} TTS Error: {e}")
                success = False

        if not success:
            all_tts_passed = False
            print(f"WARNING: TTS generation failed for Unit {idx+1} ('{unit_id}'). Generating silent fallback MP3.", file=sys.stderr)
            create_mock_mp3(unit_mp3_path, duration_seconds=desired_dur)

        actual_dur = desired_dur
        if success and os.path.exists(unit_mp3_path):
            actual_dur = get_audio_duration(unit_mp3_path, fallback_duration=desired_dur)

        unit_audio_files.append(unit_mp3_path)
        
        start_time = current_time
        end_time = current_time + actual_dur
        
        # Fine-grained sentence/clause SRT entry generation
        unit_sub_items = []
        if boundaries:
            for b_start, b_end, b_text in boundaries:
                # Clamp end boundary to actual_dur
                b_end_clamped = min(b_end, actual_dur)
                g_start = start_time + b_start
                g_end = start_time + b_end_clamped
                clauses = split_long_sentence(b_text, g_start, g_end, max_len=18)
                unit_sub_items.extend(clauses)
        else:
            # Fallback: use plain_text (SSML stripped) to avoid tags leaking into subtitles
            clauses = split_long_sentence(plain_text, start_time, end_time, max_len=18)
            unit_sub_items.extend(clauses)

        all_srt_entries.extend(unit_sub_items)

        timeline.append({
            "unit_id": unit_id,
            "text": plain_text,  # SSML stripped: subtitle/JSON consumers expect plain text
            "start_seconds": round(start_time, 3),
            "end_seconds": round(end_time, 3),
            "duration_seconds": round(actual_dur, 3),
            "audio_file": unit_mp3_filename,
            "subtitles": unit_sub_items,
            "srt_start": format_srt_timestamp(start_time),
            "srt_end": format_srt_timestamp(end_time)
        })
        current_time = end_time

    # Combine into full_voiceover.mp3 and voiceover.mp3
    full_mp3_path = os.path.join(output_dir, "full_voiceover.mp3")
    concat_mp3_files(unit_audio_files, full_mp3_path)
    voiceover_path = os.path.join(output_dir, "voiceover.mp3")
    concat_mp3_files(unit_audio_files, voiceover_path)

    # Export timestamps.json
    result_json = {
        "metadata": script_data.get("metadata", {}),
        "voice": voice,
        "provider": provider,
        "total_duration_seconds": round(current_time, 3),
        "timeline": timeline
    }
    
    json_path = os.path.join(output_dir, "timestamps.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)

    # Export audio_meta.json compliant with HyperFrames official contract
    audio_meta_json = {
        "narration": {
            "file": "full_voiceover.mp3",
            "duration": round(current_time, 3)
        },
        "segments": [
            {
                "id": item["unit_id"],
                "start": item["start_seconds"],
                "end": item["end_seconds"],
                "duration": item["duration_seconds"],
                "text": item["text"],
                "subtitles": item.get("subtitles", [])
            }
            for item in timeline
        ]
    }
    audio_meta_path = os.path.join(output_dir, "audio_meta.json")
    with open(audio_meta_path, 'w', encoding='utf-8') as f:
        json.dump(audio_meta_json, f, ensure_ascii=False, indent=2)

    # Export subtitle.srt
    lines = []
    for idx, sub in enumerate(all_srt_entries, start=1):
        lines.append(str(idx))
        lines.append(f"{format_srt_timestamp(sub['start'])} --> {format_srt_timestamp(sub['end'])}")
        lines.append(sub['text'])
        lines.append("")
    
    srt_path = os.path.join(output_dir, "subtitles.srt")
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    # Export subtitles.ass
    ass_path = os.path.join(output_dir, "subtitles.ass")
    generate_ass_file(all_srt_entries, ass_path)
        
    return {
        "output_dir": output_dir,
        "timestamps_json": json_path,
        "audio_meta_json": audio_meta_path,
        "subtitles_srt": srt_path,
        "subtitles_ass": ass_path,
        "audio_mp3": full_mp3_path,
        "total_duration_seconds": round(current_time, 3),
        "tts_engine_used": "edge_tts_live" if all_tts_passed else "fallback_mixed"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voiceover & Subtitle Generator")
    parser.add_argument("--script", required=True, help="Path to video_script.json")
    parser.add_argument("--output-dir", required=True, help="Directory to save generated audio and subtitles")
    parser.add_argument("--voice", default="zh-CN-YunxiNeural", help="TTS voice name")
    parser.add_argument("--provider", default="edge_tts", help="TTS provider (edge_tts, openai, minimax)")
    
    args = parser.parse_args()
    
    res = process_voiceover(args.script, args.output_dir, args.voice, args.provider)
    print(json.dumps(res, ensure_ascii=False, indent=2))
