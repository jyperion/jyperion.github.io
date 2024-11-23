import requests
import json
import os
from bs4 import BeautifulSoup
import markdown
from dotenv import load_dotenv
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import certifi

# Load environment variables
load_dotenv()

class SquarespaceUploader:
    def __init__(self):
        self.api_key = os.getenv('SQUARESPACE_API_KEY')
        self.website_url = os.getenv('SQUARESPACE_WEBSITE_URL', 'vanilla-smilodon-gn2y')
        
        if not self.api_key:
            raise ValueError("Missing required API key. Please ensure SQUARESPACE_API_KEY is set in .env file")
            
        # Configure session with retries and SSL verification
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Use certifi for SSL verification
        self.session.verify = certifi.where()
        
        # Set up headers
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Personal Website Uploader"
        }
        
        # Get the website ID from Squarespace
        self.website_id = self._get_website_id()
        if not self.website_id:
            raise ValueError("Could not determine website ID. Please check your API key and website URL.")
            
        self.base_url = f"https://api.squarespace.com/v2/websites/{self.website_id}"

    def _get_website_id(self):
        """Get the internal website ID from Squarespace"""
        try:
            # First, try to list all websites
            response = self.session.get(
                "https://api.squarespace.com/v2/websites",
                headers=self.headers
            )
            response.raise_for_status()
            websites = response.json().get('websites', [])
            
            # Look for our website URL
            for website in websites:
                if website.get('baseUrl') == self.website_url:
                    return website.get('id')
                    
            print(f"Could not find website with URL: {self.website_url}")
            print("Available websites:")
            for website in websites:
                print(f"- {website.get('baseUrl')} (ID: {website.get('id')})")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get website ID: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None

    def test_connection(self):
        """Test the API connection"""
        if not self.website_id:
            return False
            
        try:
            # Test with the website info endpoint
            response = self.session.get(
                f"{self.base_url}",
                headers=self.headers
            )
            if response.status_code == 401:
                print("Authentication failed. Please check your API key.")
                return False
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"API connection test failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False

    def create_page(self, title, content, url_slug):
        """Create a new page in Squarespace"""
        endpoint = f"{self.base_url}/sections"
        
        page_data = {
            "type": "page",
            "title": title,
            "urlSlug": url_slug,
            "content": {
                "layout": {
                    "type": "page",
                    "sections": [{
                        "type": "content",
                        "content": content
                    }]
                }
            },
            "visibility": "PUBLIC"
        }

        try:
            response = self.session.post(endpoint, headers=self.headers, json=page_data)
            response.raise_for_status()
            print(f"Successfully created page: {title}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to create page: {title}")
            print(f"Error: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None

    def upload_image(self, image_path):
        """Upload an image to Squarespace"""
        endpoint = f"{self.base_url}/images"
        
        try:
            with open(image_path, 'rb') as img:
                # Create multipart form-data
                files = {'file': (os.path.basename(image_path), img, 'image/png')}
                headers = self.headers.copy()
                headers.pop('Content-Type', None)  # Let requests set the correct content type
                
                response = self.session.post(
                    endpoint,
                    headers=headers,
                    files=files,
                    verify=self.session.verify
                )
                response.raise_for_status()
                
            print(f"Successfully uploaded image: {image_path}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to upload image: {image_path}")
            print(f"Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
        except IOError as e:
            print(f"Failed to read image file {image_path}: {str(e)}")
            return None

    def html_to_squarespace(self, html_content):
        """Convert HTML content to Squarespace-compatible format"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script tags
        for script in soup.find_all('script'):
            script.decompose()
            
        # Remove style tags
        for style in soup.find_all('style'):
            style.decompose()
            
        # Get the main content
        main_content = soup.find('main') or soup.find('body')
        if main_content:
            # Convert to Squarespace-compatible HTML
            content = str(main_content)
            # Clean up any specific HTML that Squarespace doesn't like
            content = content.replace('class="', 'data-class="')
            return content
        return ""

def main():
    try:
        uploader = SquarespaceUploader()
        
        # Test API connection first
        print("Testing API connection...")
        if not uploader.test_connection():
            print("Failed to establish API connection. Please check your credentials and try again.")
            return
        
        print("API connection successful!")
        
        # Upload images first
        images = ['background.png', 'icon.png']
        for image in images:
            if os.path.exists(image):
                uploader.upload_image(image)
            else:
                print(f"Warning: Image file not found: {image}")
        
        # Map of HTML files to their titles and slugs
        pages = {
            'index.html': ('Home', ''),
            'research.html': ('Research', 'research'),
            'publications.html': ('Publications', 'publications'),
            'industry.html': ('Industry Experience', 'industry'),
            'education.html': ('Education', 'education')
        }
        
        # Upload each page
        for html_file, (title, slug) in pages.items():
            if os.path.exists(html_file):
                print(f"\nProcessing {html_file}...")
                with open(html_file, 'r') as f:
                    content = f.read()
                
                # Convert HTML to Squarespace-compatible format
                sq_content = uploader.html_to_squarespace(content)
                
                # Create the page
                uploader.create_page(title, sq_content, slug)
            else:
                print(f"Warning: HTML file not found: {html_file}")
                
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
