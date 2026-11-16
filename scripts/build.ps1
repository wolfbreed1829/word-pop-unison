$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
$source = Get-Content -Raw -Encoding UTF8 src/game.u
$transcript = "``````unison`n$source`n```````n``````ucm`nword-pop/main> update`nword-pop/main> test`nword-pop/main> compile pop.local .ucm/local`nword-pop/main> compile pop.deploy .ucm/deploy`n```````n"
[IO.File]::WriteAllText((Join-Path (Get-Location) '.ucm/build.md'), $transcript, [Text.UTF8Encoding]::new($false))
chcp.com 65001 | Out-Null
ucm -c .ucm transcript.in-place .ucm/build.md
if ($LASTEXITCODE -ne 0) { throw 'Unison build failed.' }
