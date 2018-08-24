pushd .
./build_win32.ps1
cd ..

if (Test-Path -Path dist/win32)
{
	Remove-Item dist/win32 -Force -Recurse
}
mkdir dist/win32

Copy-Item bin/win32/wing.exe dist/win32
Copy-Item stdlib/ dist/win32
popd