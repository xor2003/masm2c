coverage erase
coverage run -a masm2c.py asmTests/*.asm
coverage run -a masm2c.py -m single asmTests/proc.asm
coverage run -a masm2c.py -m persegment asmTests/proc.asm
coverage run -a masm2c.py -m separate asmTests/proc.asm
coverage run -a masm2c.py -m single asmTests/jxx.asm
coverage run -a masm2c.py -m persegment asmTests/jxx.asm
coverage run -a masm2c.py -m separate asmTests/jxx.asm
coverage run -a masm2c.py -FL -d asmTests/hello.lst
coverage run -a -m pytest tests
coverage html
cd htmlcov
iexplore.exe index.html
