import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
"packages": ["os", 'sys'],
"excludes": ["tkinter"],
"include_files": ["res"]
}

#
executables = [
    Executable("MusicMainUI.py", base=base, targetName="MusicDownloader.dmg", icon="res/icon.png")
]

setup( name = "setup",
        version = "0.1",
        description = "Music Downloader",
        author = "yliu",
        author_email = "kongmingddr@163.com",
        options = {"build_exe": build_exe_options},
        executables = executables,
)