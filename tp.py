#!/usr/bin/env python3
import sys

# TODO: String escape
# TODO: Single line comment
# TODO: Test for else
# TODO: Match statement


content = sys.stdin.read()

# State
mode = 'template-expr'
mode = 'template-stmt'
mode = 'normal'
output = ''
indent = 0

def tabs():
    return '\t' * indent

def raw(c):
    if c.isalnum():
        return f'{tabs()}print("{c}", end="")\n'
    else:
        return f'{tabs()}print(chr({ord(c):#02X}), end="")\n'

def stmt(c):
    return c

def expr(c):
    return f'\\x{ord(c):02X}'

i = 0
while i < len(content):
    if mode == 'normal':
        if content[i:].startswith('{%'):
            mode = 'template-stmt'
            i += 2
            while content[i].isspace():
                i += 1

            if content[i:].startswith('end'):
                i += 3
                indent -= 1
                continue

            if content[i:].startswith('else:'):
                i += 5
                indent -= 1
                output += tabs()
                output += 'else:\n'
                indent += 1
                output += tabs()
                continue
            if content[i:].startswith('elif '):
                i += 5
                indent -= 1
                output += tabs()
                output += 'elif '
                indent += 1
                continue

            output += tabs()

            for kw in ['for', 'if', 'while', 'with']:
                if content[i:].startswith(kw):
                    output += kw
                    i += len(kw)
                    indent += 1
                    break

            continue
        if content[i:].startswith('{{'):
            mode = 'template-expr'
            i += 2
            while content[i].isspace():
                i += 1
            output += f'{tabs()}print(eval("""'
            continue

        output += raw(content[i])
        i += 1
        continue

    if mode == 'template-stmt':
        if content[i:].startswith('%}'):
            mode = 'normal'
            i += 2
            if '\n' == content[i]:
                i += 1
            output += f'\n'
            output += tabs()
            output += f'pass\n'
            continue
        output += stmt(content[i])
        i += 1
        continue

    if mode == 'template-expr':
        if content[i:].startswith('}}'):
            mode = 'normal'
            i += 2
            output += f'"""), end="")\n'
            continue

        output += expr(content[i])
        i += 1
        continue
    assert False

exec(output)
# print(output)
