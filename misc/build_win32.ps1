pushd .
cd ..

if (!(Test-Path -Path bin))
{
	mkdir bin
}

cd bin
pyinstaller ../misc/craft.spec

if (!(Test-Path -Path win32))
{
	mkdir win32
}

Copy-Item ./dist/craft.exe ./win32/
Remove-Item dist -Force -Recurse
Remove-Item build -Force -Recurse
popd
