#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import sys
from os.path import abspath, dirname, join

path = dirname(abspath(__file__))
module = join(path, "..", "..")

sys.path.append(join(module, "lib"))
sys.path.append(join(module, "remote"))

from thriftbackend.thriftgen.pyload import ttypes
from thriftbackend.thriftgen.pyload.Pyload import Iface


def main():

    enums = []
    classes = []

    print "generating lightweight ttypes.py"

    for name in dir(ttypes):
        klass = getattr(ttypes, name)

        if name in ("TBase", "TExceptionBase") or name.startswith("_") or not (issubclass(klass, ttypes.TBase) or issubclass(klass, ttypes.TExceptionBase)):
            continue

        if hasattr(klass, "thrift_spec"):
           classes.append(klass)
        else:
            enums.append(klass)


    f = open(join(path, "ttypes.py"), "wb")

    f.write(
        """#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autogenerated by pyload
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING

class BaseObject(object):
\t__slots__ = []

""")

    ## generate enums
    for enum in enums:
        name = enum.__name__
        f.write("class %s:\n" % name)

        for attr in dir(enum):
            if attr.startswith("_") or attr in ("read", "write"): continue

            f.write("\t%s = %s\n" % (attr, getattr(enum, attr)))

        f.write("\n")

    for klass in classes:
        name = klass.__name__
        base = "Exception" if issubclass(klass, ttypes.TExceptionBase) else "BaseObject"
        f.write("class %s(%s):\n" % (name,  base))
        f.write("\t__slots__ = %s\n\n" % klass.__slots__)

        #create init
        args = ["self"] + ["%s=None" % x for x in klass.__slots__]

        f.write("\tdef __init__(%s):\n" % ", ".join(args))
        for attr in klass.__slots__:
            f.write("\t\tself.%s = %s\n" % (attr, attr))

        f.write("\n")

    f.write("class Iface:\n")

    for name in dir(Iface):
        if name.startswith("_"): continue

        func = inspect.getargspec(getattr(Iface, name))

        f.write("\tdef %s(%s):\n\t\tpass\n" % (name, ", ".join(func.args)))

    f.write("\n")

    f.close()

if __name__ == "__main__":
    main()