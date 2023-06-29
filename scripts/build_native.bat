@echo off

if "%1" == "" goto error
if NOT "%1" == "Release" if NOT "%1" == "Debug" goto error

cd native
echo Building cargo in %1 mode...
if "%1" == "Release" (cargo build --release) else (cargo build)
cd ..
echo:
echo Copying native.dll...
copy native\\target\\debug\\native.dll build\\windows\\runner\\%1\\native.dll

echo:
echo Done!
exit 0

:error
echo Usage: build_native.bat [Release/Debug]
exit 1