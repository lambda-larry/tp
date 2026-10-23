#!/usr/bin/env python3
import sys

# PERF: Faster code generation
#   - string buffer for raw mode, and flush when done or newline
# TODO: String escape
# TODO: Single line comment
# TODO: Test for else
# TODO: Match statement


content = sys.stdin.buffer.read()

# State
mode = 'template-expr'
mode = 'template-stmt'
mode = 'normal'
output = bytearray(1024 * 1024 * 4)
o = 0
indent = 0

def isalnum(i):
    return (0x30 <= i and i <= 0x39) \
        or (0x41 <= i and i <= 0x5A) \
        or (0x61 <= i and i <= 0x7A)

def isspace(i):
    return 0x0A == i \
        or 0x09 == i \
        or 0x0D == i \
        or 0x20 == i

def bwrite(bs):
    global o
    for b in bs:
        output[o] = b
        o += 1

def tabs():
    global o
    for i in range(indent):
        output[o + i] = ord('\t')
    o += indent

def raw(c):
    global o
    if isalnum(c):
        tabs()
        bwrite(b'print("')
        output[o] = c
        o += 1
        bwrite(b'", end="")\n')
    else:
        tabs()
        bwrite(b'print(chr(')
        bwrite(hex(c).encode('ascii'))
        bwrite(b'), end="")\n')

def stmt(c):
    global o
    output[o] = c
    o += 1

def expr(c):
    bwrite(b'\\x')
    bwrite(c.hex().encode('ascii'))

i = 0
while i < len(content):
    if mode == 'normal':
        if content[i:].startswith(b'{%'):
            mode = 'template-stmt'
            i += 2
            while isspace(content[i]):
                i += 1

            if content[i:].startswith(b'end'):
                i += 3
                indent -= 1
                continue

            if content[i:].startswith(b'else:'):
                i += 5
                indent -= 1
                tabs()
                bwrite(b'else:\n')
                indent += 1
                tabs()
                continue
            if content[i:].startswith(b'elif '):
                i += 5
                indent -= 1
                tabs()
                bwrite(b'elif ')
                indent += 1
                continue

            tabs()

            for kw in [b'for', b'if', b'while', b'with']:
                if content[i:].startswith(kw):
                    bwrite(kw)
                    i += len(kw)
                    indent += 1
                    break

            continue
        if content[i:].startswith(b'{{{'):
            i += 3
            raw(ord(b'{'))
            raw(ord(b'{'))
            raw(ord(b'{'))
            continue
        if content[i:].startswith(b'{{'):
            mode = 'template-expr'
            i += 2
            while isspace(content[i]):
                i += 1
            tabs()
            bwrite(b'print(eval("""')
            continue

        raw(content[i])
        i += 1
        continue

    if mode == 'template-stmt':
        if content[i:].startswith(b'%}'):
            mode = 'normal'
            i += 2
            if '\n' == content[i]:
                i += 1
            bwrite(b'\n')
            tabs()
            bwrite(b'pass\n')
            continue
        stmt(content[i])
        i += 1
        continue

    if mode == 'template-expr':
        if content[i:].startswith(b'}}'):
            mode = 'normal'
            i += 2
            bwrite(b'"""), end="")\n')
            continue

        expr(content[i])
        i += 1
        continue
    assert False

# print(output[:o])
# print(output[:o].decode('utf-8'))
exec(output[:o].decode('utf-8'))
