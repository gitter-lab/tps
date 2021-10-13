tasklist /fi "ImageName eq bash.exe" /fo csv 2>NUL | find "bash.exe">NUL
if "%ERRORLEVEL%"=="0" echo Program is running
