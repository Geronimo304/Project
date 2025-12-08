#!/usr/bin/env python3
import os
import io
import tokenize

ROOT = '/root/Project/holbertonschool-hbnb/part3'

def process_file(path):
    with open(path, 'rb') as f:
        src = f.read()
    try:
        tokens = list(tokenize.tokenize(io.BytesIO(src).readline))
    except Exception as e:
        print(f"Skipping {path}: tokenize error: {e}")
        return False

    new_tokens = []
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            continue
        new_tokens.append(tok)

    try:
        new_src = tokenize.untokenize(new_tokens)
    except Exception as e:
        print(f"Skipping {path}: untokenize error: {e}")
        return False

    if isinstance(new_src, str):
        new_src = new_src.encode('utf-8')
    with open(path, 'wb') as outf:
        outf.write(new_src)
    print(f"Processed: {path}")
    return True


def should_process(path):
    if not path.endswith('.py'):
        return False
    if '__pycache__' in path:
        return False
    return True


def main():
    processed = 0
    for dirpath, dirs, files in os.walk(ROOT):
        if '.venv' in dirpath or 'venv' in dirpath:
            continue
        for fn in files:
            path = os.path.join(dirpath, fn)
            if should_process(path):
                ok = process_file(path)
                if ok:
                    processed += 1
    print(f"Done. Files processed: {processed}")

if __name__ == '__main__':
    main()
