#!/usr/bin/env python3
"""
4-Track Explainer Video Script Schema Validator
Validates video_script.json files against script_schema.json protocol.
Zero external dependencies required.
"""

import sys
import json
import os

def validate_script(script_path, schema_path=None):
    if not os.path.exists(script_path):
        return False, f"Script file not found: {script_path}"

    if schema_path is None:
        schema_path = os.path.join(os.path.dirname(__file__), "..", "references", "script_schema.json")

    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, f"Invalid JSON format: {str(e)}"

    # Check top-level required fields
    if "metadata" not in data or not isinstance(data["metadata"], dict):
        return False, "Missing or invalid 'metadata' object"
    if "units" not in data or not isinstance(data["units"], list):
        return False, "Missing or invalid 'units' array"

    # Validate metadata
    meta = data["metadata"]
    req_meta_fields = ["title", "target_duration_seconds", "genre", "mode"]
    for f in req_meta_fields:
        if f not in meta:
            return False, f"Missing required metadata field: '{f}'"
    if meta["mode"] not in ["article_derived", "standalone_topic"]:
        return False, f"Invalid metadata.mode: '{meta['mode']}'. Must be 'article_derived' or 'standalone_topic'"

    # Validate units
    if len(data["units"]) < 1:
        return False, "'units' array must contain at least one unit"

    req_unit_fields = [
        "unit_id", "duration_seconds", "voiceover",
        "visual_prompt", "ip_action", "on_screen_elements"
    ]
    req_elem_fields = ["title_card", "highlight_keywords", "graphics_hint"]

    for idx, unit in enumerate(data["units"]):
        if not isinstance(unit, dict):
            return False, f"Unit at index {idx} is not an object"

        for f in req_unit_fields:
            if f not in unit:
                return False, f"Unit {idx+1} ({unit.get('unit_id', 'unknown')}) missing required field: '{f}'"

        elems = unit["on_screen_elements"]
        if not isinstance(elems, dict):
            return False, f"Unit {idx+1} 'on_screen_elements' must be an object"

        for ef in req_elem_fields:
            if ef not in elems:
                return False, f"Unit {idx+1} 'on_screen_elements' missing field: '{ef}'"

        if not isinstance(elems["highlight_keywords"], list):
            return False, f"Unit {idx+1} 'highlight_keywords' must be an array"

    return True, "Script validation successful! Passed all 4-track schema gates."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_script.py <path_to_video_script.json>")
        sys.exit(1)

    path = sys.argv[1]
    ok, msg = validate_script(path)
    if ok:
        print(f"✅ SUCCESS: {msg}")
        sys.exit(0)
    else:
        print(f"❌ ERROR: {msg}")
        sys.exit(1)
