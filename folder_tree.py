import os
import sys
from pathlib import Path

def print_folder_tree(root_path, ignore_dirs=None, level=0, prefix='', is_last=True):
    if ignore_dirs is None:
        ignore_dirs = ['cases', '__pycache__', '.git']
    
    root = Path(root_path)
    
    # Skip ignored directories
    if root.name in ignore_dirs:
        return
    
    # ASCII-only tree symbols
    branch = '\\-- ' if is_last else '|-- '
    line = f"{prefix}{branch}{root.name}"
    
    # Write directly to stdout buffer
    try:
        sys.stdout.buffer.write(line.encode('utf-8'))
        sys.stdout.buffer.write(b'\n')
    except:
        print(line)  # Fallback
    
    # Process directories
    if root.is_dir():
        children = sorted([x for x in root.iterdir() if not x.name.startswith('.')])
        for i, child in enumerate(children):
            if child.name in ignore_dirs:
                continue
            new_prefix = prefix + ('    ' if is_last else '|   ')
            print_folder_tree(
                child, 
                ignore_dirs, 
                level + 1, 
                new_prefix, 
                is_last=(i == len(children) - 1)
            )

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    parser.add_argument('--ignore', nargs='+', default=['cases'])
    args = parser.parse_args()
    
    # Force UTF-8 output
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout.reconfigure(encoding='utf-8')
    
    print(f"Ignoring directories: {args.ignore}")
    print_folder_tree(args.root, args.ignore)