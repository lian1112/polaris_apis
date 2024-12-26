#!/usr/bin/env python3

import sys
import logging
from datetime import datetime
import json
from findings import PolarisFindingsAPI
from portfolio import PolarisPortfolioAPI, PaginationParams

def find_project_and_app(portfolio_api: PolarisPortfolioAPI, app_name: str, project_name: str):
    """
    Find application ID and project ID by their names
    """
    portfolios = portfolio_api.get_portfolios()
    if not portfolios.get('_items'):
        return None, None
        
    portfolio_id = portfolios['_items'][0]['id']
    
    # Get portfolio items with pagination
    pagination = PaginationParams(limit=100)
    items = portfolio_api.get_portfolio_items(portfolio_id, pagination)
    
    # Find application
    app_id = None
    project_id = None
    
    for item in items.get('_items', []):
        if item.get('name') == app_name:
            app_id = item.get('id')
            
            # Get projects in this application
            if app_id:
                subitems = portfolio_api.get_portfolio_item_subitems(app_id)
                for subitem in subitems.get('_items', []):
                    if subitem.get('name') == project_name:
                        project_id = subitem.get('id')
                        break
            break
            
    return app_id, project_id

def save_report(data: dict, prefix: str = "issues_report"):
    """Save data to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename

def print_issues_summary(issues: list):
    """Print summary of issues"""
    if not issues:
        print("No issues found.")
        return
        
    print(f"\nTotal issues found: {len(issues)}")
    
    # Count by severity
    severity_count = {}
    status_count = {}
    
    for issue in issues:
        occurrence = issue.get('occurrence', {})
        severity = occurrence.get('severity', 'Unknown')
        severity_count[severity] = severity_count.get(severity, 0) + 1
        
        triage = issue.get('triage', {})
        status = triage.get('status', 'Unknown')
        status_count[status] = status_count.get(status, 0) + 1
    
    print("\nIssues by severity:")
    for severity, count in sorted(severity_count.items()):
        print(f"  {severity}: {count}")
        
    print("\nIssues by status:")
    for status, count in sorted(status_count.items()):
        print(f"  {status}: {count}")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) != 5:
        print("Usage: python get_issues_detail.py <base_url> <api_token> <application_name> <project_name>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    api_token = sys.argv[2]
    app_name = sys.argv[3]      # e.g., "allenl_applications"
    project_name = sys.argv[4]  # e.g., "WebGoat"
    
    try:
        # Initialize APIs
        findings_api = PolarisFindingsAPI(base_url, api_token)
        portfolio_api = PolarisPortfolioAPI(base_url, api_token)
        
        # Get project and application IDs
        logging.info(f"Looking for project '{project_name}' in application '{app_name}'")
        app_id, project_id = find_project_and_app(portfolio_api, app_name, project_name)
        
        if not app_id:
            logging.error(f"Application '{app_name}' not found")
            sys.exit(1)
            
        if not project_id:
            logging.error(f"Project '{project_name}' not found in application '{app_name}'")
            sys.exit(1)
        
        # Get issues using findings API
        logging.info("Fetching issues...")
        issues = findings_api.get_issues(
            project_id=project_id,
        )
        
        # Save report
        report_data = {
            'application_name': app_name,
            'project_name': project_name,
            'application_id': app_id,
            'project_id': project_id,
            'issues': issues.get('_items', [])
        }
        report_file = save_report(report_data, f"issues_{app_name}_{project_name}")
        
        # Print summary
        print_issues_summary(issues.get('_items', []))
        print(f"\nDetailed report saved to: {report_file}")
        
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()