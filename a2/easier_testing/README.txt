Install
========================
1. Place Kmedians_core_GL.py beside the .pyc file. The next time you run your
local search, this will replace your .pyc file, so be aware of this.

2. pip install pyscreenshot
(globally, or in a virtual environment)

Main Changes
========================
The program closes by default when it finishes the search now. You can prevent
this to take a screenshot however.

Usage
========================
press 'p' to take a screenshot (you can change this in the kbHandler function)
however, you must change

  initKmedians(289, 1250, 9)
  to
  initKmedians(289, 1250, 9, True, 'screenshot.jpg')

to prevent the program from closing, and naming the screenshot 'screenshot.jpg'.

The argument True prevents the program from closing, the argument
'screenshot.jpg' is the filename of the screenshot.
