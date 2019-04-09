pushd test
foreach ($i in ls *.yaml) { Write-Host "---------------------------------------------------------------------"; Write-Host "$i`n`n`n"; python ../craft.py $i}
foreach ($i in ls *.craft) { Write-Host "---------------------------------------------------------------------"; Write-Host "$i`n`n`n"; python ../craft.py $i}
popd