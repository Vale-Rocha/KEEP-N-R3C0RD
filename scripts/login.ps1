#login.ps1
Param(
    [Parameter(Mandatory=$true)][string]$OutFile
)

[DateTime]$Yesterday = (Get-Date).AddDays(-1)

function Get-EpochTime {
    Param([DateTime]$Time)
    # [int] para convertir a entero y eliminar milisegundos
    return [int][double]($Time.ToFileTime() - (Get-Date "1/1/1970").ToFileTime()) / 10000000
}

$OutTmp = $OutFile
$OutCsv = Join-Path (Split-Path -Path $OutFile) "login_report.csv"

$SecFilter = @{
    LogName = 'Security'
    Id = 4624
    StartTime = $Yesterday
}

$LogonTypes = "2", "10", "7" # Interactiva, RDP, Desbloqueo
$NonRelv = "SYSTEM", "LOCAL SERVICE", "NETWORK SERVICE", "*$"

$Logins = (Get-WinEvent -FilterHashtable $SecFilter -ErrorAction SilentlyContinue)

Write-Host "Inicios de Sesión de USUARIOS desde $($Yesterday.ToString()): " -ForegroundColor Cyan
Write-Host "---------------------------------------------------------------------------------------------------"

"--- Informe de Inicios de Sesión Relevantes: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss") ---" | Set-Content -Path $OutTmp

if ($Logins) {
    $LoginsFilt = $Logins | Where-Object {
        $LogonTyp = $_.Properties[8].Value
        $Usr = $_.Properties[5].Value
        ($LogonTypes -contains $LogonTyp) -and
        ($NonRelv -notcontains $Usr) -and
        ($Usr -notlike "*$")
    }

    if (@($LoginsFilt).Count -gt 0) {

        $Count = @($LoginsFilt).Count

        $EpochProps = @(
            @{N='TimeEpoch'; E={Get-EpochTime $_.TimeCreated}},
            @{N='Usuario'; E={$_.Properties[5].Value}},
            @{N='TipoLogon'; E={$_.Properties[8].Value}},
            'MachineName'
        )

        $LoginsFilt | Select-Object $EpochProps |
        Export-Csv $OutCsv -NoTypeInformation

        "Total de inicios de sesión encontrados: $Count. (Datos completos exportados a $OutCsv)" | Add-Content -Path $OutTmp
        
        $LoginsFilt | Select-Object $EpochProps |
        Format-Table -AutoSize -Wrap | Out-String | Add-Content -Path $OutTmp

    } else {
        "No se encontraron inicios de sesión relevantes en las últimas 24 horas." | Add-Content -Path $OutTmp
    }

} else {
    "No se encontraron eventos de inicio de sesión (4624) en el registro de Seguridad. (VERIFICAR PERMISOS DE ADMINISTRADOR)" | Add-Content -Path $OutTmp
}

Write-Host "Informe de accesos guardado y sobrescrito en: $OutTmp" -ForegroundColor Green