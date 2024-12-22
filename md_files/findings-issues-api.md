# Polaris Findings API - Issues端點

## 環境變數設置
```bash
# 基本設置
export API_TOKEN="your-api-token"
export BASE_URL="https://poc.polaris.blackduck.com"

# 可選ID
export APPLICATION_ID="your-application-id"
export PROJECT_ID="your-project-id"
export ISSUE_ID="your-issue-id"
```

## Issues端點

### 獲取單個Issue
```bash
curl -X GET "$BASE_URL/api/findings/issues/$ISSUE_ID" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "_includeType=true" \
  --data-urlencode "_includeOccurrenceProperties=true" \
  --data-urlencode "_includeTriageProperties=true" \
  --data-urlencode "_includeFirstDetectedOn=true" \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Issues列表
```bash
curl -X GET "$BASE_URL/api/findings/issues" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "_includeType=true" \
  --data-urlencode "_includeOccurrenceProperties=true" \
  --data-urlencode "_includeTriageProperties=true" \
  --data-urlencode "_first=100" \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Issue分類歷史
```bash
curl -X GET "$BASE_URL/api/findings/issues/$ISSUE_ID/triage-history" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 獲取Issue檢測歷史
```bash
curl -X GET "$BASE_URL/api/findings/issues/$ISSUE_ID/detection-history" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 統計Issues
```bash
curl -X GET "$BASE_URL/api/findings/issues/_actions/count" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "_includeAverageAge=true" \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID"
```

### 統計Issues隨時間變化
```bash
# 額外的環境變數
export LAST_DAYS="30"
export FROM_DATE="2024-01-01"
export TO_DATE="2024-12-31"

curl -X GET "$BASE_URL/api/findings/issues/_actions/count-over-time" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID" \
  --data-urlencode "_lastXDays=$LAST_DAYS" \
  --data-urlencode "_fromDate=$FROM_DATE" \
  --data-urlencode "_toDate=$TO_DATE"
```

### 導出Issues
```bash
export FILE_NAME="issues-export.csv"

curl -X GET "$BASE_URL/api/findings/issues/_actions/export" \
  -H "Api-Token: $API_TOKEN" \
  -H "Accept: application/vnd.polaris.findings.issues-1+json" \
  -G \
  --data-urlencode "applicationId=$APPLICATION_ID" \
  --data-urlencode "projectId=$PROJECT_ID" \
  --data-urlencode "fileName=$FILE_NAME"
```