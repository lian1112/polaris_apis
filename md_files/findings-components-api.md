# Polaris Findings API - Components端點

## 環境變數設置
```bash
# 基本設置
export API_TOKEN="your-api-token"
export BASE_URL="https://poc.polaris.blackduck.com"
export PROJECT_ID="your-project-id"

# Component相關ID
export VERSION_ID="your-version-id"
export ORIGIN_ID="your-origin-id"
```

## Component Version端點

### 獲取Component Versions列表
```bash
curl -X GET "$BASE_URL/api/findings/component-versions" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.component-versions-1+json" \
  -G \
  --data-urlencode "projectId=$PROJECT_ID" \
  --data-urlencode "_includeComponent=true" \
  --data-urlencode "_includeLicense=true"
```

### 獲取單個Component Version
```bash
curl -X GET "$BASE_URL/api/findings/component-versions/$VERSION_ID" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.component-versions-1+json" \
  -G \
  --data-urlencode "projectId=$PROJECT_ID" \
  --data-urlencode "_includeComponent=true" \
  --data-urlencode "_includeLicense=true"
```

### 統計Component Versions
```bash
curl -X GET "$BASE_URL/api/findings/component-versions/_actions/count" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.component-versions-1+json" \
  -G \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Component Version分類歷史
```bash
curl -X GET "$BASE_URL/api/findings/component-versions/$VERSION_ID/triage-history" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.component-versions-1+json" \
  -G \
  --data-urlencode "projectId=$PROJECT_ID"
```

## Component Origin端點

### 獲取單個Component Origin
```bash
curl -X GET "$BASE_URL/api/findings/component-origins/$ORIGIN_ID" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.component-origins-1+json" \
  -G \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Component Origins列表
```bash
curl -X GET "$BASE_URL/api/findings/component-origins" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.component-origins-1+json" \
  -G \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Component Origin匹配
```bash
curl -X GET "$BASE_URL/api/findings/component-origins/$ORIGIN_ID/matches" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.component-origins-1+json" \
  -G \
  --data-urlencode "projectId=$PROJECT_ID"
```

## 常用參數說明

1. `projectId`: 專案ID，大多數請求都需要提供
2. `_includeComponent`: 是否包含組件詳細信息
3. `_includeLicense`: 是否包含許可證信息
4. API響應格式統一為JSON
5. 所有請求都需要API Token驗證