#
#  This copies all files given in argv to the same file name with a '.rep'
#  extension, replacing all the strings defined in replacements.py.
#  This is intended for use in conjunction with rstcheck which runs
#  independently of the variable replacement that sphinx does.
#

from replacements import *
import sys
from pathlib import Path

output_dir = Path(sys.argv[1])

for f in sys.argv[2:]:
    with open(f, 'r', encoding='utf-8') as fdin:
        data = fdin.read()
        for key in variable_replacements:
            data = data.replace(key, variable_replacements[key])
        with open(output_dir / f, 'w', encoding='utf-8') as fdout:
            fdout.write(data)
