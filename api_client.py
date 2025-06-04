# api_client.py
import requests
import json
from typing import Dict, Any, Optional

class GSportAPIClient:
    """Client for GSport API operations"""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        
    def get_product_data(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch product data from GSport API
        
        Args:
            product_id: Product ID to fetch
            
        Returns:
            Dictionary with product data or None if failed
        """
        params = {
            "function": "getProductData",
            "APIkey": self.api_key,
            "productID": product_id,
            "lang": "pl"
        }
        
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from API")
            
    def update_product(self, xml_content: str) -> bool:
        """
        Update product data via GSport API
        
        Args:
            xml_content: XML content with product updates
            
        Returns:
            True if successful, False otherwise
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "function": "addUpdateProducts",
            "APIkey": self.api_key,
            "importType": "update",
            "prodIndex": "prod_id",
            "xml": xml_content
        }
        
        try:
            response = requests.post(
                self.api_url,
                data=data,
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"Update successful: {response.text}")
                return True
            else:
                print(f"Update failed {response.status_code}: {response.text}")
                return False
                
        except requests.RequestException as e:
            print(f"Update request failed: {str(e)}")
            return False


class OpenAIClient:
    """Client for OpenAI API operations"""
    
    def __init__(self, api_key: str, model: str, max_tokens: int):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """
        Generate content using OpenAI API
        
        Args:
            prompt: The prompt to send to the API
            
        Returns:
            Dictionary with success status, content/error, and cost
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Calculate cost
                usage = response_data['usage']
                cost = (
                    usage['prompt_tokens'] * INPUT_COST + 
                    usage['completion_tokens'] * OUTPUT_COST
                )
                
                return {
                    'success': True,
                    'content': response_data['choices'][0]['message']['content'],
                    'cost': cost,
                    'usage': usage
                }
            else:
                return {
                    'success': False,
                    'error': f"API error {response.status_code}: {response.text}",
                    'cost': 0
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f"Request failed: {str(e)}",
                'cost': 0
            }
        except (KeyError, json.JSONDecodeError) as e:
            return {
                'success': False,
                'error': f"Invalid response format: {str(e)}",
                'cost': 0
            }


# Import cost constants from config
from config import INPUT_COST, OUTPUT_COST