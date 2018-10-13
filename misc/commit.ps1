./run_tests.ps1

if ($lastExitCode -eq 0) { }
else
{
	Write-Host "`n`n`nTests failed. Continue with commit + push?"
	pause
}

[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.VisualBasic') | Out-Null
$commit_msg = [Microsoft.VisualBasic.Interaction]::InputBox("Enter a commit message", "Computer", "")

pushd ..

git add *
git commit -m $commit_msg
git config credential.helper store
git push

popd

