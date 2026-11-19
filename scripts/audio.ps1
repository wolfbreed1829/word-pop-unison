$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$speech = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speech.Rate = -2
$voice = $speech.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Name -like '*Zira*' } | Select-Object -First 1
if ($voice) { $speech.SelectVoice($voice.VoiceInfo.Name) }
$audioDirectory = Join-Path $PSScriptRoot '../assets/audio'
New-Item -ItemType Directory -Force -Path $audioDirectory | Out-Null
$gameSource = Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot '../src/game.u')
$deckSource = ($gameSource -split 'pop.word :', 2)[0]
$words = @([regex]::Matches($deckSource, 'Card "([a-z]+)"') | ForEach-Object { $_.Groups[1].Value })
for ($i = 0; $i -lt $words.Count; $i++) {
  $audioPath = [IO.Path]::GetFullPath((Join-Path $audioDirectory "$i.wav"))
  if (Test-Path -LiteralPath $audioPath) { continue }
  $speech.SetOutputToWaveFile($audioPath)
  $speech.Speak($words[$i])
  $speech.SetOutputToNull()
}
$speech.Dispose()
Write-Output "Verified $($words.Count) spoken word clips for native browser audio playback."
