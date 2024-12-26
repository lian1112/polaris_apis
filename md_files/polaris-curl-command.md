# Polaris API 使用指南

## 環境變數設置

### 基本變數設置
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

### 動態獲取 Issue IDs 與 Occurrence IDs

#### 獲取 Issue IDs
```bash
# 獲取單個 Issue ID
export ISSUE_ID=$(curl -X GET "$BASE_URL/api/findings/issues?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=1" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" | \
  jq -r '._items[0].id')

# 確認變量已經設置
echo "ISSUE_ID: $ISSUE_ID"

# 獲取多個 Issue IDs
export ISSUE_IDS=$(curl -X GET "$BASE_URL/api/findings/issues?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=5" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" | \
  jq -r '._items[].id')

# 在 zsh 中設置陣列
export ISSUE_ID_ARRAY=("${(@f)ISSUE_IDS}")

# 設置獨立變量
export ISSUE_ID1="${ISSUE_ID_ARRAY[1]}"  # zsh 陣列索引從 1 開始
export ISSUE_ID2="${ISSUE_ID_ARRAY[2]}"

# 確認變量設置
echo "ISSUE_ID1: $ISSUE_ID1"
echo "ISSUE_ID2: $ISSUE_ID2"
```

#### 獲取 Occurrence IDs
```bash
# 獲取單個 Occurrence ID
export OCCURRENCE_ID=$(curl -X GET "$BASE_URL/api/findings/occurrences?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=1" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" | \
  jq -r '._items[0].id')

# 確認變量已經設置
echo "OCCURRENCE_ID: $OCCURRENCE_ID"

# 獲取多個 Occurrence IDs
export OCCURRENCE_IDS=$(curl -X GET "$BASE_URL/api/findings/occurrences?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=5" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" | \
  jq -r '._items[].id')

# 在 zsh 中設置陣列
export OCCURRENCE_ID_ARRAY=("${(@f)OCCURRENCE_IDS}")

# 設置獨立變量
export OCCURRENCE_ID1="${OCCURRENCE_ID_ARRAY[1]}"  # zsh 陣列索引從 1 開始
export OCCURRENCE_ID2="${OCCURRENCE_ID_ARRAY[2]}"

# 確認變量設置
echo "OCCURRENCE_ID1: $OCCURRENCE_ID1"
echo "OCCURRENCE_ID2: $OCCURRENCE_ID2"
```

## API 使用指南

### 1. 獲取 Portfolio ID
```bash
curl -X GET "$BASE_URL/api/portfolio/portfolios" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.portfolio-1+json" | jq
```

### 2. 獲取 Portfolio Items (Applications)
```bash
curl -X GET "$BASE_URL/api/portfolio/portfolios/$PORTFOLIO_ID/portfolio-items?_offset=0&_limit=100" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.portfolio-items-1+json" | jq
```

### 3. 獲取特定應用程序
```bash
export APP_FILTER=allenl_applications

curl -X GET "$BASE_URL/api/portfolio/portfolios/$PORTFOLIO_ID/portfolio-items?_offset=0&_limit=100&name=$APP_FILTER" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.portfolio-items-1+json" | jq
```

### 4. 獲取特定項目
```bash
export PROJECT_FILTER=WebGoat

curl -X GET "$BASE_URL/api/portfolio/portfolio-items/$PORTFOLIO_ITEM_ID_APPLICATION/portfolio-sub-items?_offset=0&_limit=100&name=$PROJECT_FILTER" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.portfolio-subitems-1+json" | jq
```

### 5. 分支管理

#### 5.1 使用分支名稱過濾獲取分支
```bash
curl -X GET "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID_PROJECT/branches?name=main" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.branches-1+json" | jq
```

#### 5.2 獲取所有分支
```bash
curl -X GET "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID_PROJECT/branches" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.branches-1+json" | jq
```

#### 5.3 按分支名稱過濾
```bash
export BRANCH_FILTER="main"
curl -X GET "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID_PROJECT/branches?name=$BRANCH_FILTER" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.pm.branches-1+json" | jq
```

### 6. 問題管理

#### 6.1 獲取 Issue 列表
```bash
# 獲取所有 Issues
curl -X GET "$BASE_URL/api/findings/issues?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=100" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" | jq
```

#### 6.2 獲取特定 Issue 的詳細資訊（包含 Occurrence 資訊）
```bash
curl -X GET "$BASE_URL/api/findings/issues/$ISSUE_ID1?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_includeOccurrenceProperties=true" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" | jq
```

#### 6.3 獲取 Occurrence 列表
```bash
# 獲取前100個 Occurrences
curl -X GET "$BASE_URL/api/findings/occurrences?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=100" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" | jq
```

#### 6.4 獲取特定 Occurrence 的程式碼片段
```bash
# 獲取特定 Occurrence 的程式碼片段
curl -X GET "$BASE_URL/api/findings/occurrences/$OCCURRENCE_ID/snippet?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" | jq
```

#### 6.5 獲取特定 Occurrence 的AI輔助修復建議
```bash
curl -X GET "$BASE_URL/api/findings/occurrences/$OCCURRENCE_ID/assist?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" | jq
```

### 7. 分頁和過濾

#### 7.1 分頁獲取問題
```bash
# 使用 cursor 參數進行分頁
curl -X GET "$BASE_URL/api/findings/occurrences?projectId=$PORTFOLIO_SUBITEM_ID_PROJECT&_first=100&_cursor=YOUR_CURSOR" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" | jq
```

#### 7.2 按問題ID過濾
```bash
# 使用 RSQL 過濾多個 Issues
curl -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "_filter=occurrence:issue-id=in=($ISSUE_ID1,$ISSUE_ID2)" \
  --data-urlencode "projectId=$PORTFOLIO_SUBITEM_ID_PROJECT" \
  --data-urlencode "_includeProperties=true" \
  --data-urlencode "_includeType=true" | jq
```