# REQUIERE PERMISOS DE ADMINISTRADOR
# Este script sobreescribe 'out.tmp' en cada ejecución.

cd $PSScriptRoot
[DateTime]$Yesterday = (Get-Date).AddDays(-1)

# --- Variables de Configuración ---
$RutaSalida = ".\out.tmp"
$SecFilter = @{
    LogName = 'Security'
    Id = 4624
    StartTime = $Yesterday
}
$LogonTypes = "2", "10", "7" # Interactiva, RDP, Desbloqueo
$NonRelv = "SYSTEM", "LOCAL SERVICE", "NETWORK SERVICE", "*$"

# --- 1. Obtención y Filtrado de Eventos ---

$Logins = (Get-WinEvent -FilterHashtable $SecFilter -ErrorAction SilentlyContinue)

Write-Host "Inicios de Sesión de USUARIOS desde $($Yesterday.ToString()): " -ForegroundColor Cyan
Write-Host "---------------------------------------------------------------------------------------------------"

# --- 2. Inicializar el Archivo de Salida (SOBRESCRIBIR) ---

"--- Informe de Inicios de Sesión Relevantes: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss") ---" | Set-Content -Path $RutaSalida

if ($Logins) {
    $LoginsFilt = $Logins | Where-Object {
        $LogonTyp = $_.Properties[8].Value
        $Usr = $_.Properties[5].Value
        ($LogonTypes -contains $LogonTyp) -and
        ($NonRelv -notcontains $Usr) -and
        ($Usr -notlike "*$")
    }

    # --- 3. Escribir Resultados ---

    if (@($LoginsFilt).Count -gt 0) {
        # Escribir el conteo (AÑADIR)
        "Total de inicios de sesión encontrados: $(@($LoginsFilt).Count)" | Add-Content -Path $RutaSalida
        " " | Add-Content -Path $RutaSalida

        # Escribir la tabla formateada (AÑADIR)
        $LoginsFilt | Select-Object TimeCreated,
            @{N='Usr'; E={$_.Properties[5].Value}},
            @{N='LogonTyp'; E={$_.Properties[8].Value}},
            MachineName |
        Format-Table -AutoSize -Wrap | Out-String | Add-Content -Path $RutaSalida

    } else {
        # Escribir mensaje de no encontrados (AÑADIR)
        "No se encontraron inicios de sesión relevantes en las últimas 24 horas." | Add-Content -Path $RutaSalida
    }

} else {
    # Escribir mensaje de error de acceso (AÑADIR)
    "No se encontraron eventos de inicio de sesión (4624) en el registro de Seguridad. (VERIFICAR PERMISOS DE ADMINISTRADOR)" | Add-Content -Path $RutaSalida
}

Write-Host "Informe de accesos guardado y sobrescrito en: $RutaSalida" -ForegroundColor Green