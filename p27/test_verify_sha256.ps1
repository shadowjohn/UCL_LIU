$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$verifier = Join-Path $repoRoot "p27\verify_sha256.ps1"
$caseRoot = Join-Path $env:TEMP ("uclliu-sha256-test-" + [guid]::NewGuid().ToString("N"))

function New-TestFile {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$Content
  )
  $dir = Split-Path -Parent $Path
  if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir | Out-Null
  }
  [System.IO.File]::WriteAllText($Path, $Content, [System.Text.Encoding]::ASCII)
}

function Invoke-Verifier {
  param(
    [Parameter(Mandatory = $true)][string]$ManifestPath,
    [Parameter(Mandatory = $true)][string]$BasePath
  )
  & pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File $verifier -ManifestPath $ManifestPath -BasePath $BasePath *> $null
  return $LASTEXITCODE
}

function Assert-Equal {
  param(
    [Parameter(Mandatory = $true)]$Actual,
    [Parameter(Mandatory = $true)]$Expected,
    [Parameter(Mandatory = $true)][string]$Message
  )
  if ($Actual -ne $Expected) {
    throw "$Message Expected <$Expected>, got <$Actual>."
  }
}

try {
  New-Item -ItemType Directory -Path $caseRoot | Out-Null

  $validBase = Join-Path $caseRoot "valid"
  $validFile = Join-Path $validBase "nested\ok.txt"
  New-TestFile -Path $validFile -Content "known content"
  $validHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $validFile).Hash.ToLowerInvariant()
  $validManifest = Join-Path $caseRoot "valid.sha256"
  New-TestFile -Path $validManifest -Content "$validHash  nested/ok.txt`r`n"
  Assert-Equal -Actual (Invoke-Verifier -ManifestPath $validManifest -BasePath $validBase) -Expected 0 -Message "Valid manifest should pass."

  $badHashManifest = Join-Path $caseRoot "bad-hash.sha256"
  New-TestFile -Path $badHashManifest -Content ("{0}  nested/ok.txt`r`n" -f ("0" * 64))
  Assert-Equal -Actual (Invoke-Verifier -ManifestPath $badHashManifest -BasePath $validBase) -Expected 1 -Message "Hash mismatch should fail."

  $missingManifest = Join-Path $caseRoot "missing.sha256"
  New-TestFile -Path $missingManifest -Content "$validHash  nested/missing.txt`r`n"
  Assert-Equal -Actual (Invoke-Verifier -ManifestPath $missingManifest -BasePath $validBase) -Expected 1 -Message "Missing file should fail."

  Write-Host "[OK] verify_sha256 tests passed."
}
finally {
  Remove-Item -LiteralPath $caseRoot -Recurse -Force -ErrorAction SilentlyContinue
}
