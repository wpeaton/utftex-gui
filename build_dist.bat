REM build number currently manually incremented in file_version_info.txt
REM TODO add called to incrementer e.g. python increment_buildnum.py
pyinstaller utftex_gui.spec

REM to fix pyi-set_version edit SetVersion function in c:\python34\Lib\site-packages\pyinstaller\utils\win32\versioninfo.py
REM    # insert new code here
REM    import pefile
REM    pe = pefile.PE(exenm, fast_load=True)
REM    try:
REM       overlay = pe.get_overlay()
REM    finally:
REM        pe.close()
REM    # end of added code
REM        
REM    hdst = win32api.BeginUpdateResource(exenm, 0)
REM    win32api.UpdateResource(hdst, pefile.RESOURCE_TYPE['RT_VERSION'], 1, vs.toRaw())
REM    win32api.EndUpdateResource (hdst, 0)
REM    
REM    # more new code
REM    with open(exenm, 'ab') as exef:
REM        exef.write(overlay)
REM    # end of more new code

REM  edit version.txt to change version
REM python make_version.py
REM pyi-set_version file_version_info.txt dist\antijam\antijam.exe
pause
