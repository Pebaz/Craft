#
pushd ..
cls; pyinstaller craft.spec --onedir --workpath bin/build --distpath bin -y
popd
