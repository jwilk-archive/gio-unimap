# encoding=UTF-8

# Copyright © 2012-2020 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

import ctypes
import errno
import fcntl
import sys

...  # Python 3 is required

GIO_UNIMAP = 0x4B66

class struct_unipair(ctypes.Structure):
    _fields_ = [
        ('unicode', ctypes.c_ushort),
        ('fontpos', ctypes.c_ushort),
    ]

class struct_unimap_desc(ctypes.Structure):
    _fields_ = [
        ('count', ctypes.c_ushort),
        ('entries', ctypes.POINTER(struct_unipair))
    ]

def get_unicode_map(file):
    if isinstance(file, int):
        fd = file
    else:
        fd = file.fileno()
    unimap_desc = struct_unimap_desc(count=0, entries=None)
    while True:
        try:
            fcntl.ioctl(fd, GIO_UNIMAP, unimap_desc)
        except IOError as ex:
            if ex.errno == errno.ENOMEM:
                if unimap_desc.count == 0:
                    raise
                entries = (struct_unipair * unimap_desc.count)()
                unimap_desc.entries = entries
                continue
            else:
                raise
        break
    return {
        chr(e.unicode): e.fontpos
        for e in entries
    }

if __name__ == '__main__':
    unicode_map = get_unicode_map(sys.stdin)
    print(*unicode_map, sep='')

# vim:ts=4 sts=4 sw=4 et
