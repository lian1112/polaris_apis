# Polaris Findings API - 其他端點

## 環境變數設置
```bash
# 基本設置
export API_TOKEN="your-api-token"
export BASE_URL="https://poc.polaris.blackduck.com"
export PROJECT_ID="your-project-id"

# 其他ID
export OCCURRENCE_ID="your-occurrence-id"
export LICENSE_ID="your-license-id"
export TAXON_ID="your-taxon-id"
export ARTIFACT_ID="your-artifact-id"
```

## Occurrences端點

### 獲取Occurrences列表
```bash
curl -X GET "$BASE_URL/api/findings/occurrences" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" \
  -G \
  --data-urlencode "_includeDescendants=true" \
  --data-urlencode "_includeOnlyStandards=true"
```

## 常用參數說明

### Occurrence參數
- `_includeProperties`: 包含屬性信息
- `_includeType`: 包含類型信息
- `applicationId`: 應用程式ID（可選）
- `projectId`: 專案ID（可選）

### License參數
- `_includeLicenseText`: 包含許可證文本
- `projectId`: 專案ID（用於過濾）

### Taxa參數
- `_includeDescendants`: 是否包含所有後代而不僅是子分類
- `_includeOnlyStandards`: 是否只包含標準過濾器（如OWASP）

## 響應格式
- Issues相關：`application/vnd.polaris.findings.issues-1+json`
- Occurrences相關：`application/vnd.polaris.findings.occurrences-1+json`
- Licenses相關：`application/vnd.polaris.findings.licenses-1+json`
- Taxa相關：`application/vnd.polaris.findings.taxa-1+json`
- 製品（artifacts）：`text/plain`deProperties=true" \
  --data-urlencode "_includeType=true" \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取單個Occurrence
```bash
curl -X GET "$BASE_URL/api/findings/occurrences/$OCCURRENCE_ID" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" \
  -G \
  --data-urlencode "_includeProperties=true" \
  --data-urlencode "_includeType=true" \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Occurrence代碼片段
```bash
curl -X GET "$BASE_URL/api/findings/occurrences/$OCCURRENCE_ID/snippet" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" \
  -G \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Occurrence AI輔助
```bash
curl -X GET "$BASE_URL/api/findings/occurrences/$OCCURRENCE_ID/assist" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.occurrences-1+json" \
  -G \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Occurrence製品
```bash
curl -X GET "$BASE_URL/api/findings/occurrences/$OCCURRENCE_ID/artifacts/$ARTIFACT_ID" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: text/plain" \
  -G \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

## Licenses端點

### 獲取單個License
```bash
curl -X GET "$BASE_URL/api/findings/licenses/$LICENSE_ID" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.licenses-1+json" \
  -G \
  --data-urlencode "_includeLicenseText=true"
```

### 獲取Licenses列表
```bash
curl -X GET "$BASE_URL/api/findings/licenses" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.licenses-1+json" \
  -G \
  --data-urlencode "_includeLicenseText=true" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 統計Licenses
```bash
curl -X GET "$BASE_URL/api/findings/licenses/_actions/count" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.licenses-1+json" \
  -G \
  --data-urlencode "projectId=$PROJECT_ID"
```

## Taxa端點

### 獲取單個Taxon
```bash
curl -X GET "$BASE_URL/api/findings/taxa/$TAXON_ID" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.taxa-1+json"
```

### 獲取Taxon的子分類
```bash
curl -X GET "$BASE_URL/api/findings/taxa/$TAXON_ID/subtaxa" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.taxa-1+json"
```

### 獲取Taxon的Issue類型
```bash
curl -X GET "$BASE_URL/api/findings/taxa/$TAXON_ID/issue-types" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.taxa-1+json"
```

### 獲取Taxonomies
```bash
curl -X GET "$BASE_URL/api/findings/taxonomies" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.taxonomies-1+json" \
  -G \
  --data-urlencode "_inclu