#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from urllib.parse import unquote
from unicodedata import lookup

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

def convert_emojies_in_file(filepath):

    emojies_dict = {
        r":warning:": lookup("WARNING SIGN"),
        r':round_pushpin:': lookup("ROUND PUSHPIN"),
        r':information_source:': lookup("INFORMATION SOURCE"),
        r':large_blue_diamond:': lookup("LARGE BLUE DIAMOND")
    }

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original_content = content

    for ptn in emojies_dict.keys():
        content = re.sub(ptn, emojies_dict[ptn], content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Update emojies: {filepath}")
        return True
    else:
        print(f"  No changes with emojies: {filepath}")
        return False

def generate_contents(filename):
    if filename.name in ('Intro.md', 'README.md'):
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original_content = content

    header_pattern = r'^(#{1,6})\s+(.+)$'
    headers = []

    for line in content.split('\n'):
        match = re.match(header_pattern, line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headers.append((level, title))

    if not headers:
        print(f"  No changes with contents: {filepath}")
        return False

    toc_lines = [
        ''
        '# Быстрый поиск',
        ''
    ]

    seen_titles = {}

    for level, title in headers:
        anchor = unquote(title)

        anchor = re.sub(r'\s+', '-', anchor)
        anchor = re.sub(r'[`:]', '', anchor)

        anchor = re.sub(r'-+', '-', anchor)
        anchor = anchor.strip('-').lower()

        if anchor in seen_titles:
            seen_titles[anchor] += 1
            anchor = f"{anchor}-{seen_titles[anchor]}"
        else:
            seen_titles[anchor] = 1

        indent = ' ' * (2 * (level - 1))
        toc_lines.append(f'{indent} + [{title}](#{anchor})')

    toc_lines.append('')
    toc_lines.append('---')

    content = re.sub(r'\[:contents:\]', '\n'.join(toc_lines), content, flags=re.MULTILINE)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Generate contents: {filepath}")
        return True
    else:
        print(f"  No changes with contents: {filepath}")
        return False

def generate_startlines(filename):
    if filename.name in ('Intro.md', 'README.md'):
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original_content = content

    # Получаем имя текущего файла без расширения и директорию
    _name = filename.stem  # Имя файла без расширения
    _dir = filename.parent

    # Извлекаем номер лабораторной из имени директории
    dir_match = re.match(r'^(\d+)_(.+)$', _dir.name)
    lab_num_str, dirname = dir_match.groups()
    lab_num = int(lab_num_str)

    # Находим предыдущую и следующую директории
    parent_dir = _dir.parent

    # Находим предыдущую лабораторную
    prev_lab_num = lab_num - 1
    prev_lab_num_str = f"{prev_lab_num:02d}"
    next_lab_num = lab_num + 1
    next_lab_num_str = f"{next_lab_num:02d}"

    # Ищем предыдущую директорию
    prev_directory, next_directory = None, None
    for child in parent_dir.iterdir():
        if child.is_dir() and child.name.startswith(prev_lab_num_str + '_'):
            prev_directory = child
        if child.is_dir() and child.name.startswith(next_lab_num_str + '_'):
            next_directory = child

    # Находим файлы .md в найденных директориях
    prev_file = None
    if prev_directory:
        for file in prev_directory.iterdir():
            if file.is_file() and file.suffix == '.md':
                prev_file = file
                break

    next_file = None
    if next_directory:
        for file in next_directory.iterdir():
            if file.is_file() and file.suffix == '.md':
                next_file = file
                break

    # Получаем имена для вывода
    prev_name = prev_file.stem if prev_file else "Не найдена"
    next_name = next_file.stem if next_file else "Не найдена"

    # Формируем относительные пути
    prev_rel_path = f"../{prev_directory.name}/{prev_name.replace(' ', '%20')}.md" if prev_file else "#"
    next_rel_path = f"../{next_directory.name}/{next_name.replace(' ', '%20')}.md" if next_file else "#"

    # Выводим результат
    toc_lines = []
    toc_lines.append(f"# Лабораторная работа №{lab_num} — {_name}")
    toc_lines.append('')
    toc_lines.append(f" + [Все лабораторные работы по сетевым протоколам в Linux](../Intro.md)")
    if prev_file:
        toc_lines.append(f" + [Предыдущая лабораторная работа — {prev_name}]({prev_rel_path})")
    if next_file:
        toc_lines.append(f" + [Следующая лабораторная работа — {next_name}]({next_rel_path})")

    toc_lines.append('')
    toc_lines.append('---')


    content = re.sub(r'\[:startlines:\]', '\n'.join(toc_lines), content, flags=re.MULTILINE)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Generate startlines: {filepath}")
        return True
    else:
        print(f"  No changes with startlines: {filepath}")
        return False

md_files =  [
                f for f in Path('.').rglob('*.md')
                if '.git' not in str(f)
            ]

if not md_files:
    print("No .md files found")
    exit(0)

changed = 0
for filepath in sorted(md_files):
    if any([
        generate_contents(filepath),
        generate_startlines(filepath),
        convert_links_in_file(filepath),
        convert_emojies_in_file(filepath),
    ]):
        changed += 1

print(f"\nTotal: {len(md_files)} files processed, {changed} files changed")

