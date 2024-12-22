# findings.py - Polaris Findings API Client

import requests
from typing import Dict, List, Optional, Union
import logging

class PolarisFindingsAPI:
    """
    A class to handle all Polaris Findings API endpoints
    """
    
    def __init__(self, base_url: str, api_token: str):
        """
        Initialize the API handler
        
        Args:
            base_url: Base URL for the Polaris instance
            api_token: API token for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            'Api-Token': api_token
        }
        self.logger = logging.getLogger(__name__)

    def _make_request(self, method: str, endpoint: str, accept_type: str, 
                     params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        """
        Make HTTP request to Polaris API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            accept_type: Accept header type
            params: Query parameters
            data: Request body data
            
        Returns:
            API response as dictionary
        """
        headers = self.headers.copy()
        headers['Accept'] = accept_type
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise

    # Issues endpoints
    def get_issue_by_id(self, issue_id: str, app_id: str = None, project_id: str = None, 
                        include_type: bool = True, include_occurrence: bool = True,
                        include_triage: bool = True, include_first_detected: bool = True) -> Dict:
        """Get issue by ID"""
        params = {
            '_includeType': include_type,
            '_includeOccurrenceProperties': include_occurrence,
            '_includeTriageProperties': include_triage,
            '_includeFirstDetectedOn': include_first_detected
        }
        if app_id:
            params['applicationId'] = app_id
        if project_id:
            params['projectId'] = project_id
            
        return self._make_request(
            'GET',
            f'/api/findings/issues/{issue_id}',
            'application/vnd.polaris.findings.issues-1+json',
            params=params
        )

    def get_issues(self, app_id: str = None, project_id: str = None, 
                   params: Optional[Dict] = None) -> Dict:
        """Get list of issues"""
        default_params = {
            '_includeType': True,
            '_includeOccurrenceProperties': True,
            '_includeTriageProperties': True,
            '_first': 100
        }
        if params:
            default_params.update(params)
        if app_id:
            default_params['applicationId'] = app_id
        if project_id:
            default_params['projectId'] = project_id
            
        return self._make_request(
            'GET',
            '/api/findings/issues',
            'application/vnd.polaris.findings.issues-1+json',
            params=default_params
        )

    def get_issue_triage_history(self, issue_id: str, app_id: str = None,
                                project_id: str = None) -> Dict:
        """Get issue triage history"""
        params = {}
        if app_id:
            params['applicationId'] = app_id
        if project_id:
            params['projectId'] = project_id
            
        return self._make_request(
            'GET',
            f'/api/findings/issues/{issue_id}/triage-history',
            'application/vnd.polaris.findings.issues-1+json',
            params=params
        )

    def get_detection_history(self, issue_id: str, app_id: str = None,
                            project_id: str = None) -> Dict:
        """Get issue detection history"""
        params = {}
        if app_id:
            params['applicationId'] = app_id
        if project_id:
            params['projectId'] = project_id
            
        return self._make_request(
            'GET',
            f'/api/findings/issues/{issue_id}/detection-history',
            'application/vnd.polaris.findings.issues-1+json',
            params=params
        )

    def count_issues(self, app_id: str = None, project_id: str = None,
                    params: Optional[Dict] = None) -> Dict:
        """Count issues with optional grouping"""
        default_params = {
            '_includeAverageAge': True
        }
        if app_id:
            default_params['applicationId'] = app_id
        if project_id:
            default_params['projectId'] = project_id
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/findings/issues/_actions/count',
            'application/vnd.polaris.findings.issues-1+json',
            params=default_params
        )

    def count_issues_over_time(self, app_id: str = None, project_id: str = None,
                             last_days: int = None, from_date: str = None, 
                             to_date: str = None) -> Dict:
        """Count issues over time period"""
        params = {}
        if app_id:
            params['applicationId'] = app_id
        if project_id:
            params['projectId'] = project_id
        if last_days:
            params['_lastXDays'] = last_days
        if from_date:
            params['_fromDate'] = from_date
        if to_date:
            params['_toDate'] = to_date
            
        return self._make_request(
            'GET',
            '/api/findings/issues/_actions/count-over-time',
            'application/vnd.polaris.findings.issues-1+json',
            params=params
        )

    def export_issues(self, app_id: str = None, project_id: str = None,
                     file_name: str = None, params: Optional[Dict] = None) -> Dict:
        """Export issues to CSV/JSON"""
        default_params = {}
        if app_id:
            default_params['applicationId'] = app_id
        if project_id:
            default_params['projectId'] = project_id
        if file_name:
            default_params['fileName'] = file_name
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/findings/issues/_actions/export',
            'application/vnd.polaris.findings.issues-1+json',
            params=default_params
        )

    # Occurrence endpoints
    def get_occurrences(self, app_id: str = None, project_id: str = None,
                       params: Optional[Dict] = None) -> Dict:
        """Get list of occurrences"""
        default_params = {
            '_includeProperties': True,
            '_includeType': True
        }
        if app_id:
            default_params['applicationId'] = app_id
        if project_id:
            default_params['projectId'] = project_id
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/findings/occurrences',
            'application/vnd.polaris.findings.occurrences-1+json',
            params=default_params
        )

    def get_occurrence_by_id(self, occurrence_id: str, app_id: str = None,
                            project_id: str = None) -> Dict:
        """Get occurrence by ID"""
        params = {
            '_includeProperties': True,
            '_includeType': True
        }
        if app_id:
            params['applicationId'] = app_id
        if project_id:
            params['projectId'] = project_id
            
        return self._make_request(
            'GET',
            f'/api/findings/occurrences/{occurrence_id}',
            'application/vnd.polaris.findings.occurrences-1+json',
            params=params
        )

    def get_occurrence_snippet(self, occurrence_id: str, app_id: str = None,
                             project_id: str = None) -> Dict:
        """Get occurrence code snippet"""
        params = {}
        if app_id:
            params['applicationId'] = app_id
        if project_id:
            params['projectId'] = project_id
            
        return self._make_request(
            'GET',
            f'/api/findings/occurrences/{occurrence_id}/snippet',
            'application/vnd.polaris.findings.occurrences-1+json',
            params=params
        )

    def get_occurrence_assist(self, occurrence_id: str, app_id: str = None,
                            project_id: str = None) -> Dict:
        """Get AI assistance for occurrence"""
        params = {}
        if app_id:
            params['applicationId'] = app_id
        if project_id:
            params['projectId'] = project_id
            
        return self._make_request(
            'GET',
            f'/api/findings/occurrences/{occurrence_id}/assist',
            'application/vnd.polaris.findings.occurrences-1+json',
            params=params
        )

    def get_occurrence_artifact(self, occurrence_id: str, artifact_id: str,
                              app_id: str = None, project_id: str = None) -> Dict:
        """Get occurrence artifact"""
        params = {}
        if app_id:
            params['applicationId'] = app_id
        if project_id:
            params['projectId'] = project_id
            
        return self._make_request(
            'GET',
            f'/api/findings/occurrences/{occurrence_id}/artifacts/{artifact_id}',
            'text/plain',
            params=params
        )

    # Component Version endpoints
    def get_component_versions(self, project_id: str, params: Optional[Dict] = None) -> Dict:
        """Get component versions"""
        default_params = {
            'projectId': project_id,
            '_includeComponent': True,
            '_includeLicense': True
        }
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/findings/component-versions',
            'application/vnd.polaris.findings.component-versions-1+json',
            params=default_params
        )

    def get_component_version_by_id(self, version_id: str, project_id: str,
                                  include_component: bool = True,
                                  include_license: bool = True) -> Dict:
        """Get component version by ID"""
        params = {
            'projectId': project_id,
            '_includeComponent': include_component,
            '_includeLicense': include_license
        }
        return self._make_request(
            'GET',
            f'/api/findings/component-versions/{version_id}',
            'application/vnd.polaris.findings.component-versions-1+json',
            params=params
        )

    def count_component_versions(self, project_id: str, 
                               params: Optional[Dict] = None) -> Dict:
        """Count component versions with optional grouping"""
        default_params = {
            'projectId': project_id
        }
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/findings/component-versions/_actions/count',
            'application/vnd.polaris.findings.component-versions-1+json',
            params=default_params
        )

    def get_component_version_triage_history(self, version_id: str, project_id: str,
                                           params: Optional[Dict] = None) -> Dict:
        """Get triage history for component version"""
        default_params = {
            'projectId': project_id
        }
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            f'/api/findings/component-versions/{version_id}/triage-history',
            'application/vnd.polaris.findings.component-versions-1+json',
            params=default_params
        )

    # Component Origin endpoints
    def get_component_origin(self, origin_id: str, project_id: str) -> Dict:
        """Get component origin by ID"""
        params = {
            'projectId': project_id
        }
        return self._make_request(
            'GET',
            f'/api/findings/component-origins/{origin_id}',
            'application/vnd.polaris.findings.component-origins-1+json',
            params=params
        )

    def get_component_origins(self, project_id: str, params: Optional[Dict] = None) -> Dict:
        """Get list of component origins"""
        default_params = {
            'projectId': project_id
        }
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/findings/component-origins',
            'application/vnd.polaris.findings.component-origins-1+json',
            params=default_params
        )

    def get_component_origin_matches(self, origin_id: str, project_id: str,
                                   params: Optional[Dict] = None) -> Dict:
        """Get dependency paths for component origin"""
        default_params = {
            'projectId': project_id
        }
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            f'/api/findings/component-origins/{origin_id}/matches',
            'application/vnd.polaris.findings.component-origins-1+json',
            params=default_params
        )

    # License endpoints
    def get_license_by_id(self, license_id: str, include_text: bool = False) -> Dict:
        """Get license by ID"""
        params = {
            '_includeLicenseText': include_text
        }
        return self._make_request(
            'GET',
            f'/api/findings/licenses/{license_id}',
            'application/vnd.polaris.findings.licenses-1+json',
            params=params
        )

    def get_licenses(self, project_id: str = None, params: Optional[Dict] = None) -> Dict:
        """Get list of licenses"""
        default_params = {
            '_includeLicenseText': True
        }
        if project_id:
            default_params['projectId'] = project_id
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/findings/licenses',
            'application/vnd.polaris.findings.licenses-1+json',
            params=default_params
        )

    def count_licenses(self, project_id: str, params: Optional[Dict] = None) -> Dict:
        """Count licenses with optional grouping"""
        default_params = {
            'projectId': project_id
        }
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/findings/licenses/_actions/count',
            'application/vnd.polaris.findings.licenses-1+json',
            params=default_params
        )

    # Taxa endpoints
    def get_taxon(self, taxon_id: str) -> Dict:
        """Get taxon by ID"""
        return self._make_request(
            'GET',
            f'/api/findings/taxa/{taxon_id}',
            'application/vnd.polaris.findings.taxa-1+json'
        )

    def get_taxon_subtaxa(self, taxon_id: str, params: Optional[Dict] = None) -> Dict:
        """Get taxon's subtaxa"""
        return self._make_request(
            'GET',
            f'/api/findings/taxa/{taxon_id}/subtaxa',
            'application/vnd.polaris.findings.taxa-1+json',
            params=params
        )

    def get_taxon_issue_types(self, taxon_id: str, params: Optional[Dict] = None) -> Dict:
        """Get taxon's issue types"""
        return self._make_request(
            'GET',
            f'/api/findings/taxa/{taxon_id}/issue-types',
            'application/vnd.polaris.findings.taxa-1+json',
            params=params
        )

    def get_taxonomies(self, include_descendants: bool = False,
                      include_only_standards: bool = False) -> Dict:
        """
        Get list of taxonomies
        
        Args:
            include_descendants: Include all descendants instead of just child taxa
            include_only_standards: Include only the standards filter (like OWASP)
        """
        params = {
            '_includeDescendants': include_descendants,
            '_includeOnlyStandards': include_only_standards
        }
        return self._make_request(
            'GET',
            '/api/findings/taxonomies',
            'application/vnd.polaris.findings.taxonomies-1+json',
            params=params
        )


def main():
    """Main function to demonstrate usage"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Your API token here
    API_TOKEN = "your_api_token"
    
    # Create API instance
    api = PolarisFindingsAPI(
        base_url='https://poc.polaris.blackduck.com',
        api_token=API_TOKEN
    )
    
    try:
        # Get issues example
        logger.info("Starting issues fetch")
        issues = api.get_issues(project_id="your_project_id")
        logger.info(f"Found {issues['_collection']['itemCount']} issues")
        
        # Get occurrences example
        logger.info("Starting occurrences fetch")
        occurrences = api.get_occurrences(project_id="your_project_id")
        logger.info(f"Found {occurrences['_collection']['itemCount']} occurrences")
        
        # Get licenses example
        logger.info("Starting licenses fetch")
        licenses = api.get_licenses(project_id="your_project_id")
        logger.info(f"Found {licenses['_collection']['itemCount']} licenses")
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise


if __name__ == '__main__':
    main()