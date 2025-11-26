#winlog.ps1
Param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$OutputPath

)

function Get-EpochTime {
    Param([DateTime]$Time)

    if ($null -eq $Time) {
        return 0
    }

    try {
        return [int]([DateTimeOffset]$Time).ToUnixTimeSeconds()
    }
    catch {
        return 0
    }
}


$CsvFileName = "winlog_events.csv"
$CsvPath = Join-Path $OutputPath $CsvFileName

$CheckTime = 24
$Limit = (Get-Date).AddHours(-$CheckTime)
$Logging = "System"

Write-Output "Buscando Events de error y críticos en el Logging '$Logging' de las últimas $CheckTime horas..."

$Events = Get-WinEvent -FilterHashtable @{
    LogName = $Logging
    StartTime = $Limit
    Level = 1, 2
} -ErrorAction SilentlyContinue

if ($Events) {

    $Events |
    Select-Object `
        @{Name='TimeEpoch'; Expression={ Get-EpochTime $_.TimeCreated }}, `
        Id, `
        LevelDisplayName, `
        ProviderName, `
        Message |
    Export-Csv -Path $CsvPath -NoTypeInformation -Encoding UTF8


    Write-Host "Eventos guardados en: $CsvPath" -ForegroundColor Green

} else {
    Write-Host "No se encontraron Events Críticos/Error en las últimas $CheckTime horas." -ForegroundColor Yellow
}
