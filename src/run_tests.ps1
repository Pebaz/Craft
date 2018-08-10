pushd test
foreach ($i in ls) { Write-Host $i; Write-Host "---------------";python ../wing.py $i}
popd