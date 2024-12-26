# Polaris API 完整使用指南

## 一、環境變數設置

### 1.1 基本變數設置
```bash
# API 設定
export BASE_URL="https://poc.polaris.blackduck.com"
export API_TOKEN="s4jpgckfat47f3dcaebrc486lj8aft8d2974e3t8usg8ku3lhnd0rgb6944o5kru05ti0mac4o50i"

# Portfolio 結構 IDs
export PORTFOLIO_ID="8ad7aaa9-dc3b-4ced-a0b0-8ef308dfef6f"
export PORTFOLIO_ITEM_ID_APPLICATION="4577667b-1d49-4099-b0a9-bb33c48195da"  # Application ID
export PORTFOLIO_SUBITEM_ID_PROJECT="19e77822-f26e-4766-bc97-65133299fa1f"   # Project ID
export BRANCH_ID="1ee9e0e8-57f8-47d3-ab2f-7d5b1546c2d1"

# Issue IDs
export ISSUE_ID1="1efa0a52-89c8-6945-8dbc-6bdb69a02101"      
export ISSUE_ID2="1efa0a52-89c8-6946-8dbc-fbd08d163d21"      
```

### 1.2 動態獲取 Issue IDs

```bash
# 獲取單個 Issue ID
export ISSUE_ID=$(curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=1" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" | \
  jq -r '._items[0].id')

# 確認變量設置
echo "ISSUE_ID: $ISSUE_ID"

# 獲取多個 Issue IDs
export ISSUE_IDS=$(curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=5" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" | \
  jq -r '._items[].id')

# 在 zsh 中設置陣列
export ISSUE_ID_ARRAY=("${(@f)ISSUE_IDS}")
export ISSUE_ID1="${ISSUE_ID_ARRAY[1]}"  # zsh 陣列索引從 1 開始
export ISSUE_ID2="${ISSUE_ID_ARRAY[2]}"
```

### 1.3 動態獲取 Occurrence IDs

```bash
# 獲取單個 Occurrence ID
export OCCURRENCE_ID=$(curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/occurrences?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=1" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" | \
  jq -r '._items[0].id')

echo "OCCURRENCE_ID: $OCCURRENCE_ID"

# 獲取多個 Occurrence IDs
export OCCURRENCE_IDS=$(curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/occurrences?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=5" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" | \
  jq -r '._items[].id')

export OCCURRENCE_ID_ARRAY=("${(@f)OCCURRENCE_IDS}")
export OCCURRENCE_ID1="${OCCURRENCE_ID_ARRAY[1]}"
export OCCURRENCE_ID2="${OCCURRENCE_ID_ARRAY[2]}"
```

## 二、API 使用指南

### 2.1 Portfolio 管理

#### 2.1.1 獲取 Portfolio 列表
```bash
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/portfolio/portfolios" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.portfolio-1+json" | jq
```

#### 2.1.2 獲取 Portfolio Items (Applications)
```bash
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/portfolio/portfolios/$PORTFOLIO_ID/portfolio-items" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.portfolio-items-1+json" \
  -G \
  --data-urlencode "_offset=0" \
  --data-urlencode "_limit=100" | jq
```

#### 2.1.3 按名稱過濾應用程序
```bash
export APP_FILTER=allenl_applications

curl -s --fail --compressed \
  -X GET "$BASE_URL/api/portfolio/portfolios/$PORTFOLIO_ID/portfolio-items" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.portfolio-items-1+json" \
  -G \
  --data-urlencode "_offset=0" \
  --data-urlencode "_limit=100" \
  --data-urlencode "name=$APP_FILTER" | jq
```

### 2.2 Branch 管理

#### 2.2.1 獲取所有分支
```bash
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID_PROJECT/branches" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.branches-1+json" | jq
```

#### 2.2.2 按分支名稱過濾
```bash
export BRANCH_FILTER="main"
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID_PROJECT/branches" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.branches-1+json" \
  -G \
  --data-urlencode "name=$BRANCH_FILTER" | jq
```

### 2.3 Issue 管理

#### 2.3.1 查詢 Issue（完整參數版本）
```bash
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -H "Accept-Language: en-US" \
  -G \
  --data-urlencode "_first=1" \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "branchId=$BRANCH_ID" \
  --data-urlencode "testId=latest" \
  --data-urlencode "_sort=occurrence:severity|desc" \
  --data-urlencode "_filter=occurrence:severity=='high'" \
  --data-urlencode "_includeType=true" \
  --data-urlencode "_includeOccurrenceProperties=true" \
  --data-urlencode "_includeTriageProperties=true" \
  --data-urlencode "_includeFirstDetectedOn=true" \
  --data-urlencode "_includeContext=true" | jq

curl 基本參數

-s: (silent) 不顯示進度條和錯誤信息
--fail: 在 HTTP 錯誤時立即終止
--compressed: 支持壓縮傳輸
-X GET: 指定 HTTP 方法為 GET
-G: 將數據附加到 URL 上而不是通過 POST 傳送
-H: 設置 HTTP 標頭

HTTP 標頭參數

Api-Token: API 認證令牌
Accept: 指定接受的回應格式為 Polaris findings issues JSON 格式
Accept-Language: 指定響應使用的語言為英文

查詢參數 (URL Parameters)

projectId: 指定要查詢的專案 ID
branchId: 指定要查詢的分支 ID
testId=latest: 只包含最新測試中檢測到的問題

排序和過濾參數

_sort=occurrence:severity|desc: 按嚴重性降序排序
_filter=occurrence:severity=='high': 只顯示高嚴重性的問題

--data-urlencode 是 curl 的參數：
用於對數據進行 URL 編碼
確保特殊字符能被正確傳輸
會自動將參數加到 URL 查詢字串中

包含附加資訊的參數

_includeType=true: 包含問題類型資訊
_includeOccurrenceProperties=true: 包含問題屬性資訊
_includeTriageProperties=true: 包含分類狀態資訊
_includeFirstDetectedOn=true: 包含首次檢測時間
_includeContext=true: 包含問題上下文資訊

輸出處理

| jq: 使用 jq 工具格式化 JSON 輸出
```

#### 2.3.2 使用 RSQL 查詢多個 Issues
```bash
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "_filter=occurrence:issue-id=in=($ISSUE_ID1,$ISSUE_ID2)" \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_includeProperties=true" \
  --data-urlencode "_includeType=true" | jq
```

### 2.4 Occurrence 管理

#### 2.4.1 獲取 Occurrence 列表
```bash
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/occurrences" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_first=100" | jq
```

#### 2.4.2 獲取 Occurrence 程式碼片段
```bash
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/occurrences/$OCCURRENCE_ID/snippet" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" | jq
```

#### 2.4.3 獲取 AI 修復建議
```bash
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/occurrences/$OCCURRENCE_ID/assist" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" | jq
```

## 三、進階使用技巧

### 3.1 分頁查詢

```bash
# 首次查詢
export NEXT_CURSOR=$(curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=100" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" | \
  jq -r '._links[] | select(.rel=="next") | .href | capture(".*_cursor=(?<cursor>[^&]*).*").cursor')

# 使用 cursor 進行下一頁查詢
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_first=100" \
  --data-urlencode "_cursor=$NEXT_CURSOR" | jq
```

### 3.2 複雜 RSQL 查詢

```bash
先只查詢所有問題，看看實際的值：
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_includeOccurrenceProperties=true" \
  --data-urlencode "_includeTriageProperties=true" \
  --data-urlencode "_first=1" | jq '.'

從輸出結果可以看到正確的值：

severity 是在 occurrenceProperties 中：
"key": "severity", "value": "medium"
所以值是小寫：medium, high, critical
language 也在 occurrenceProperties 中：
"key": "language", "value": "JavaScript"
所以語言首字母需要大寫：JavaScript, Java
triage status 在 triageProperties 中：
"key": "status", "value": "not-dismissed"
"key": "dismissal-reason", "value": "unset"



所以正確的查詢應該是：
# 組合多個條件的查詢
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "_filter=occurrence:severity=='medium';occurrence:language=='Java';triage:status=='not-dismissed'" \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_includeOccurrenceProperties=true" \
  --data-urlencode "_includeTriageProperties=true" | jq
```

## 四、最佳實踐

### 4.1 錯誤處理
- 使用 --fail 參數確保在 HTTP 錯誤時終止
- 使用 --compressed 支持壓縮傳輸
- 使用 -s 參數減少不必要的輸出
- 設置合適的超時參數

### 4.2 性能優化
- 合理使用分頁參數
- 使用精確的過濾條件
- 只請求必要的字段和屬性
- 適當使用壓縮傳輸

### 4.3 安全性考慮
- 不要在腳本中硬編碼 API Token
- 使用 HTTPS 進行所有 API 調用
- 定期更換 API Token
- 避免暴露敏感資訊

四,其他技巧
根據 Findings_GET.txt 文件，我們有幾種方式可以找到所有可能的值：

1. 透過 API 查詢所有資料，然後用 jq 來過濾出所有可能的值：

```bash
# 查詢 severity 的所有可能值
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_includeOccurrenceProperties=true" \
  --data-urlencode "_first=100" | \
  jq '[._items[].occurrenceProperties[] | select(.key=="severity").value] | unique'

# 查詢 language 的所有可能值
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_includeOccurrenceProperties=true" \
  --data-urlencode "_first=100" | \
  jq '[._items[].occurrenceProperties[] | select(.key=="language").value] | unique'

# 查詢 triage status 的所有可能值
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_includeTriageProperties=true" \
  --data-urlencode "_first=100" | \
  jq '[._items[].triageProperties[] | select(.key=="status").value] | unique'
```

2. 使用 count API 加上分組功能：

```bash
# 按 severity 分組計數
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues/_actions/count" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_group=occurrence:severity" | jq '._items'

# 按 language 分組計數
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues/_actions/count" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_group=occurrence:language" | jq '._items'

# 按 triage status 分組計數
curl -s --fail --compressed \
  -X GET "$BASE_URL/api/findings/issues/_actions/count" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_group=triage:status" | jq '._items'
```

這兩種方法都可以幫助你找到所有可能的值：
- 第一種方法會直接列出實際存在的所有不同值
- 第二種方法會同時給你每個值的計數，讓你知道有多少個問題屬於每個分類

建議都試試看，這樣可以更全面地了解你的專案中實際使用的值。