#!/usr/bin/env python3

import sys
import logging
import argparse
from datetime import datetime
import json
from typing import Dict, List, Optional, Any, Iterator
from dataclasses import dataclass
from findings import PolarisFindingsAPI
from portfolio import PolarisPortfolioAPI, PaginationParams

@dataclass
class ReportConfig:
    """Report configuration class"""
    base_url: str
    api_token: str
    app_name: str
    project_name: str
    branch: Optional[str] = None
    page_size: int = 100
    max_retries: int = 3
    timeout: int = 30

class ReportFormatter:
    """Formats report data for output"""
    
    @staticmethod
    def print_header(data: dict) -> None:
        """Print report header"""
        print("=" * 80)
        print(" " * 30 + "POLARIS SCAN REPORT")
        print("=" * 80)
        print(f"Application:     {data['application']}")
        print(f"Project:         {data['project']}")
        print(f"Branch:          {data.get('branch', 'N/A')}")
        print(f"Total Issues:    {data.get('total_issues', 0)}")
        print(f"Generated At:    {data['generated_at']}")
        print("=" * 80)
        print()

    @staticmethod
    def print_finding(finding: dict, index: int) -> None:
        """Print individual finding details"""
        try:
            # Get type info from localized name
            finding_type = finding.get('type', {}).get('_localized', {}).get('name', 'Unknown')
            
            # Get properties from occurrenceProperties
            occurrence_props = finding.get('occurrenceProperties', [])
            
            # Extract all necessary information at once
            info = {
                'severity': 'Unknown',
                'filename': 'Unknown',
                'line_number': 'Unknown',
                'location': 'Unknown',
                'cwe': 'Unknown',
                'description': None,
                'technical_description': None,
                'component_name': None,
                'vulnerability_id': None,
                'solution': None
            }
            
            # Update info from occurrence properties
            for prop in occurrence_props:
                key = prop.get('key', '')
                value = prop.get('value', '')
                
                if key == 'severity':
                    info['severity'] = value
                elif key == 'filename':
                    info['filename'] = value
                elif key == 'line-number':
                    info['line_number'] = value
                elif key == 'location':
                    info['location'] = value
                elif key == 'cwe':
                    info['cwe'] = f"CWE-{value}"
                elif key == 'description':
                    info['description'] = value
                elif key == 'technical-description':
                    info['technical_description'] = value
                elif key == 'component-name':
                    info['component_name'] = value
                elif key == 'vulnerability-id':
                    info['vulnerability_id'] = value
                elif key == 'solution':
                    info['solution'] = value
            
            # Print basic info
            print(f"Finding #{index}")
            print(f"Type:          {finding_type}")
            print(f"Severity:      {severity}")
            print(f"File Path:     {file_path}")
            print(f"Line Number:   {line_number}")
            print(f"CWE:          {cwe}")
            
            # Print additional properties
            for prop in occurrence_props:
                if prop['key'] not in ['cwe', 'severity']:
                    print(f"{prop['key']}:".ljust(14) + str(prop['value']))
            
            print()
            
        except Exception as e:
            logging.error(f"Error printing finding: {str(e)}")
            print()

    @staticmethod
    def print_code_snippet(finding: dict) -> None:
        """Print code snippet if available"""
        try:
            snippet = finding.get('code_snippet')
            if not snippet:
                return
                
            print("=== Code Snippet ===")
            if 'content' in snippet:
                print(snippet['content'].strip())
                
            if 'context' in snippet:
                print("\nContext:")
                print(snippet['context'].strip())
                
            print("=== End Snippet ===\n")
                
        except Exception as e:
            logging.error(f"Error printing code snippet: {str(e)}")

    @staticmethod
    def print_remediation(finding: dict) -> None:
        """Print AI remediation if available"""
        try:
            remediation = finding.get('ai_remediation')
            if not remediation:
                return
                
            print("=== AI Remediation ===")
            
            if 'analysis' in remediation:
                print("Analysis:")
                print(remediation['analysis'].strip())
                print()
                
            if 'recommendation' in remediation:
                print("Recommendation:")
                print(remediation['recommendation'].strip())
                
            print("=== End Remediation ===\n")
                
        except Exception as e:
            logging.error(f"Error printing remediation: {str(e)}")

class PolarisReporter:
    """Main reporter class"""
    
    def __init__(self, config: ReportConfig):
        """Initialize reporter with configuration"""
        self.config = config
        self.findings_api = PolarisFindingsAPI(config.base_url, config.api_token)
        self.portfolio_api = PolarisPortfolioAPI(config.base_url, config.api_token)
        self.logger = logging.getLogger(__name__)

    def find_project_ids(self) -> tuple[Optional[str], Optional[str]]:
        """Find application and project IDs"""
        try:
            # Get portfolios
            portfolios = self.portfolio_api.get_portfolios()
            if not portfolios.get('_items'):
                self.logger.error("No portfolios found")
                return None, None
                
            portfolio_id = portfolios['_items'][0]['id']
            
            # Get portfolio items (applications)
            pagination = PaginationParams(limit=100)
            items = self.portfolio_api.get_portfolio_items(portfolio_id, pagination)
            
            # Find matching application
            for item in items.get('_items', []):
                if item['name'] == self.config.app_name:
                    app_id = item['id']
                    
                    # Get application subitems (projects)
                    subitems = self.portfolio_api.get_portfolio_item_subitems(app_id)
                    
                    # Find matching project
                    for subitem in subitems.get('_items', []):
                        if subitem['name'] == self.config.project_name:
                            return app_id, subitem['id']
                            
            self.logger.error(f"Application '{self.config.app_name}' or project '{self.config.project_name}' not found")
            return None, None
            
        except Exception as e:
            self.logger.error(f"Error finding project IDs: {str(e)}")
            return None, None

    def get_issues_info(self, project_id: str) -> Optional[Dict]:
        """Get issues summary information"""
        try:
            results = self.findings_api.get_issues(
                project_id=project_id,
                params={'_first': 1}
            )
            return {
                'total_issues': results.get('_collection', {}).get('itemCount', 0)
            }
        except Exception as e:
            self.logger.error(f"Error getting issues info: {str(e)}")
            return None

    def get_findings(self, project_id: str) -> Iterator[Dict]:
        """Get all findings using pagination"""
        try:
            for page in self.findings_api.get_issues_paginated(
                project_id=project_id,
                page_size=self.config.page_size
            ):
                for finding in page.get('_items', []):
                    yield finding
                    
        except Exception as e:
            self.logger.error(f"Error getting findings: {str(e)}")

    def get_finding_details(self, finding_id: str, project_id: str) -> Optional[Dict]:
        """Get detailed information for a finding"""
        try:
            # Get basic finding info
            finding = self.findings_api.get_issue_by_id(
                issue_id=finding_id,
                project_id=project_id,
                include_type=True,
                include_occurrence=True,
                include_triage=True,
                include_first_detected=True
            )
            
            # Debug log the structure
            self.logger.debug(f"Finding structure: {json.dumps(finding, indent=2)}")
            
            # Get occurrence details if available
            occurrence = finding.get('occurrence', {})
            occurrence_id = occurrence.get('id')
            
            if occurrence_id:
                try:
                    # Get code snippet
                    snippet = self.findings_api.get_occurrence_snippet(
                        occurrence_id=occurrence_id,
                        project_id=project_id
                    )
                    finding['code_snippet'] = snippet
                except Exception as e:
                    self.logger.warning(f"Error getting code snippet: {str(e)}")
                    
                try:
                    # Get AI remediation
                    assist = self.findings_api.get_occurrence_assist_with_retry(
                        occurrence_id=occurrence_id,
                        project_id=project_id,
                        max_retries=self.config.max_retries
                    )
                    finding['ai_remediation'] = assist
                except Exception as e:
                    self.logger.warning(f"Error getting AI remediation: {str(e)}")
                    
            return finding
            
        except Exception as e:
            self.logger.error(f"Error getting finding details: {str(e)}")
            return None

    def generate_report(self) -> None:
        """Generate and save the full report"""
        try:
            # Find project
            app_id, project_id = self.find_project_ids()
            if not app_id or not project_id:
                return
                
            # Get issues info
            issues_info = self.get_issues_info(project_id)
            if not issues_info:
                return
                
            # Prepare report header
            report_data = {
                'application': self.config.app_name,
                'project': self.config.project_name,
                'branch': self.config.branch,
                'total_issues': issues_info['total_issues'],
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'findings': []
            }
            
            # Print header
            ReportFormatter.print_header(report_data)
            
            # Process each finding
            for index, finding in enumerate(self.get_findings(project_id), 1):
                self.logger.info(f"Processing finding {index} of {issues_info['total_issues']}")
                
                # Get detailed finding info
                detailed_finding = self.get_finding_details(finding['id'], project_id)
                if detailed_finding:
                    # Print finding details
                    ReportFormatter.print_finding(detailed_finding, index)
                    ReportFormatter.print_code_snippet(detailed_finding)
                    ReportFormatter.print_remediation(detailed_finding)
                    
                    # Add to report data
                    report_data['findings'].append(detailed_finding)
                    
            # Save report to file
            filename = f"polaris_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Report saved to: {filename}")
            
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise

def setup_logging(debug: bool = False) -> None:
    """Configure logging"""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Polaris Scan Report Generator')
    parser.add_argument('base_url', help='Polaris base URL')
    parser.add_argument('api_token', help='API token')
    parser.add_argument('application_name', help='Application name')
    parser.add_argument('project_name', help='Project name')
    parser.add_argument('--branch', help='Branch name')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    return parser.parse_args()

def main() -> None:
    """Main entry point"""
    try:
        # Parse arguments and setup logging
        args = parse_args()
        setup_logging(args.debug)
        
        # Create configuration
        config = ReportConfig(
            base_url=args.base_url,
            api_token=args.api_token,
            app_name=args.application_name,
            project_name=args.project_name,
            branch=args.branch
        )
        
        # Create and run reporter
        reporter = PolarisReporter(config)
        reporter.generate_report()
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        if args.debug:
            logging.exception("Detailed error information:")
        sys.exit(1)

if __name__ == '__main__':
    main()