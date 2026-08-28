@echo off
setlocal
set GRADLE_VERSION=9.2.1
set GRADLE_SHA256=72f44c9f8ebcb1af43838f45ee5c4aa9c5444898b3468ab3f4af7b6076c5bc3f
if "%GRADLE_USER_HOME%"=="" set GRADLE_USER_HOME=%USERPROFILE%\.gradle
set BASE=%GRADLE_USER_HOME%\black-arcana-bootstrap
set INSTALL=%BASE%\gradle-%GRADLE_VERSION%
if exist "%INSTALL%\bin\gradle.bat" goto run
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $v='%GRADLE_VERSION%'; $expected='%GRADLE_SHA256%'; $base='%BASE%'; $zip=Join-Path $base ('gradle-'+$v+'-bin.zip'); New-Item -ItemType Directory -Force -Path $base | Out-Null; Invoke-WebRequest ('https://services.gradle.org/distributions/gradle-'+$v+'-bin.zip') -OutFile $zip; $actual=(Get-FileHash $zip -Algorithm SHA256).Hash.ToLowerInvariant(); if ($actual -ne $expected.ToLowerInvariant()) { Remove-Item $zip -Force -ErrorAction SilentlyContinue; throw 'Gradle distribution checksum mismatch.' }; $tmp=Join-Path $base '.tmp'; Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue; Expand-Archive $zip -DestinationPath $tmp -Force; Remove-Item '%INSTALL%' -Recurse -Force -ErrorAction SilentlyContinue; Move-Item (Join-Path $tmp ('gradle-'+$v)) '%INSTALL%'; Remove-Item $tmp -Recurse -Force; Remove-Item $zip -Force"
if errorlevel 1 exit /b 1
:run
call "%INSTALL%\bin\gradle.bat" %*
exit /b %ERRORLEVEL%
