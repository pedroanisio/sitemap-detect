import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask import Flask, request, jsonify
import functools

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DetectionStrategy:
    """
    Base class for sitemap detection strategies.
    """
    def detect(self, url: str) -> list:
        """
        Abstract method to detect sitemap URLs from a given URL.

        Args:
            url (str): The URL to detect sitemaps from.

        Returns:
            list: A list of sitemap URLs.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

class RobotsTxtStrategy(DetectionStrategy):
    """
    Strategy for detecting sitemaps from the robots.txt file.
    """
    def detect(self, url: str) -> list:
        robots_url = urljoin(url, '/robots.txt')
        sitemap_urls = []
        try:
            response = requests.get(robots_url)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for line in lines:
                    if line.lower().startswith('sitemap:'):
                        sitemap_url = line.split(':', 1)[1].strip()
                        sitemap_urls.append(sitemap_url)
        except requests.RequestException as e:
            logging.error(f"Failed to fetch or parse robots.txt at {url}: {e}", exc_info=True)

        return sitemap_urls

class XMLSitemapStrategy(DetectionStrategy):
    """
    Strategy for detecting XML Sitemaps.
    """
    def detect(self, url: str) -> list:
        sitemap_urls = []
        common_sitemaps = [url.rstrip('/') + path for path in ['/sitemap.xml', '/sitemap_index.xml', '/sitemap1.xml']]
        for sitemap_url in common_sitemaps:
            try:
                response = requests.get(sitemap_url)
                if response.status_code == 200:
                    sitemap_urls.append(sitemap_url)
            except requests.RequestException as e:
                logging.error(f"Failed to retrieve sitemap at {sitemap_url}: {e}", exc_info=True)

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for sitemap_tag in soup.find_all('link', {'rel': 'sitemap'}):
                sitemap_href = sitemap_tag.get('href')
                if sitemap_href:
                    sitemap_urls.append(sitemap_href)
        except Exception as e:
            logging.error(f"Failed to detect XML sitemap at {url}: {e}", exc_info=True)

        return sitemap_urls

class SitemapDetector:
    """
    A class to detect sitemap URLs using multiple detection strategies.
    """
    def __init__(self, strategies: list):
        self.strategies = strategies

    @functools.lru_cache(maxsize=128)
    def detect_sitemap(self, url: str) -> list:
        for strategy in self.strategies:
            sitemap_urls = strategy.detect(url)
            if sitemap_urls:
                return sitemap_urls
        return []

# Flask application setup in a different module (not shown here)
app = Flask(__name__)
detector = SitemapDetector([RobotsTxtStrategy(), XMLSitemapStrategy()])  # Multiple strategies

@app.route('/detect_sitemap', methods=['GET'])
def detect_sitemap():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    sitemap_urls = detector.detect_sitemap(url)
    return jsonify({'url': url, 'sitemaps': sitemap_urls}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
