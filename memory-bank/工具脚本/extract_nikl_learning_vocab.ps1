param(
    [string]$OutputPath,
    [switch]$Refresh
)

$ErrorActionPreference = "Stop"

$taskScriptRoot = $PSScriptRoot
if (-not $taskScriptRoot) {
    $taskScriptRoot = Join-Path (Get-Location).Path "memory-bank\工具脚本"
}
$taskRoot = (Resolve-Path (Join-Path $taskScriptRoot "..\..")).Path
if (-not $OutputPath) {
    $OutputPath = Join-Path $taskRoot "memory-bank\数据文件\topik_ii_nikl_source_snapshot.json"
}

$taskDownloadUrl = "https://www.korean.go.kr/common/download.do?file_path=etcData&c_file_name=5a4a2f5c-66c9-425d-88fb-854289ea2521_0.xls&o_file_name=%ED%95%9C%EA%B5%AD%EC%96%B4%20%ED%95%99%EC%8A%B5%EC%9A%A9%20%EC%96%B4%ED%9C%98%20%EB%AA%A9%EB%A1%9D.xls"
$taskSourcePage = "https://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=71"
$taskReportPage = "https://www.korean.go.kr/front/reportData/reportDataView.do?mn_id=186&report_seq=581"
$taskExpectedSha256 = "DF05D31942DB919668A91234539ED63A200C77F4058A9A135B64C3ED08219475"
$taskXls = Join-Path $env:TEMP "nikl_korean_learning_vocab.xls"
$taskCurriculumPage = "https://www.korean.go.kr/front_eng/down/down_01V.do?report_seq=932"
$taskCurriculumDownloadUrl = "https://www.korean.go.kr/common/download.do?file_path=reportData&c_file_name=157339df-1904-443a-b1a9-d6d34578ba93.xlsx&o_file_name=2017%EB%85%84%20%EA%B5%AD%EC%A0%9C%20%ED%86%B5%EC%9A%A9%20%ED%95%9C%EA%B5%AD%EC%96%B4%20%ED%91%9C%EC%A4%80%20%EA%B5%90%EC%9C%A1%EA%B3%BC%EC%A0%95%20%EC%A0%81%EC%9A%A9%20%EC%97%B0%EA%B5%AC(4%EB%8B%A8%EA%B3%84)%20%EC%96%B4%ED%9C%98,%20%EB%AC%B8%EB%B2%95%20%EB%93%B1%EA%B8%89%20%EB%AA%A9%EB%A1%9D_20180227_20201117%20%EC%88%98%EC%A0%95.xlsx"
$taskCurriculumExpectedSha256 = "2CDE28AB90E04728513E65EF5DF4BAAA400A4055FE2ABD1856889CB983C4C3AC"
$taskCurriculumXlsx = Join-Path $env:TEMP "nikl_2017_standard_curriculum_vocab.xlsx"

if ($Refresh -or -not (Test-Path -LiteralPath $taskXls)) {
    Invoke-WebRequest -UseBasicParsing -Headers @{"User-Agent" = "Mozilla/5.0"} `
        -Uri $taskDownloadUrl -OutFile $taskXls -TimeoutSec 120
}
if ($Refresh -or -not (Test-Path -LiteralPath $taskCurriculumXlsx)) {
    Invoke-WebRequest -UseBasicParsing -Headers @{"User-Agent" = "Mozilla/5.0"} `
        -Uri $taskCurriculumDownloadUrl -OutFile $taskCurriculumXlsx -TimeoutSec 120
}

$taskActualSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskXls).Hash
if ($taskActualSha256 -ne $taskExpectedSha256) {
    throw "国立国语院附件哈希变化，需先人工复核来源。expected=$taskExpectedSha256 actual=$taskActualSha256"
}
$taskCurriculumActualSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskCurriculumXlsx).Hash
if ($taskCurriculumActualSha256 -ne $taskCurriculumExpectedSha256) {
    throw "2017标准课程附件哈希变化，需先人工复核来源。expected=$taskCurriculumExpectedSha256 actual=$taskCurriculumActualSha256"
}

$taskExcel = $null
$taskBook = $null
$taskSheet = $null
$taskCurriculumBook = $null
$taskCurriculumSheet = $null
try {
    $taskExcel = New-Object -ComObject Excel.Application
    $taskExcel.Visible = $false
    $taskExcel.DisplayAlerts = $false
    $taskBook = $taskExcel.Workbooks.Open($taskXls, 0, $true)
    $taskSheet = $taskBook.Worksheets.Item(1)
    $taskValues = $taskSheet.UsedRange.Value2

    $taskHeaders = @("顺位", "词条", "词性", "原语信息", "等级")
    for ($taskCol = 1; $taskCol -le 5; $taskCol++) {
        $taskActualHeader = [string]$taskValues.GetValue(1, $taskCol)
        $taskExpectedHeader = @("순위", "단어", "품사", "풀이", "등급")[$taskCol - 1]
        if ($taskActualHeader -ne $taskExpectedHeader) {
            throw "官方Excel表头变化：第${taskCol}列 expected=$taskExpectedHeader actual=$taskActualHeader"
        }
    }

    $taskWords = New-Object System.Collections.Generic.List[object]
    $taskGradeCounts = @{A = 0; B = 0; C = 0}
    for ($taskRow = 2; $taskRow -le $taskValues.GetLength(0); $taskRow++) {
        $taskEntry = [string]$taskValues.GetValue($taskRow, 2)
        $taskKorean = $taskEntry
        $taskHomonymNo = $null
        if ($taskEntry -match "^(?<base>.+?)(?<number>\d{2})$") {
            $taskKorean = $Matches.base
            $taskHomonymNo = $Matches.number
        }

        $taskGrade = [string]$taskValues.GetValue($taskRow, 5)
        if (-not $taskGradeCounts.ContainsKey($taskGrade)) {
            throw "发现未知等级：row=$taskRow grade=$taskGrade"
        }
        $taskGradeCounts[$taskGrade]++

        $taskWords.Add([ordered]@{
            source_row = $taskRow - 1
            rank = [int]$taskValues.GetValue($taskRow, 1)
            entry = $taskEntry
            korean = $taskKorean
            homonym_no = $taskHomonymNo
            pos_code = [string]$taskValues.GetValue($taskRow, 3)
            origin = [string]$taskValues.GetValue($taskRow, 4)
            grade = $taskGrade
        })
    }

    if ($taskWords.Count -ne 5965) {
        throw "官方词表应为5965条，实际为$($taskWords.Count)条"
    }
    if ($taskGradeCounts.A -ne 982 -or $taskGradeCounts.B -ne 2111 -or $taskGradeCounts.C -ne 2872) {
        throw "官方等级计数异常：$($taskGradeCounts | ConvertTo-Json -Compress)"
    }

    $taskUniqueCount = @($taskWords | ForEach-Object { $_["korean"] } | Sort-Object -Unique).Count
    $taskCurriculumBook = $taskExcel.Workbooks.Open($taskCurriculumXlsx, 0, $true)
    $taskCurriculumSheet = $taskCurriculumBook.Worksheets.Item("어휘")
    $taskCurriculumValues = $taskCurriculumSheet.UsedRange.Value2
    $taskCurriculumExpectedHeaders = @("전체 번호", "등급별 번호", "등급", "어휘", "품사", "길잡이말", "어휘교육내용개발(1-4단계)", "등급")
    for ($taskCol = 1; $taskCol -le 8; $taskCol++) {
        $taskActualHeader = [string]$taskCurriculumValues.GetValue(1, $taskCol)
        $taskExpectedHeader = $taskCurriculumExpectedHeaders[$taskCol - 1]
        if ($taskActualHeader -ne $taskExpectedHeader) {
            throw "2017标准课程Excel表头变化：第${taskCol}列 expected=$taskExpectedHeader actual=$taskActualHeader"
        }
    }

    $taskCurriculumWords = New-Object System.Collections.Generic.List[object]
    $taskCurriculumGradeCounts = @{"1급" = 0; "2급" = 0; "3급" = 0; "4급" = 0; "5급" = 0; "6급" = 0}
    for ($taskRow = 2; $taskRow -le $taskCurriculumValues.GetLength(0); $taskRow++) {
        $taskEntry = [string]$taskCurriculumValues.GetValue($taskRow, 4)
        $taskKorean = $taskEntry
        $taskHomonymNo = $null
        if ($taskEntry -match "^(?<base>.+?)(?<number>\d{2})$") {
            $taskKorean = $Matches.base
            $taskHomonymNo = $Matches.number
        }

        $taskGrade = [string]$taskCurriculumValues.GetValue($taskRow, 3)
        if (-not $taskCurriculumGradeCounts.ContainsKey($taskGrade)) {
            throw "2017标准课程发现未知等级：row=$taskRow grade=$taskGrade"
        }
        $taskCurriculumGradeCounts[$taskGrade]++

        $taskCurriculumWords.Add([ordered]@{
            source_row = $taskRow - 1
            overall_no = [int]$taskCurriculumValues.GetValue($taskRow, 1)
            level_no = [int]$taskCurriculumValues.GetValue($taskRow, 2)
            grade = $taskGrade
            entry = $taskEntry
            korean = $taskKorean
            homonym_no = $taskHomonymNo
            pos = [string]$taskCurriculumValues.GetValue($taskRow, 5)
            guide = [string]$taskCurriculumValues.GetValue($taskRow, 6)
            prior_stage = [string]$taskCurriculumValues.GetValue($taskRow, 7)
            confirmed_grade = [string]$taskCurriculumValues.GetValue($taskRow, 8)
        })
    }

    if ($taskCurriculumWords.Count -ne 10635) {
        throw "2017标准课程词表应为10635条，实际为$($taskCurriculumWords.Count)条"
    }
    $taskExpectedCurriculumCounts = @{"1급" = 735; "2급" = 1100; "3급" = 1655; "4급" = 2200; "5급" = 2365; "6급" = 2580}
    foreach ($taskGrade in $taskExpectedCurriculumCounts.Keys) {
        if ($taskCurriculumGradeCounts[$taskGrade] -ne $taskExpectedCurriculumCounts[$taskGrade]) {
            throw "2017标准课程等级计数异常：grade=$taskGrade expected=$($taskExpectedCurriculumCounts[$taskGrade]) actual=$($taskCurriculumGradeCounts[$taskGrade])"
        }
    }
    $taskCurriculumUniqueCount = @($taskCurriculumWords | ForEach-Object { $_["korean"] } | Sort-Object -Unique).Count

    $taskPayload = [ordered]@{
        status = "official_source_snapshot_not_final_wordbook"
        retrieved_at = "2026-08-01"
        source = [ordered]@{
            name = "韩国国立国语院《韩国语学习用词汇目录》"
            organization = "국립국어원"
            source_page = $taskSourcePage
            report_page = $taskReportPage
            download_url = $taskDownloadUrl
            file_sha256 = $taskActualSha256
            source_note = "官方韩国语学习者词汇分级，不是TOPIK官方逐词考纲"
        }
        raw_total = $taskWords.Count
        unique_korean_after_homonym_suffix_removal = $taskUniqueCount
        grade_counts = [ordered]@{A = $taskGradeCounts.A; B = $taskGradeCounts.B; C = $taskGradeCounts.C}
        headers_cn = $taskHeaders
        words = $taskWords
        standard_curriculum_source = [ordered]@{
            name = "韩国国立国语院《2017国际通用韩国语标准教育课程应用研究（第4阶段）》词汇等级目录"
            organization = "국립국어원"
            source_page = $taskCurriculumPage
            download_url = $taskCurriculumDownloadUrl
            file_sha256 = $taskCurriculumActualSha256
            source_note = "官方韩国语标准课程1-6级词汇分级，不是TOPIK官方逐词考纲；附件于2020-11-17修订"
        }
        standard_curriculum_raw_total = $taskCurriculumWords.Count
        standard_curriculum_unique_korean_after_homonym_suffix_removal = $taskCurriculumUniqueCount
        standard_curriculum_grade_counts = [ordered]@{
            "1급" = $taskCurriculumGradeCounts["1급"]
            "2급" = $taskCurriculumGradeCounts["2급"]
            "3급" = $taskCurriculumGradeCounts["3급"]
            "4급" = $taskCurriculumGradeCounts["4급"]
            "5급" = $taskCurriculumGradeCounts["5급"]
            "6급" = $taskCurriculumGradeCounts["6급"]
        }
        standard_curriculum_words = $taskCurriculumWords
    }

    $taskOutputDir = Split-Path -Parent $OutputPath
    if (-not (Test-Path -LiteralPath $taskOutputDir)) {
        New-Item -ItemType Directory -Path $taskOutputDir | Out-Null
    }
    $taskJson = $taskPayload | ConvertTo-Json -Depth 8
    [IO.File]::WriteAllText($OutputPath, $taskJson + "`n", (New-Object Text.UTF8Encoding($false)))

    Write-Output "output=$OutputPath"
    Write-Output "raw_total=$($taskWords.Count)"
    Write-Output "unique_korean=$taskUniqueCount"
    Write-Output "grades=A:$($taskGradeCounts.A),B:$($taskGradeCounts.B),C:$($taskGradeCounts.C)"
    Write-Output "sha256=$taskActualSha256"
    Write-Output "standard_curriculum_raw_total=$($taskCurriculumWords.Count)"
    Write-Output "standard_curriculum_unique_korean=$taskCurriculumUniqueCount"
    Write-Output "standard_curriculum_grades=1:$($taskCurriculumGradeCounts['1급']),2:$($taskCurriculumGradeCounts['2급']),3:$($taskCurriculumGradeCounts['3급']),4:$($taskCurriculumGradeCounts['4급']),5:$($taskCurriculumGradeCounts['5급']),6:$($taskCurriculumGradeCounts['6급'])"
    Write-Output "standard_curriculum_sha256=$taskCurriculumActualSha256"
}
finally {
    if ($taskCurriculumBook) { $taskCurriculumBook.Close($false) }
    if ($taskBook) { $taskBook.Close($false) }
    if ($taskExcel) { $taskExcel.Quit() }
    if ($taskCurriculumSheet) { [Runtime.InteropServices.Marshal]::ReleaseComObject($taskCurriculumSheet) | Out-Null }
    if ($taskCurriculumBook) { [Runtime.InteropServices.Marshal]::ReleaseComObject($taskCurriculumBook) | Out-Null }
    if ($taskSheet) { [Runtime.InteropServices.Marshal]::ReleaseComObject($taskSheet) | Out-Null }
    if ($taskBook) { [Runtime.InteropServices.Marshal]::ReleaseComObject($taskBook) | Out-Null }
    if ($taskExcel) { [Runtime.InteropServices.Marshal]::ReleaseComObject($taskExcel) | Out-Null }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
