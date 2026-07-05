<#
.SYNOPSIS
  Max-quality one-pass duplex scan from the Plustek MobileOffice D620 via TWAIN
  (NAPS2 engine), with auto-deskew and auto-crop.

.DESCRIPTION
  WIA cannot drive this scanner's duplex (the Plustek WIA driver advertises duplex
  but rejects every duplex transfer). The working path is the Plustek TWAIN source,
  driven here through NAPS2's console. Scans both sides in a single feed at the
  hardware maximum (600 dpi, 24-bit color), deskews via NAPS2, and trims the dark
  feeder margins via a content-aware crop.

.PARAMETER OutDir
  Folder to write images into. Defaults to the user's Downloads folder.

.PARAMETER BaseName
  Base file name. Output is <BaseName>_1.<ext> (front) and <BaseName>_2.<ext> (back).

.PARAMETER Dpi
  Scan resolution. Default 600 (the D620 maximum).

.PARAMETER Format
  Output image extension: jpg (default) or png.

.PARAMETER NoCrop
  Skip the auto-crop border trim (deskew still applies).

.EXAMPLE
  .\scan_duplex.ps1 -BaseName badge          # 600 dpi duplex, deskew + crop
  .\scan_duplex.ps1 -BaseName doc -Dpi 300   # lower res
#>
param(
  [string]$OutDir   = (Join-Path $env:USERPROFILE 'Downloads'),
  [string]$BaseName = 'duplex',
  [int]$Dpi         = 600,
  [ValidateSet('jpg','png')] [string]$Format = 'jpg',
  [switch]$NoCrop,
  [switch]$NoRotate,  # by default the two faces are rotated to upright landscape (the décimo
                      # feeds short-edge-first, so it scans 90° rotated; front/back are 180° apart).
  [switch]$NoDeskew,  # NAPS2 software deskew is ON by default (décimos are text-dense so it
                      # behaves well); it straightens a skewed feed and the auto-crop then
                      # trims the black corners it introduces. Pass -NoDeskew to disable.
  [string]$Naps2Path         # Explicit path to NAPS2.Console.exe. If omitted, auto-detected
                             # (see Resolve-Naps2 below) so no per-machine edit is needed.
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

# --- locate NAPS2.Console.exe without hardcoding a username ---
# Order: -Naps2Path arg > $env:NAPS2_CONSOLE > per-user portable (USERPROFILE) >
# common install locations. This makes the script portable across machines/users.
function Resolve-Naps2 {
  param([string]$Override)
  $candidates = @(
    $Override,
    $env:NAPS2_CONSOLE,
    (Join-Path $env:USERPROFILE 'Tools\naps2\App\NAPS2.Console.exe'),
    'C:\Program Files\NAPS2\NAPS2.Console.exe',
    'C:\Program Files (x86)\NAPS2\NAPS2.Console.exe'
  ) | Where-Object { $_ }
  foreach ($c in $candidates) { if (Test-Path $c) { return $c } }
  throw ("NAPS2.Console.exe not found. Looked in:`n  " + ($candidates -join "`n  ") +
         "`nInstall the NAPS2 portable zip under %USERPROFILE%\Tools\naps2\ " +
         "or pass -Naps2Path 'C:\path\to\NAPS2.Console.exe'.")
}
$naps2  = Resolve-Naps2 -Override $Naps2Path
$device = 'Plustek MobileOffice A6 Duplex BU'   # D620 TWAIN source (as NAPS2 reports it)
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# --- content-aware crop: trim near-uniform dark border (the scanner feeder edge) ---
function Invoke-AutoCrop {
  param([string]$Path)
  $bmp = New-Object System.Drawing.Bitmap $Path
  try {
    $w = $bmp.Width; $h = $bmp.Height
    $rect = New-Object System.Drawing.Rectangle 0,0,$w,$h
    $data = $bmp.LockBits($rect, [System.Drawing.Imaging.ImageLockMode]::ReadOnly, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $stride = $data.Scan0.ToInt64()
    $bytes = New-Object byte[] ($data.Stride * $h)
    [System.Runtime.InteropServices.Marshal]::Copy([IntPtr]$stride, $bytes, 0, $bytes.Length)
    $bmp.UnlockBits($data)
    $st = $data.Stride
    $darkThresh = 60      # mean luminance below this = dark feeder margin
    $sampleStep = 4       # subsample for speed
    $rowMean = {
      param($y)
      $sum=0; $cnt=0
      for ($x=0; $x -lt $w; $x+=$sampleStep) {
        $o = $y*$st + $x*3
        $sum += ($bytes[$o]*0.114 + $bytes[$o+1]*0.587 + $bytes[$o+2]*0.299); $cnt++
      }
      $sum/$cnt
    }
    $colMean = {
      param($x)
      $sum=0; $cnt=0
      for ($y=0; $y -lt $h; $y+=$sampleStep) {
        $o = $y*$st + $x*3
        $sum += ($bytes[$o]*0.114 + $bytes[$o+1]*0.587 + $bytes[$o+2]*0.299); $cnt++
      }
      $sum/$cnt
    }
    $maxTrimY = [int]($h*0.30); $maxTrimX = [int]($w*0.30)
    $top=0;    while ($top -lt $maxTrimY -and (& $rowMean $top) -lt $darkThresh) { $top++ }
    $bottom=$h-1; while (($h-1-$bottom) -lt $maxTrimY -and (& $rowMean $bottom) -lt $darkThresh) { $bottom-- }
    $left=0;   while ($left -lt $maxTrimX -and (& $colMean $left) -lt $darkThresh) { $left++ }
    $right=$w-1;  while (($w-1-$right) -lt $maxTrimX -and (& $colMean $right) -lt $darkThresh) { $right-- }
    $nw = $right-$left+1; $nh = $bottom-$top+1
    if ($nw -lt $w -or $nh -lt $h) {
      $crop = New-Object System.Drawing.Bitmap $nw,$nh
      $g = [System.Drawing.Graphics]::FromImage($crop)
      $src = New-Object System.Drawing.Rectangle $left,$top,$nw,$nh
      $dst = New-Object System.Drawing.Rectangle 0,0,$nw,$nh
      $g.DrawImage($bmp,$dst,$src,[System.Drawing.GraphicsUnit]::Pixel)
      $g.Dispose()
      $fmt = if ($Path -match '\.png$') { [System.Drawing.Imaging.ImageFormat]::Png } else { [System.Drawing.Imaging.ImageFormat]::Jpeg }
      $bmp.Dispose()
      $crop.Save($Path,$fmt); $crop.Dispose()
      return "$w x $h -> $nw x $nh"
    }
    return "$w x $h (no dark border to trim)"
  } finally { if ($bmp) { $bmp.Dispose() } }
}

# NAPS2 expands $(n) -> 1,2,... for multi-page output (front=1, back=2)
$pattern = Join-Path $OutDir ("{0}_`$(n).{1}" -f $BaseName, $Format)
Get-ChildItem $OutDir -Filter ("{0}_*.{1}" -f $BaseName, $Format) -ErrorAction SilentlyContinue | Remove-Item -Force

$naps2Args = @('-o', $pattern, '--noprofile', '--driver', 'twain', '--device', $device,
               '--source', 'duplex', '--dpi', $Dpi, '--bitdepth', 'color',
               '--jpegquality', '92', '--force')
if (-not $NoDeskew) { $naps2Args += '--deskew' }
Write-Host "Scanning duplex (both sides, one pass) at $Dpi dpi, 24-bit color$(if(-not $NoDeskew){', deskew'})..."
$log = & $naps2 @naps2Args 2>&1
$log | ForEach-Object { Write-Host "  $_" }
if ($log -match 'No scanned pages') {
  Write-Warning "Feeder empty -- load the card and push it in until the light goes SOLID, then rerun."
  return
}
if ($LASTEXITCODE -ne 0) { throw "NAPS2 exited $LASTEXITCODE" }

$files = Get-ChildItem $OutDir -Filter ("{0}_*.{1}" -f $BaseName, $Format) | Sort-Object Name
if ($files.Count -lt 2) {
  Write-Warning "Expected 2 sides, got $($files.Count). Is the card loaded (solid light) and feeding straight?"
}

Write-Host ""
foreach ($f in $files) {
  if (-not $NoCrop) {
    $msg = Invoke-AutoCrop -Path $f.FullName
    Write-Host ("  cropped {0}: {1}" -f $f.Name, $msg)
  }
  if (-not $NoRotate) {
    # Front (_1) needs 90° CCW; back (_2) needs 90° CW — so both read upright landscape.
    $rot = if ($f.Name -match '_1\.') { [System.Drawing.RotateFlipType]::Rotate270FlipNone }
           elseif ($f.Name -match '_2\.') { [System.Drawing.RotateFlipType]::Rotate90FlipNone }
           else { $null }
    if ($rot) {
      $b = New-Object System.Drawing.Bitmap $f.FullName
      $b.RotateFlip($rot)
      $fmt = if ($f.Name -match '\.png$') { [System.Drawing.Imaging.ImageFormat]::Png } else { [System.Drawing.Imaging.ImageFormat]::Jpeg }
      $tmp = [System.IO.Path]::GetTempFileName()
      $b.Save($tmp, $fmt); $b.Dispose()          # release the file handle before overwriting
      Move-Item -Force -LiteralPath $tmp -Destination $f.FullName
      Write-Host ("  rotated {0} upright" -f $f.Name)
    }
  }
}
Write-Host ""
Write-Host "Done. $($files.Count) side(s):"
$files | ForEach-Object {
  $img = [System.Drawing.Image]::FromFile($_.FullName)
  Write-Host ("  {0}  {1}x{2}px  {3:N1} KB" -f $_.FullName,$img.Width,$img.Height,($_.Length/1KB))
  $img.Dispose()
}
$files.FullName
