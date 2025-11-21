param(
    [Parameter(Mandatory=$false)]
    [string]$MyPath
)

$Mypath = $null
$OutCsv = "./critical.csv"

$CheckTime = 24
$Limit = (Get-Date).AddHours(-$CheckTime)
$Logging = "System"

Write-Host "Buscando Events de error y críticos en el Logging '$Logging' de las últimas $CheckTime horas..."

$Events = Get-WinEvent -FilterHashtable @{
    LogName = $Logging
    StartTime = $Limit
    Level = 1, 2
} -ErrorAction SilentlyContinue

if ($Events) {
    $Events | Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message |
    Format-Table -AutoSize | Export-Csv $OutCsv -NoTypeInformation
} else {
    Write-Host "No se encontraron Events Críticos/Error en las últimas $CheckTime horas." -ForegroundColor Yellow
}

