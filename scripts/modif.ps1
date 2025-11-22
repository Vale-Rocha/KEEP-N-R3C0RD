#modif.ps1
Param(
    [Parameter(Mandatory=$true)]
    [string]$MyPath,
    
    [Parameter(Mandatory=$false)]
    [string]$UpdateFlag = "False",

    [Parameter(Mandatory=$false)]
    [stringg]$OutPath
)

function Get-EpochTime {
    Param([DateTime]$Time)
    # [int] para convertir a entero y eliminar milisegundos
    return [int][double]($Time.ToFileTime() - (Get-Date "1/1/1970").ToFileTime()) / 10000000
}

$HashArch = Join-Path $OutPath "hash_record.csv"
$ShotTimeEpoch = Get-EpochTime (Get-Date)

$OutCsv = Join-Path $OutPath "hash_wind.csv"

Write-Host "--- Monitoreo de Contenido por Hash en '$MyPath' ---" -ForegroundColor Cyan
Write-Host "Tipo de Hash: SHA256"

$MyPathClean = $MyPath.TrimEnd('\')

$Shot = Get-ChildItem -Path $MyPath -File -Recurse | 
    Get-FileHash -Algorithm SHA256 |
    Select-Object @{N='Namefile'; E={$_.Path.Replace("$MyPathClean\", "")}}, Hash | 
    Sort-Object Namefile

if (Test-Path $HashArch) {
    Write-Host "Cargando hashes anteriores desde '$HashArch'..."
    $Prev = Import-Csv $HashArch

    $Changes = Compare-Object $Prev $Shot -Property Namefile, Hash -PassThru

    Write-Host "`n[ $ShotTimeEpoch ] Informe de Cambios Detectados:" -ForegroundColor Yellow
    Write-Host "----------------------------------------------------------------"
    
    $Report = @()
    
    $DelFiles = $Changes | Where-Object {$_.SideIndicator -eq '<='}
    if (@($DelFiles).Count -gt 0) {
        Write-Host "* Archivos **ELIMINADOS**: $($DelFiles.Count)" -ForegroundColor Red
        $DelFiles | Select-Object Path | Out-Host
        $Report += $DelFiles | Select-Object Path, Hash, @{N='TipoCambio'; E={'ELIMINADO'}}
    }

    $CurrentChanges = $Changes | Where-Object {$PrevPaths -eq '=>'}
    $PrevPaths = $Prev.Path
    
    $NewFiles = $CurrentChanges | Where-Object { $PrevPaths -notcontains $_.Path }
    if (@($NewFiles).Count -gt 0) {
        Write-Host "* Archivos **NUEVOS**: $($NewFiles.Count)" -ForegroundColor Green
        $NewFiles | Select-Object Path | Out-Host 
        $Report += $NewFiles | Select-Object Path, Hash, @{N='TipoCambio'; E={'NUEVO'}}
    }

    $ModFiles = $CurrentChanges | Where-Object { $PrevPaths -contains $_.Path }
    if (@($ModFiles).Count -gt 0) {
        Write-Host "* Archivos **MODIFICADOS** (Cambio de Hash): $($ModFiles.Count)" -ForegroundColor Blue
        $ModFiles | Select-Object Path | Out-Host
        $Report += $ModFiles | Select-Object Path, Hash, @{N='TipoCambio'; E={'MODIFICADO'}}
    }
    
    if (@($Report).Count -gt 0) {
        $Report | Export-Csv $OutCsv -NoTypeInformation
        Write-Host "Reporte de cambios (Delta) generado en: $OutCsv" -ForegroundColor Green
    } else {
        Write-Host "¡No se detectaron cambios en el contenido de los archivos!" -ForegroundColor White
    }
    
    $ShouldUpdate = [bool]::Parse($UpdateFlag)

    if ($ShouldUpdate -eq $true) {
        $Shot | Export-Csv $HashArch -NoTypeInformation
        Write-Host "`nRegistro de hashes actualizado por decisión del usuario."
    } else {
        Write-Host "`nRegistro de hashes NO actualizado."
    }

} else {
    Write-Host "Es la **PRIMERA** ejecución. Creando el archivo de registro con los hashes actuales." -ForegroundColor Yellow
    $Shot | Export-Csv $HashArch -NoTypeInformation
    Write-Host "¡El registro se ha creado correctamente! Ejecuta el script de nuevo para monitorear cambios."
}

Write-Host "Auditoría de cambio de hashes finalizada para $MyPath"