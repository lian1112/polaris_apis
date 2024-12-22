import requests
from typing import Dict, List, Optional, Union
import logging

class PolarisPortfolioAPI:
    """
    A class to handle all Polaris Portfolio API endpoints
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

    # Portfolio endpoints
    def get_portfolios(self) -> Dict:
        """Get all portfolios"""
        return self._make_request(
            'GET',
            '/api/portfolio/portfolios',
            'application/vnd.pm.portfolio-1+json'
        )

    def get_portfolio_catalog(self, portfolio_id: str, params: Optional[Dict] = None) -> Dict:
        """Get portfolio catalog information"""
        return self._make_request(
            'GET',
            f'/api/portfolio/portfolios/{portfolio_id}/catalog',
            'application/vnd.pm.portfolio-catalog-1+json',
            params=params
        )

    # Portfolio Items endpoints
    def get_portfolio_items(self, portfolio_id: str, params: Optional[Dict] = None) -> Dict:
        """Get all portfolio items"""
        return self._make_request(
            'GET',
            f'/api/portfolio/portfolios/{portfolio_id}/portfolio-items',
            'application/vnd.pm.portfolio-items-1+json',
            params=params
        )

    def create_portfolio_item(self, portfolio_id: str, data: Dict) -> Dict:
        """Create a new portfolio item"""
        return self._make_request(
            'POST',
            f'/api/portfolio/portfolios/{portfolio_id}/portfolio-items',
            'application/vnd.pm.portfolio-items-1+json',
            data=data
        )

    def get_portfolio_item(self, item_id: str) -> Dict:
        """Get a specific portfolio item"""
        return self._make_request(
            'GET',
            f'/api/portfolio/portfolio-items/{item_id}',
            'application/vnd.pm.portfolio-items-1+json'
        )

    def update_portfolio_item(self, item_id: str, data: Dict) -> Dict:
        """Update a portfolio item"""
        return self._make_request(
            'PATCH',
            f'/api/portfolio/portfolio-items/{item_id}',
            'application/vnd.pm.portfolio-items-1+json',
            data=data
        )

    def delete_portfolio_item(self, item_id: str) -> None:
        """Delete a portfolio item"""
        self._make_request(
            'DELETE',
            f'/api/portfolio/portfolio-items/{item_id}',
            'application/vnd.pm.portfolio-items-1+json'
        )

    # Portfolio Sub-items endpoints
    def get_portfolio_subitems(self, params: Optional[Dict] = None) -> Dict:
        """Get all portfolio subitems"""
        return self._make_request(
            'GET',
            '/api/portfolio/portfolio-sub-items',
            'application/vnd.pm.portfolio-subitems-1+json',
            params=params
        )

    def create_portfolio_subitem(self, item_id: str, data: Dict) -> Dict:
        """Create a new portfolio subitem"""
        return self._make_request(
            'POST',
            f'/api/portfolio/portfolio-items/{item_id}/portfolio-sub-items',
            'application/vnd.pm.portfolio-subitems-1+json',
            data=data
        )

    def get_portfolio_item_subitems(self, item_id: str, params: Optional[Dict] = None) -> Dict:
        """Get subitems for a specific portfolio item"""
        return self._make_request(
            'GET',
            f'/api/portfolio/portfolio-items/{item_id}/portfolio-sub-items',
            'application/vnd.pm.portfolio-subitems-1+json',
            params=params
        )

    # Branches endpoints
    def get_branches(self, params: Optional[Dict] = None) -> Dict:
        """Get all branches"""
        return self._make_request(
            'GET',
            '/api/portfolio/branches',
            'application/vnd.pm.branches-1+json',
            params=params
        )

    def get_subitem_branches(self, subitem_id: str, params: Optional[Dict] = None) -> Dict:
        """Get branches for a specific subitem"""
        return self._make_request(
            'GET',
            f'/api/portfolio/portfolio-sub-items/{subitem_id}/branches',
            'application/vnd.pm.branches-1+json',
            params=params
        )

    # Tags endpoints
    def get_tags(self, params: Optional[Dict] = None) -> Dict:
        """Get all tags"""
        return self._make_request(
            'GET',
            '/api/portfolio/tags',
            'application/vnd.pm.tags-1+json',
            params=params
        )

    def get_application_tags(self, app_id: str, params: Optional[Dict] = None) -> Dict:
        """Get tags for a specific application"""
        return self._make_request(
            'GET',
            f'/api/portfolio/applications/{app_id}/tags',
            'application/vnd.pm.tags-1+json',
            params=params
        )

    # Entitlements endpoints
    def get_entitlements(self, item_id: str, params: Optional[Dict] = None) -> Dict:
        """Get entitlements for a portfolio item"""
        return self._make_request(
            'GET',
            f'/api/portfolio/portfolio-items/{item_id}/entitlements',
            'application/vnd.pm.entitlements-2+json',
            params=params
        )

    def get_entitlement_portfolio_count(self, entitlement_id: str) -> Dict:
        """Get portfolio item count for an entitlement"""
        return self._make_request(
            'GET',
            f'/api/portfolio/entitlements/{entitlement_id}/portfolio-item-count',
            'application/vnd.pm.entitlements-1+json'
        )

    # Issues endpoints
    def get_issues(self, subitem_id: str, params: Optional[Dict] = None) -> Dict:
        """Get issues for a portfolio subitem"""
        default_params = {
            'portfolioSubItemId': subitem_id,
            'testId': 'latest',
            '_includeAttributes': True
        }
        if params:
            default_params.update(params)
            
        return self._make_request(
            'GET',
            '/api/specialization-layer-service/issues/_actions/list',
            'application/vnd.polaris-one.issue-management.issue-paginated-list-1+json',
            params=default_params
        )

# Usage example
def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create API instance
    api = PolarisPortfolioAPI(
        base_url='https://polaris.blackduck.com',
        api_token='your_api_token_here'
    )
    
    try:
        # Get all portfolios
        portfolios = api.get_portfolios()
        portfolio_id = portfolios['_items'][0]['id']
        
        # Get portfolio items
        portfolio_items = api.get_portfolio_items(
            portfolio_id,
            params={'_limit': 10}
        )
        
        # Print results
        print("Portfolio Items:", portfolio_items)
        
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")

if __name__ == '__main__':
    main()
