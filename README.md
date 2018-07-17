# encryption

`encrypt.py` requires the user to pip install the `pycryptodome` package. 

`encrypt.exe` holds both `encrypt.py` and the `pycryptodome` package; allowing it to be run without any installs.


## compiling instructions

first use pip to install the pyinstaller package, then run this command to convert encrypt.py to a signle file executible that does not open a console when run.


`pyinstaller -w -F encrypt.py`


if you want to compile using a custom .ico file put it in the same directory as encrypt.py and run the command below


`pyinstaller -w -F -i [icon_file] encrypt.py`
