from cx_Freeze import setup, Executable

base = None

executables = [Executable("NotSuspciousFile.py", base=base)]

packages = ['os','cffi',"idna",'cryptography']
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Test",
    options = options,
    version = "1",
    description = 'Penis',
    executables = executables
)
