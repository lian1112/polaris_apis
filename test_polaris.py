from findings_api import PolarisFindingsAPI
import logging

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 設置你的認證信息
BASE_URL = "https://poc.polaris.blackduck.com"  # 替換成你的 Polaris 服務器地址
API_TOKEN = "your-api-token-here"  # 替換成你的 API token
PROJECT_ID = "your-project-id"  # 替換成你的項目 ID

# 創建 API 實例
api = PolarisFindingsAPI(base_url=BASE_URL, api_token=API_TOKEN)

# 測試各種 API 調用
def test_api():
    try:
        # 獲取問題列表
        issues = api.get_issues(project_id=PROJECT_ID)
        print(f"Found {issues.get('_collection', {}).get('itemCount', 0)} issues")

        # 使用過濾器獲取高嚴重性的問題
        high_severity_issues = api.get_issues_with_filter(
            project_id=PROJECT_ID,
            severity="high"
        )
        print(f"Found {high_severity_issues.get('_collection', {}).get('itemCount', 0)} high severity issues")

        # 獲取按語言分組的統計
        language_counts = api.get_group_counts(
            project_id=PROJECT_ID,
            group_by="occurrence:language"
        )
        print("Issues by language:", language_counts)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    test_api()
