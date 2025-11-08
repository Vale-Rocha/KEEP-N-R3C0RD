param(
    [Parameter(Mandatory=$false)]
    [string]$MyPath
)

$Mypath = $null

[DateTime]$Yesterday = (Get-Date).AddDays(-1)

$SecFilter = @{
    LogName = 'Security'
    Id = 4624
    StartTime = $Yesterday
}

$Logins = (Get-WinEvent -FilterHashtable $SecFilter -ErrorAction SilentlyContinue)

$LogonTypes = "2", "10", "7"

$NonRelv = "SYSTEM", "LOCAL SERVICE", "NETWORK SERVICE", "*$" # El * incluye las Usrs de máquina (ej: NOMBREPC$)

Write-Host "Inicios de Sesión de USUARIOS desde $($Yesterday.ToString()): " -ForegroundColor Cyan
Write-Host "---------------------------------------------------------------------------------------------------"

if ($Logins) {
    $LoginsFilt = $Logins | Where-Object {
        $LogonTyp = $_.Properties[8].Value
        $Usr = $_.Properties[5].Value
        ($LogonTypes -contains $LogonTyp) -and 
        ($NonRelv -notcontains $Usr) -and
        ($Usr -notlike "*$")
    }

    if ($LoginsFilt.Count -gt 0) {
        Write-Host "Total de inicios de sesión encontrados: $($LoginsFilt.Count)" -ForegroundColor Green
        
        $LoginsFilt | Select-Object TimeCreated, 
            @{N='Usr'; E={$_.Properties[5].Value}},
            @{N='LogonTyp'; E={$_.Properties[8].Value}},
            MachineName |
        Format-Table -AutoSize -Wrap
    } else {
        Write-Host "No se encontraron inicios de sesión relevantes en las últimas 24 horas." -ForegroundColor Yellow
    }

} else {
    Write-Host "No se encontraron eventos de inicio de sesión (4624)." -ForegroundColor Yellow
}