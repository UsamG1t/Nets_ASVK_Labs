#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from urllib.parse import unquote

def normalize_anchor(anchor):
    """
    Преобразует якорь в формат GitHub Pages:
    - Заменяет %20 на -
    - Приводит в lowercase
    - Убирает лишние символы (оставляет только буквы, цифры, дефисы)
    """
    anchor = unquote(anchor)
    
    anchor = re.sub(r'\s+', '-', anchor)
    anchor = re.sub(r'[`:]', '', anchor)
    
    anchor = re.sub(r'-+', '-', anchor)
    anchor = anchor.strip('-').lower()
    
    return anchor

def replace_link_with_anchor(match):
    path_part = match.group(1)
    anchor_part = match.group(2)
    
    normalized_anchor = normalize_anchor(anchor_part)
    new_path = path_part.replace('.md', '.html')

    return f"]({new_path}#{normalized_anchor})"


def convert_links_in_file(filepath):
    """
    1. .md#anchor -> .html#normalized-anchor
    2. .md) -> .html)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original_content = content
    
    pattern_with_anchor = r'\]\(([^\)]+\.md)#([^\)]*)\)'
    content = re.sub(pattern_with_anchor, replace_link_with_anchor, content)
    content = re.sub(r'\.md\)', '.html)', content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated: {filepath}")
        return True
    else:
        print(f"  No changes: {filepath}")
        return False

md_files = [f for f in Path('.').rglob('*.md') if '.git' not in str(f)]
    
if not md_files:
    print("No .md files found")
    exit(0)

changed = 0
for filepath in sorted(md_files):
    if convert_links_in_file(filepath):
        changed += 1
    
print(f"\nTotal: {len(md_files)} files processed, {changed} files changed")

