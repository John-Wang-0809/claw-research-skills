"""
[IN]  Dependencies/Inputs:
 - 科研技能目录.md (Chinese catalog with English descriptions)
 - yunwu.ai API (LLM translation)
[OUT] Outputs:
 - 科研技能目录.md (updated with Chinese descriptions)
[POS] Position in the system:
 - One-time translation script. Batch-translates English skill descriptions
   to Chinese via LLM API. Supports checkpoint/resume.
"""

import re
import json
import time
import os
from dotenv import load_dotenv
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_BASE = os.getenv("BASE_URL", "https://yunwu.ai") + "/v1"
MODEL = "gpt-4o-mini"  # Use cheaper model for translation
BATCH_SIZE = 80
CONCURRENCY = 5
CHECKPOINT_FILE = "translate_checkpoint.json"

client = OpenAI(api_key=API_KEY, base_url=API_BASE)


def extract_descriptions(filepath):
    """Read catalog and extract (line_index, description) pairs from table rows."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (stripped.startswith('|')
            and not stripped.startswith('| 技能名称')
            and not stripped.startswith('|---')
            and not stripped.startswith('| #')
            and not stripped.startswith('| |')):
            cols = stripped.split('|')
            if len(cols) >= 4:
                desc = cols[2].strip()
                if desc and not all(ord(c) > 0x4e00 for c in desc[:3] if c.strip()):
                    entries.append((i, desc))
    return lines, entries


def translate_batch(descriptions, batch_id):
    """Send a batch of descriptions to LLM for translation."""
    numbered = "\n".join(f"{j+1}. {d}" for j, d in enumerate(descriptions))
    prompt = (
        "请将以下英文技术描述逐条翻译为简体中文。保留技术术语原文（如工具名、模型名、协议名、缩写等）。"
        "每行一条，严格按原编号输出，不要添加额外内容。\n\n"
        f"{numbered}"
    )
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4096,
        )
        text = resp.choices[0].message.content.strip()
        # Parse numbered lines
        results = {}
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^(\d+)\.\s*(.+)$', line)
            if m:
                idx = int(m.group(1)) - 1
                translation = m.group(2).strip()
                results[idx] = translation
        return results
    except Exception as e:
        print(f"  Batch {batch_id} error: {e}")
        return {}


def load_checkpoint():
    """Load translation checkpoint if exists."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_checkpoint(translations):
    """Save translation checkpoint."""
    with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)


def main():
    catalog_path = '科研技能目录.md'

    print(f"Reading {catalog_path}...")
    lines, entries = extract_descriptions(catalog_path)
    print(f"Found {len(entries)} descriptions to translate")

    # Load checkpoint
    checkpoint = load_checkpoint()
    print(f"Checkpoint: {len(checkpoint)} already translated")

    # Filter out already translated
    todo = [(i, desc) for i, desc in entries if str(i) not in checkpoint]
    print(f"Remaining: {len(todo)} to translate")

    if not todo:
        print("All descriptions already translated, applying...")
    else:
        # Create batches
        batches = []
        for start in range(0, len(todo), BATCH_SIZE):
            batch = todo[start:start + BATCH_SIZE]
            batches.append(batch)
        print(f"Batches: {len(batches)} (size {BATCH_SIZE}, concurrency {CONCURRENCY})")

        # Process batches with concurrency
        completed = 0
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
            futures = {}
            for batch_id, batch in enumerate(batches):
                descs = [desc for _, desc in batch]
                line_indices = [idx for idx, _ in batch]
                future = executor.submit(translate_batch, descs, batch_id)
                futures[future] = (batch_id, line_indices)

            for future in as_completed(futures):
                batch_id, line_indices = futures[future]
                results = future.result()
                for local_idx, translation in results.items():
                    if local_idx < len(line_indices):
                        line_idx = line_indices[local_idx]
                        checkpoint[str(line_idx)] = translation

                completed += 1
                translated_count = len(checkpoint)
                print(f"  Batch {batch_id + 1}/{len(batches)} done "
                      f"({translated_count}/{len(entries)} total, "
                      f"{translated_count * 100 // len(entries)}%)")

                # Save checkpoint periodically
                if completed % 3 == 0:
                    save_checkpoint(checkpoint)

        save_checkpoint(checkpoint)
        print(f"\nTranslation complete: {len(checkpoint)}/{len(entries)}")

    # Apply translations to file
    applied = 0
    for i, line in enumerate(lines):
        if str(i) in checkpoint:
            stripped = line.strip()
            cols = stripped.split('|')
            if len(cols) >= 4:
                cols[2] = f' {checkpoint[str(i)]} '
                lines[i] = '|'.join(cols) + '\n'
                applied += 1

    with open(catalog_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"Applied {applied} translations to {catalog_path}")

    # Clean up checkpoint
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
        print("Checkpoint cleaned up")


if __name__ == '__main__':
    main()
