pushd test
foreach ($i in ls *.yaml) { Write-Host "---------------------------------------------------------------------"; Write-Host "$i`n`n`n"; python ../wing.py $i}
foreach ($i in ls *.wing) { Write-Host "---------------------------------------------------------------------"; Write-Host "$i`n`n`n"; python ../wing.py $i}
popd