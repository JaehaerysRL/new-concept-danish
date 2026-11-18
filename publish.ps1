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
    @{ Dir = "syllabus"; Tex = "00_NCD_Syllabus.tex"; OutPdf = "00_新概念丹麦语_总目录与语法大纲.pdf" },
    @{ Dir = "ncd1";     Tex = "NCD1_Book.tex";       OutPdf = "NCD1_Foerste_Skridt.pdf" },
    @{ Dir = "ncd2";     Tex = "NCD2_Book.tex";       OutPdf = "NCD2_Fra_Saetning_til_Tekst.pdf" }
)

foreach ($job in $Jobs) {
    $WorkDir = Join-Path $Root $job.Dir
    $TexPath = Join-Path $WorkDir $job.Tex
    if (-not (Test-Path $TexPath)) { continue }

    Write-Host "==> Compiling $($job.Tex) (2 passes)..." -ForegroundColor Cyan
    Push-Location $WorkDir
    try {
        & xelatex -interaction=nonstopmode -halt-on-error $job.Tex | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "xelatex pass 1 failed for $($job.Tex)" }
        & xelatex -interaction=nonstopmode -halt-on-error $job.Tex | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "xelatex pass 2 failed for $($job.Tex)" }

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
