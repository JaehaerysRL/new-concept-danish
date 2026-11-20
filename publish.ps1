param(
    [switch]$SyncDrive
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$DistDir = Join-Path $Root "dist"
New-Item -ItemType Directory -Force -Path $DistDir | Out-Null

# Google Drive target folder: Dansk/NCD
$DriveFolderId = "1duB6-R7kq5gv8DBrMr99lP1CusMxbqSh"

$Jobs = @(
    @{ Dir = "syllabus";     Tex = "00_NCD_Syllabus.tex";     OutPdf = "00_新概念丹麦语_总目录与语法大纲.pdf" },
    @{ Dir = "ncd1";         Tex = "NCD1_Book.tex";           OutPdf = "NCD1_Foerste_Skridt.pdf" },
    @{ Dir = "ncd2";         Tex = "NCD2_Book.tex";           OutPdf = "NCD2_Fra_Saetning_til_Tekst.pdf" },
    @{ Dir = "modul2_tests"; Tex = "NCD2_Modultest_Book.tex"; OutPdf = "NCD2_DU3_Modul2_Modultest_1_4.pdf" },
    @{ Dir = "ncd3";         Tex = "NCD3_Book.tex";           OutPdf = "NCD3_Hverdag_og_Samfund.pdf" },
    @{ Dir = "modul3_tests"; Tex = "NCD3_Modultest_Book.tex"; OutPdf = "NCD3_DU3_Modul3_Modultest_1_4.pdf" },
    @{ Dir = "ncd4";         Tex = "NCD4_Book.tex";           OutPdf = "NCD4_Holdning_og_Debat.pdf" },
    @{ Dir = "modul4_tests"; Tex = "NCD4_Modultest_Book.tex"; OutPdf = "NCD4_DU3_Modul4_Modultest_1_4.pdf" },
    @{ Dir = "ncd5";         Tex = "NCD5_Book.tex";           OutPdf = "NCD5_Tanke_og_Perspektiv.pdf" }
)

function Get-AuxSignature {
    param([string]$Dir, [string]$BaseName)
    $parts = foreach ($ext in @(".toc", ".out", ".aux")) {
        $p = Join-Path $Dir ($BaseName + $ext)
        if (Test-Path $p) { (Get-FileHash -Path $p -Algorithm SHA256).Hash } else { "MISSING" }
    }
    return ($parts -join "|")
}

foreach ($job in $Jobs) {
    $WorkDir = Join-Path $Root $job.Dir
    $TexPath = Join-Path $WorkDir $job.Tex
    if (-not (Test-Path $TexPath)) { continue }

    $BaseName = [System.IO.Path]::GetFileNameWithoutExtension($job.Tex)
    $MaxPasses = 4
    Write-Host "==> Compiling $($job.Tex) (up to $MaxPasses passes until TOC/bookmarks stabilize)..." -ForegroundColor Cyan
    Push-Location $WorkDir
    try {
        for ($pass = 1; $pass -le $MaxPasses; $pass++) {
            $prevSig = Get-AuxSignature -Dir $WorkDir -BaseName $BaseName
            & xelatex -interaction=nonstopmode -halt-on-error $job.Tex | Out-Null
            if ($LASTEXITCODE -ne 0) {
                $LogFile = "$BaseName.log"
                if (Test-Path $LogFile) {
                    Write-Host "=== Tail of $LogFile ===" -ForegroundColor Red
                    Get-Content $LogFile -Tail 40 | ForEach-Object { Write-Host $_ }
                }
                throw "xelatex pass $pass failed for $($job.Tex)"
            }
            $currSig = Get-AuxSignature -Dir $WorkDir -BaseName $BaseName
            if ($pass -ge 2 -and $currSig -eq $prevSig) {
                Write-Host "    Converged after $pass passes." -ForegroundColor DarkGray
                break
            }
        }

        $BuiltPdf = [System.IO.Path]::ChangeExtension($job.Tex, ".pdf")
        Copy-Item -Path (Join-Path $WorkDir $BuiltPdf) -Destination (Join-Path $DistDir $job.OutPdf) -Force
        Write-Host "    Built dist\$($job.OutPdf)" -ForegroundColor Green
    }
    finally {
        Pop-Location
    }
}

if ($SyncDrive) {
    Write-Host "==> Syncing PDFs to Google Drive (Dansk/NCD)..." -ForegroundColor Cyan
    $ExistingJson = & gdrive readonly ls $DriveFolderId --json | ConvertFrom-Json
    foreach ($job in $Jobs) {
        $LocalPdf = Join-Path $DistDir $job.OutPdf
        if (-not (Test-Path $LocalPdf)) { continue }

        $Match = $ExistingJson | Where-Object { $_.name -eq $job.OutPdf } | Select-Object -First 1
        if ($Match) {
            Write-Host "    Updating existing file: $($job.OutPdf) (ID: $($Match.id))"
            & gdrive mutate update $Match.id $LocalPdf
        } else {
            Write-Host "    Uploading new file: $($job.OutPdf)"
            & gdrive mutate upload $LocalPdf --parent $DriveFolderId
        }
    }
}

Write-Host "Done!" -ForegroundColor Green
