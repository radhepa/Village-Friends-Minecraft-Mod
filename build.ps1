$ErrorActionPreference = 'Stop'
$jdk = [Environment]::GetEnvironmentVariable('JAVA_HOME', 'User')
if (-not $jdk -or -not (Test-Path (Join-Path $jdk 'bin\javac.exe'))) {
    throw 'Install a 64-bit JDK 25 and set JAVA_HOME before building.'
}
$env:JAVA_HOME = $jdk
$env:Path = (Join-Path $jdk 'bin') + ';' + $env:Path
Push-Location $PSScriptRoot
try {
    & .\gradlew.bat build --console=plain
    if ($LASTEXITCODE -ne 0) { throw 'Build or tests failed.' }
} finally { Pop-Location }
