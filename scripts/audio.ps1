$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$speech = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speech.Rate = -2
$voice = $speech.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Name -like '*Zira*' } | Select-Object -First 1
if ($voice) { $speech.SelectVoice($voice.VoiceInfo.Name) }
$audioDirectory = Join-Path $PSScriptRoot '../assets/audio'
New-Item -ItemType Directory -Force -Path $audioDirectory | Out-Null
$words = 'smart','award','charge','worn','argue','stormy','bore','ward','warp','backyard','door','dart','fort','morning','carpet','core','spark','charcoal','forecast','guard'
for ($i = 0; $i -lt $words.Count; $i++) {
  $audioPath = [IO.Path]::GetFullPath((Join-Path $audioDirectory "$i.wav"))
  $speech.SetOutputToWaveFile($audioPath)
  $speech.Speak($words[$i])
  $speech.SetOutputToNull()
}
$speech.Dispose()
Write-Output 'Created 20 spoken word clips for native browser audio playback.'
