param([Parameter(ValueFromRemainingArguments=$true)][string[]]$UcmArguments)
$ErrorActionPreference = 'Stop'
chcp.com 65001 | Out-Null
& ucm @UcmArguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
