#login.ps1

Param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$OutPath
)

[DateTime]$Yesterday = (Get-Date).AddDays(-1)

function Get-EpochTime {
    param([DateTime]$Time)
    if ($null -eq $Time) { return 0 }
    try { return [int]([DateTimeOffset]$Time).ToUnixTimeSeconds() }
    catch { return 0 }
}

$basePath = $OutPath
$outputFile = Join-Path $basePath "login_report.csv"

Write-Host "Guardando en: $outputFile" -ForegroundColor Cyan

$SecFilter = @{
    LogName = 'Security'
    Id = 4624
    StartTime = $Yesterday
}

$LogonTypes = "2", "10", "7" # Interactiva, RDP, Desbloqueo
$NonRelv = '^(SYSTEM|LOCAL SERVICE|NETWORK SERVICE|.*\$)$'

$Logins = (Get-WinEvent -FilterHashtable $SecFilter -ErrorAction SilentlyContinue)

Write-Host "Inicios de Sesión de USUARIOS desde $($Yesterday.ToString()): " -ForegroundColor Cyan
Write-Host "---------------------------------------------------------------------------------------------------"

if ($Logins) {

    $LoginsFilt = foreach ($ev in $Logins) {

        $props = $ev.Properties
        $Usr = $props[5].Value
        if ([string]::IsNullOrWhiteSpace($Usr) -and $props.Count -gt 6) {
            $Usr = $props[6].Value
        }

        $LogonType = $props[8].Value
        if ([string]::IsNullOrWhiteSpace($LogonType) -and $props.Count -gt 9) {
            $LogonType = $props[9].Value
        }

        if(-not $LogonType){
            continue
        }

        if(($LogonType -in $LogonTypes) -and ($Usr -notmatch $NonRelv)){

            [PSCustomObject]@{
                TimeEpoch   = Get-EpochTime $ev.TimeCreated
                Usuario     = $Usr
                TipoLogon   = $LogonType
                MachineName = $ev.MachineName
            }
        }
    }

    if (@($LoginsFilt).Count -gt 0) {

        $LoginsFilt | Export-Csv $outputFile -NoTypeInformation -Encoding UTF8 -Force
        Write-Host "Registros exportados a: $outputFile" -ForegroundColor Green

    } else {

        "TimeEpoch,Usuario,TipoLogon,MachineName" | Out-File -Encoding UTF8 $outputFile
        "0,NO_DATA,NO_DATA,NO_DATA" | Add-Content -Encoding UTF8 $outputFile
        Write-Host "Sin eventos relevantes. Se generó un CSV vacío en: $outputFile" -ForegroundColor Yellow

    }
}

