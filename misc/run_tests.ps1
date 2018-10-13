pushd .
cd ../src/test
py.test

if ($lastExitCode -eq 0) { }
else
{
	pause
}

popd

