#!/bin/bash

# 設置預設值和說明
usage() {
    echo "使用方式: $0 [-t API_TOKEN] [-u BASE_URL] [-a APP_NAME] [-p PROJECT_NAME] [-b BRANCH_NAME]"
    echo "  -t: API Token"
    echo "  -u: Base URL (預設: https://poc.polaris.blackduck.com)"
    echo "  -a: Application名稱過濾"
    echo "  -p: Project名稱過濾"
    echo "  -b: Branch名稱過濾"
    echo "  -h: 顯示此說明"
    exit 1
}

# 預設值
BASE_URL="https://poc.polaris.blackduck.com"
API_TOKEN=""
APP_FILTER=""
PROJECT_FILTER=""
BRANCH_FILTER=""

# 解析命令行參數
while getopts "t:u:a:p:b:h" opt; do
    case $opt in
        t) API_TOKEN="$OPTARG" ;;
        u) BASE_URL="$OPTARG" ;;
        a) APP_FILTER="$OPTARG" ;;
        p) PROJECT_FILTER="$OPTARG" ;;
        b) BRANCH_FILTER="$OPTARG" ;;
        h) usage ;;
        ?) usage ;;
    esac
done

# 檢查必要參數
if [ -z "$API_TOKEN" ]; then
    echo "錯誤: 必須提供 API Token"
    usage
fi

# 創建輸出目錄和curl命令文件
OUTPUT_DIR="polaris_output"
mkdir -p "$OUTPUT_DIR"
CURL_FILE="$OUTPUT_DIR/curl_commands.txt"
ID_FILE="$OUTPUT_DIR/id_variables.txt"

# 清空或創建文件
echo "# Polaris API Curl Commands" > "$CURL_FILE"
echo "# Polaris API ID Variables" > "$ID_FILE"

# 記錄環境變數
echo "# Environment Variables" >> "$ID_FILE"
echo "export BASE_URL=\"$BASE_URL\"" >> "$ID_FILE"
echo "export API_TOKEN=\"$API_TOKEN\"" >> "$ID_FILE"
echo "" >> "$ID_FILE"

# Common headers for curl
COMMON_HEADERS=(
    -H "Api-Token: $API_TOKEN"
)

print_curl_command() {
    local url="$1"
    local accept_header="$2"
    local description="$3"
    
    # 輸出到螢幕
    echo "=== $description ==="
    echo "curl -X GET \"$url\" \\"
    echo "  -H \"Api-Token: $API_TOKEN\" \\"
    echo "  -H \"Accept: $accept_header\""
    echo
    
    # 替換變數為實際值
    local actual_url=$(eval echo "$url")
    
    # 輸出到文件
    echo "# $description" >> "$CURL_FILE"
    echo "# Current Variables:" >> "$CURL_FILE"
    echo "export BASE_URL=\"$BASE_URL\"" >> "$CURL_FILE"
    echo "export API_TOKEN=\"$API_TOKEN\"" >> "$CURL_FILE"
    
    # 根據當前步驟輸出相應的ID變數
    if [ ! -z "$PORTFOLIO_ID" ]; then
        echo "export PORTFOLIO_ID=\"$PORTFOLIO_ID\"" >> "$CURL_FILE"
    fi
    if [ ! -z "$PORTFOLIO_ITEM_ID" ]; then
        echo "export PORTFOLIO_ITEM_ID=\"$PORTFOLIO_ITEM_ID\"" >> "$CURL_FILE"
    fi
    if [ ! -z "$PORTFOLIO_SUBITEM_ID" ]; then
        echo "export PORTFOLIO_SUBITEM_ID=\"$PORTFOLIO_SUBITEM_ID\"" >> "$CURL_FILE"
    fi
    if [ ! -z "$BRANCH_ID" ]; then
        echo "export BRANCH_ID=\"$BRANCH_ID\"" >> "$CURL_FILE"
    fi
    echo "" >> "$CURL_FILE"
    
    # 輸出curl命令（帶變數）
    echo "# Command with variables:" >> "$CURL_FILE"
    echo "curl -X GET \"$url\" \\" >> "$CURL_FILE"
    echo "  -H \"Api-Token: \$API_TOKEN\" \\" >> "$CURL_FILE"
    echo "  -H \"Accept: $accept_header\"" >> "$CURL_FILE"
    echo "" >> "$CURL_FILE"
    
    # 輸出實際的curl命令
    echo "# Actual command:" >> "$CURL_FILE"
    echo "curl -X GET \"$actual_url\" \\" >> "$CURL_FILE"
    echo "  -H \"Api-Token: $API_TOKEN\" \\" >> "$CURL_FILE"
    echo "  -H \"Accept: $accept_header\"" >> "$CURL_FILE"
    echo "" >> "$CURL_FILE"
    
    # 分隔線
    echo "# -------------------------------------------" >> "$CURL_FILE"
    echo "" >> "$CURL_FILE"
}

# 記錄初始環境設置
echo "# Initial Environment Setup" > "$CURL_FILE"
echo "export BASE_URL=\"$BASE_URL\"" >> "$CURL_FILE"
echo "export API_TOKEN=\"$API_TOKEN\"" >> "$CURL_FILE"
echo "" >> "$CURL_FILE"
echo "# -------------------------------------------" >> "$CURL_FILE"
echo "" >> "$CURL_FILE"
# Step 1: Get Portfolio ID
echo "Step 1: Getting Portfolio ID..."

print_curl_command \
    "$BASE_URL/api/portfolio/portfolios" \
    "application/vnd.pm.portfolio-1+json" \
    "Step 1: 獲取 Portfolio ID"

PORTFOLIO_RESPONSE=$(curl -s "${COMMON_HEADERS[@]}" \
    -H "Accept: application/vnd.pm.portfolio-1+json" \
    "$BASE_URL/api/portfolio/portfolios")

# Save formatted response using jq
echo "$PORTFOLIO_RESPONSE" | jq '{
    portfolio_id: ._items[0].id,
    total_items: ._collection.itemCount,
    links: ._links
}' > "$OUTPUT_DIR/1_portfolios.json"

# Extract Portfolio ID using jq
PORTFOLIO_ID=$(echo "$PORTFOLIO_RESPONSE" | jq -r '._items[0].id')
echo "export PORTFOLIO_ID=\"$PORTFOLIO_ID\"" >> "$ID_FILE"

export PORTFOLIO_ID
echo "Portfolio ID: $PORTFOLIO_ID"

# Step 2: Get Portfolio Items (Applications)
echo "=== Step 2: Getting Portfolio Items ==="
print_curl_command \
    "$BASE_URL/api/portfolio/portfolios/\$PORTFOLIO_ID/portfolio-items?_offset=0&_limit=100" \
    "application/vnd.pm.portfolio-items-1+json" \
    "Get Portfolio Items (Applications)"

if [ ! -z "$APP_FILTER" ]; then
    print_curl_command \
        "$BASE_URL/api/portfolio/portfolios/\$PORTFOLIO_ID/portfolio-items?_offset=0&_limit=100&name=\$APP_FILTER" \
        "application/vnd.pm.portfolio-items-1+json" \
        "Get Portfolio Items (Filtered by App Name)"
fi

PORTFOLIO_ITEMS_RESPONSE=$(curl -s -H "Api-Token: $API_TOKEN" \
    -H "Accept: application/vnd.pm.portfolio-items-1+json" \
    "$BASE_URL/api/portfolio/portfolios/$PORTFOLIO_ID/portfolio-items?_offset=0&_limit=100")

PORTFOLIO_ITEM_ID=$(echo "$PORTFOLIO_ITEMS_RESPONSE" | jq -r '._items[0].id')
echo "export PORTFOLIO_ITEM_ID=\"$PORTFOLIO_ITEM_ID\"" >> "$ID_FILE"


# Function to get portfolio items with pagination
get_all_portfolio_items() {
    local offset=$1
    local limit=$2
    local filter=$3
    local url="$BASE_URL/api/portfolio/portfolios/$PORTFOLIO_ID/portfolio-items?_offset=$offset&_limit=$limit"
    
    if [ ! -z "$filter" ]; then
        url="$url&$filter"
    fi
    
    curl -s "${COMMON_HEADERS[@]}" \
        -H "Accept: application/vnd.pm.portfolio-items-1+json" \
        "$url"
}

# Get first page to get total count
echo "獲取所有應用程式..."
FIRST_PAGE=$(get_all_portfolio_items 0 100 "")
TOTAL_ITEMS=$(echo "$FIRST_PAGE" | jq -r '._collection.itemCount')
TOTAL_PAGES=$(echo "$FIRST_PAGE" | jq -r '._collection.pageCount')

echo "發現總共 $TOTAL_ITEMS 個應用程式，分 $TOTAL_PAGES 頁"

# Initialize results array for all items
echo "[]" > "$OUTPUT_DIR/2_portfolio_items_all.json"

# Get all pages and combine them
for ((page=0; page<$TOTAL_PAGES; page++)); do
    offset=$((page * 100))
    echo "獲取應用程式第 $((page + 1))/$TOTAL_PAGES 頁..."
    
    RESPONSE=$(get_all_portfolio_items $offset 100 "")
    
    # Extract and format items from this page
    echo "$RESPONSE" | jq '[._items[] | {
        id,
        name,
        description,
        itemType,
        subscriptionTypeUsed,
        portfolioId,
        inTrash,
        createdAt,
        updatedAt,
        autoDeleteSetting,
        branchRetentionPeriodSetting,
        autoDeleteSettingsCustomized
    }]' > "$OUTPUT_DIR/temp_page.json"
    
    # Combine with existing results
    jq -s 'add' "$OUTPUT_DIR/2_portfolio_items_all.json" "$OUTPUT_DIR/temp_page.json" > "$OUTPUT_DIR/temp_combined.json"
    mv "$OUTPUT_DIR/temp_combined.json" "$OUTPUT_DIR/2_portfolio_items_all.json"
done

# Create filtered version if filter is specified
if [ ! -z "$APP_FILTER" ]; then
    PORTFOLIO_ITEMS_RESPONSE=$(get_all_portfolio_items 0 100 "name=$APP_FILTER")
else
    PORTFOLIO_ITEMS_RESPONSE="$FIRST_PAGE"
fi

# Save filtered/summary response
echo "$PORTFOLIO_ITEMS_RESPONSE" | jq '{
    total_items: ._collection.itemCount,
    applications: [._items[] | {
        id,
        name,
        description,
        itemType,
        createdAt,
        updatedAt,
        inTrash
    }]
}' > "$OUTPUT_DIR/2_portfolio_items.json"

# Extract Portfolio Item ID using jq
if [ ! -z "$APP_FILTER" ]; then
    PORTFOLIO_ITEM_ID=$(echo "$PORTFOLIO_ITEMS_RESPONSE" | jq -r --arg name "$APP_FILTER" '._items[] | select(.name == $name) | .id')
else
    PORTFOLIO_ITEM_ID=$(echo "$PORTFOLIO_ITEMS_RESPONSE" | jq -r '._items[0].id')
fi

export PORTFOLIO_ITEM_ID
echo "Portfolio Item ID: $PORTFOLIO_ITEM_ID"

# Step 3: Get Portfolio Subitems (Projects)
echo "=== Step 3: Getting Portfolio Subitems ==="
print_curl_command \
    "$BASE_URL/api/portfolio/portfolio-items/\$PORTFOLIO_ITEM_ID/portfolio-sub-items?_offset=0&_limit=100" \
    "application/vnd.pm.portfolio-subitems-1+json" \
    "Get Portfolio Subitems (Projects)"

if [ ! -z "$PROJECT_FILTER" ]; then
    print_curl_command \
        "$BASE_URL/api/portfolio/portfolio-items/\$PORTFOLIO_ITEM_ID/portfolio-sub-items?_offset=0&_limit=100&name=\$PROJECT_FILTER" \
        "application/vnd.pm.portfolio-subitems-1+json" \
        "Get Portfolio Subitems (Filtered by Project Name)"
fi

PORTFOLIO_SUBITEMS_RESPONSE=$(curl -s -H "Api-Token: $API_TOKEN" \
    -H "Accept: application/vnd.pm.portfolio-subitems-1+json" \
    "$BASE_URL/api/portfolio/portfolio-items/$PORTFOLIO_ITEM_ID/portfolio-sub-items?_offset=0&_limit=100")

PORTFOLIO_SUBITEM_ID=$(echo "$PORTFOLIO_SUBITEMS_RESPONSE" | jq -r '._items[0].id')
echo "export PORTFOLIO_SUBITEM_ID=\"$PORTFOLIO_SUBITEM_ID\"" >> "$ID_FILE"

# Function to get portfolio subitems with pagination
get_all_portfolio_subitems() {
    local offset=$1
    local limit=$2
    local filter=$3
    local url="$BASE_URL/api/portfolio/portfolio-items/$PORTFOLIO_ITEM_ID/portfolio-sub-items?_offset=$offset&_limit=$limit"
    
    if [ ! -z "$filter" ]; then
        url="$url&$filter"
    fi
    
    curl -s "${COMMON_HEADERS[@]}" \
        -H "Accept: application/vnd.pm.portfolio-subitems-1+json" \
        "$url"
}

# Get first page to get total count
echo "獲取所有專案..."
FIRST_PAGE=$(get_all_portfolio_subitems 0 100 "")
TOTAL_ITEMS=$(echo "$FIRST_PAGE" | jq -r '._collection.itemCount')
TOTAL_PAGES=$(echo "$FIRST_PAGE" | jq -r '._collection.pageCount')

echo "發現總共 $TOTAL_ITEMS 個專案，分 $TOTAL_PAGES 頁"

# Initialize results array for all items
echo "[]" > "$OUTPUT_DIR/3_portfolio_subitems_all.json"

# Get all pages and combine them
for ((page=0; page<$TOTAL_PAGES; page++)); do
    offset=$((page * 100))
    echo "獲取專案第 $((page + 1))/$TOTAL_PAGES 頁..."
    
    RESPONSE=$(get_all_portfolio_subitems $offset 100 "")
    
    # Extract and format items from this page
    echo "$RESPONSE" | jq '[._items[] | {
        id,
        name,
        description,
        subItemType,
        portfolioItemId,
        inTrash,
        createdAt,
        updatedAt,
        autoDeleteSetting,
        branchRetentionPeriodSetting,
        autoDeleteSettingsCustomized,
        defaultBranch: (if .defaultBranch then .defaultBranch else null end),
        entryPointUrl: (if .entryPointUrl then .entryPointUrl else null end),
        entryPointPrivate: (if .entryPointPrivate then .entryPointPrivate else null end),
        profile: (if .profile then .profile else null end)
    }]' > "$OUTPUT_DIR/temp_page.json"
    
    # Combine with existing results
    jq -s 'add' "$OUTPUT_DIR/3_portfolio_subitems_all.json" "$OUTPUT_DIR/temp_page.json" > "$OUTPUT_DIR/temp_combined.json"
    mv "$OUTPUT_DIR/temp_combined.json" "$OUTPUT_DIR/3_portfolio_subitems_all.json"
done

# Create filtered version if filter is specified
if [ ! -z "$PROJECT_FILTER" ]; then
    PORTFOLIO_SUBITEMS_RESPONSE=$(get_all_portfolio_subitems 0 100 "name=$PROJECT_FILTER")
else
    PORTFOLIO_SUBITEMS_RESPONSE="$FIRST_PAGE"
fi

# Save filtered/summary response
echo "$PORTFOLIO_SUBITEMS_RESPONSE" | jq '{
    total_items: ._collection.itemCount,
    projects: [._items[] | {
        id,
        name,
        description,
        subItemType,
        createdAt,
        updatedAt,
        inTrash,
        portfolioItemId
    }]
}' > "$OUTPUT_DIR/3_portfolio_subitems.json"

# Extract Portfolio Subitem ID using jq
if [ ! -z "$PROJECT_FILTER" ]; then
    PORTFOLIO_SUBITEM_ID=$(echo "$PORTFOLIO_SUBITEMS_RESPONSE" | jq -r --arg name "$PROJECT_FILTER" '._items[] | select(.name == $name) | .id')
else
    PORTFOLIO_SUBITEM_ID=$(echo "$PORTFOLIO_SUBITEMS_RESPONSE" | jq -r '._items[0].id')
fi

export PORTFOLIO_SUBITEM_ID
echo "Portfolio Subitem ID: $PORTFOLIO_SUBITEM_ID"
print_curl_command \
    "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID/branches" \
    "application/vnd.pm.branches-1+json" \
    "Step 4: 獲取所有分支"

print_curl_command \
    "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID/branches?name=$BRANCH_FILTER" \
    "application/vnd.pm.branches-1+json" \
    "Step 4: 使用分支名稱過濾獲取分支"

# Step 4: Get Branches
echo "=== Step 4: Getting Branches ==="
print_curl_command \
    "$BASE_URL/api/portfolio/portfolio-sub-items/\$PORTFOLIO_SUBITEM_ID/branches" \
    "application/vnd.pm.branches-1+json" \
    "Get All Branches"

if [ ! -z "$BRANCH_FILTER" ]; then
    print_curl_command \
        "$BASE_URL/api/portfolio/portfolio-sub-items/\$PORTFOLIO_SUBITEM_ID/branches?name=\$BRANCH_FILTER" \
        "application/vnd.pm.branches-1+json" \
        "Get Branches (Filtered by Branch Name)"
fi

BRANCHES_RESPONSE=$(curl -s -H "Api-Token: $API_TOKEN" \
    -H "Accept: application/vnd.pm.branches-1+json" \
    "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID/branches")

BRANCH_ID=$(echo "$BRANCHES_RESPONSE" | jq -r '._items[0].id')
echo "export BRANCH_ID=\"$BRANCH_ID\"" >> "$ID_FILE"

QUERY_PARAMS=""
if [ ! -z "$BRANCH_FILTER" ]; then
    QUERY_PARAMS="?name=$BRANCH_FILTER"
fi

BRANCHES_RESPONSE=$(curl -s "${COMMON_HEADERS[@]}" \
    -H "Accept: application/vnd.pm.branches-1+json" \
    "$BASE_URL/api/portfolio/portfolio-sub-items/$PORTFOLIO_SUBITEM_ID/branches$QUERY_PARAMS")

# Save formatted response using jq
echo "$BRANCHES_RESPONSE" | jq '{
    total_items: ._collection.itemCount,
    branches: [._items[] | {
        id,
        name,
        description,
        source,
        isDefault,
        createdAt,
        updatedAt,
        autoDeleteSetting,
        branchRetentionPeriodSetting
    }]
}' > "$OUTPUT_DIR/4_branches.json"

# Extract Branch ID if needed
if [ ! -z "$BRANCH_FILTER" ]; then
    BRANCH_ID=$(echo "$BRANCHES_RESPONSE" | jq -r --arg name "$BRANCH_FILTER" '._items[] | select(.name == $name) | .id')
else
    BRANCH_ID=$(echo "$BRANCHES_RESPONSE" | jq -r '._items[0].id')
fi

export BRANCH_ID
echo "Branch ID: $BRANCH_ID"

# Step 5: Get Issues from Latest Test
echo -e "\nStep 5: Getting Issues from Latest Test..."
echo "=== Step 5: Getting Issues ==="
print_curl_command \
    "$BASE_URL/api/specialization-layer-service/issues/_actions/list?portfolioSubItemId=\$PORTFOLIO_SUBITEM_ID&testId=latest&_offset=0&_limit=100&_includeAttributes=true" \
    "application/vnd.polaris-one.issue-management.issue-paginated-list-1+json" \
    "Get Issues from Latest Test"


print_curl_command \
    "$BASE_URL/api/specialization-layer-service/issues/_actions/list?portfolioSubItemId=$PORTFOLIO_SUBITEM_ID&testId=latest&_offset=0&_limit=100&_includeAttributes=true" \
    "application/vnd.polaris-one.issue-management.issue-paginated-list-1+json" \
    "Step 5: 獲取最新測試的所有問題"

print_curl_command \
    "$BASE_URL/api/specialization-layer-service/issues/_actions/list?portfolioSubItemId=$PORTFOLIO_SUBITEM_ID&testId=latest&_offset=100&_limit=100&_includeAttributes=true" \
    "application/vnd.polaris-one.issue-management.issue-paginated-list-1+json" \
    "Step 5: 獲取下一頁的問題"
# 函數:獲取帶分頁的 issues
get_all_issues() {
    local offset=$1
    local limit=$2
    local url="$BASE_URL/api/specialization-layer-service/issues/_actions/list?portfolioSubItemId=$PORTFOLIO_SUBITEM_ID&testId=latest&_offset=$offset&_limit=$limit&_includeAttributes=true"
    
    curl -s "${COMMON_HEADERS[@]}" \
        -H "Accept: application/vnd.polaris-one.issue-management.issue-paginated-list-1+json" \
        "$url"
}

# 獲取第一頁以獲得總數
echo "獲取所有 issues..."
FIRST_PAGE=$(get_all_issues 0 100)

# 保存原始回應以便調試
echo "$FIRST_PAGE" > "$OUTPUT_DIR/debug_first_page.json"

TOTAL_ITEMS=$(echo "$FIRST_PAGE" | jq -r '._collection.itemCount')
TOTAL_PAGES=$(echo "$FIRST_PAGE" | jq -r '._collection.pageCount')

echo "發現總共 $TOTAL_ITEMS 個 issues，分 $TOTAL_PAGES 頁"

# 初始化空陣列
echo "[]" > "$OUTPUT_DIR/temp_all_issues.json"

# 獲取所有頁面
for ((page=0; page<$TOTAL_PAGES; page++)); do
    offset=$((page * 100))
    echo "獲取第 $((page + 1))/$TOTAL_PAGES 頁..."
    
    if [ $page -eq 0 ]; then
        RESPONSE="$FIRST_PAGE"
    else
        RESPONSE=$(get_all_issues $offset 100)
        # 添加延遲以防止速率限制
        sleep 1
    fi
    
    # 使用修正後的 jq 邏輯提取和格式化此頁的 issues
    echo "$RESPONSE" | jq '._items | map({
        id,
        type: (.type._localized.name // "Unknown"),
        severity: (
            .attributes | map(select(.key == "severity")) | 
            if length > 0 then .[0].value else "Unknown" end
        ),
        description: (
            .attributes | map(select(.key == "description")) | 
            if length > 0 then .[0].value else null end
        ),
        cwe: (
            .attributes | map(select(.key == "cwe")) | 
            if length > 0 then .[0].value else "Unknown" end
        ),
        location: (
            .attributes | map(select(.key == "location")) | 
            if length > 0 then .[0].value else "Unknown" end
        ),
        published_date: (
            .attributes | map(select(.key == "published-date")) | 
            if length > 0 then .[0].value else null end
        ),
        component_name: (
            .attributes | map(select(.key == "component-name")) | 
            if length > 0 then .[0].value else "Unknown" end
        ),
        component_version: (
            .attributes | map(select(.key == "component-version-name")) | 
            if length > 0 then .[0].value else "Unknown" end
        ),
        overall_score: (
            .attributes | map(select(.key == "overall-score")) | 
            if length > 0 then .[0].value else null end
        ),
        vulnerability_id: (
            .attributes | map(select(.key == "vulnerability-id")) | 
            if length > 0 then .[0].value else null end
        ),
        vulnerability_source: (
            .attributes | map(select(.key == "vulnerability-source")) | 
            if length > 0 then .[0].value else "Unknown" end
        )
    })' > "$OUTPUT_DIR/temp_page.json"
    
    # 與現有結果合併
    jq -s 'add' "$OUTPUT_DIR/temp_all_issues.json" "$OUTPUT_DIR/temp_page.json" > "$OUTPUT_DIR/temp_combined.json"
    mv "$OUTPUT_DIR/temp_combined.json" "$OUTPUT_DIR/temp_all_issues.json"
    
    # 顯示頁面統計資訊
    PAGE_COUNT=$(jq 'length' "$OUTPUT_DIR/temp_page.json")
    echo "本頁處理了 $PAGE_COUNT 個 issues"
done

# 獲取最終計數
FINAL_COUNT=$(jq 'length' "$OUTPUT_DIR/temp_all_issues.json")
echo "最終收集到 $FINAL_COUNT issues"

# 生成最終文件
jq '{
    total_count: length,
    issues: sort_by(.severity) | reverse
}' "$OUTPUT_DIR/temp_all_issues.json" > "$OUTPUT_DIR/5_issues_all.json"

# 生成統計資訊
jq '
{
    total_count: length,
    severity_distribution: (
        reduce .[] as $item (
            {critical: 0, high: 0, medium: 0, low: 0};
            .[$item.severity | ascii_downcase] += 1
        )
    ),
    cwe_distribution: (
        reduce .[] as $item (
            {};
            . + { ($item.cwe): (.[($item.cwe)] + 1 // 1) }
        )
    ),
    component_distribution: (
        reduce .[] as $item (
            {};
            . + { ($item.component_name): (.[($item.component_name)] + 1 // 1) }
        )
    ),
    vulnerability_source_distribution: (
        reduce .[] as $item (
            {};
            . + { ($item.vulnerability_source): (.[($item.vulnerability_source)] + 1 // 1) }
        )
    )
}' "$OUTPUT_DIR/temp_all_issues.json" > "$OUTPUT_DIR/5_issues_statistics.json"

# 生成摘要報告
jq '{
    total_issues: length,
    severity_summary: {
        critical: map(select(.severity == "critical")) | length,
        high: map(select(.severity == "high")) | length,
        medium: map(select(.severity == "medium")) | length,
        low: map(select(.severity == "low")) | length
    },
    top_components: (
        group_by(.component_name) | 
        map({key: .[0].component_name, count: length}) |
        sort_by(.count) | reverse | 
        .[0:5]
    ),
    issues: sort_by(.severity) | reverse | .[0:10]
}' "$OUTPUT_DIR/temp_all_issues.json" > "$OUTPUT_DIR/5_issues_summary.json"

echo "完整的 issues 已保存到 $OUTPUT_DIR/5_issues_all.json"
echo "統計資訊已保存到 $OUTPUT_DIR/5_issues_statistics.json"
echo "摘要報告已保存到 $OUTPUT_DIR/5_issues_summary.json"
echo "Curl命令已保存到: $CURL_FILE"
echo "ID變數已保存到: $ID_FILE"