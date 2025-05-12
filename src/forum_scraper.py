from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import time
import os
from pathlib import Path
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scraper.log', encoding='utf-8')
    ]
)

# Get output path from environment variable or use default
DEFAULT_OUTPUT_FILE = "foro_exportado.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "outputdata"
# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class ForumPost:
    title: str
    content: str
    author: str
    date: str

class MoodleForumScraper:
    def __init__(self, base_url: str, moodle_session: str):
        """
        Initialize the forum scraper
        
        Args:
            base_url: The base URL of the Moodle forum
            moodle_session: The MoodleSession cookie value
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.cookies.set('MoodleSession', moodle_session)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        logging.info(f"Initialized scraper for URL: {base_url}")
        logging.info("Cookie and headers set")

    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a page's content
        
        Args:
            url: The URL to fetch
            
        Returns:
            BeautifulSoup object or None if the request fails
        """
        try:
            logging.info(f"Fetching URL: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            # Check if we got a login page instead of content
            if "login" in response.url.lower():
                logging.error("Got redirected to login page. Session cookie might be invalid")
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if we can find any forum content using the new selector
            #if not soup.select(".forumpost .posting.fullpost") and not soup.select("tr.discussion a.d-block"):
            #    logging.error(f"No forum content found at {url}. Page content type: {response.headers.get('content-type')}")
            #    logging.debug(f"Page content preview: {response.text[:200]}")
            #    return None
                
            return soup
            
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error processing {url}: {str(e)}")
            return None

    def get_discussion_links(self, soup: BeautifulSoup) -> List[str]:
        """
        Extract discussion links from a forum page
        
        Args:
            soup: BeautifulSoup object of the forum page
            
        Returns:
            List of discussion URLs
        """
        discussion_links = []
        # Look for discussion links using the new selector
        for link in soup.select(".topic .d-flex a.w-100.h-100.d-block"):
            discussion_url = urljoin(self.base_url, link.get('href'))
            if discussion_url:
                logging.info(f"Found discussion: {link.text.strip()} - {discussion_url}")
                discussion_links.append(discussion_url)
        return discussion_links

    def extract_posts_from_discussion(self, url: str) -> List[ForumPost]:
        """
        Extract all posts from a discussion page
        
        Args:
            url: The URL of the discussion
            
        Returns:
            List of ForumPost objects
        """
        soup = self.get_page_content(url)
        if not soup:
            return []

        posts = []
        # Get all forum posts
        for post_article in soup.select("article.forum-post-container"):
            try:
                # Get the post content div
                post_content = post_article.select_one(".post-content-container")
                # Get header info
                header = post_article.select_one("header")
                
                if post_content and header:
                    # Extract title
                    title = header.select_one('h3[data-region-content="forum-post-core-subject"]')
                    # Extract author
                    author_link = header.select_one('a[href*="/user/view.php"]')
                    # Extract date
                    date = header.select_one('time')
                    
                    if all([title, author_link, date, post_content]):
                        post = ForumPost(
                            title=title.get_text(strip=True),
                            content=post_content.get_text(strip=True),
                            author=author_link.get_text(strip=True),
                            date=date.get('datetime', '')
                        )
                        # Log the scraped post to console
                        logging.info(f"\nPost found:")
                        logging.info(f"Title: {post.title}")
                        logging.info(f"Author: {post.author}")
                        logging.info(f"Date: {post.date}")
                        logging.info(f"Content: {post.content[:100]}...")  # Show first 100 chars of content
                        
                        posts.append(post)
                    else:
                        logging.warning(f"Incomplete post data found. Missing some required elements.")
            except Exception as e:
                logging.error(f"Error extracting post data: {str(e)}")
                continue

        return posts

    def scrape_forum(self) -> Dict[str, List[ForumPost]]:
        """
        Scrape all discussions and posts from the forum
        
        Returns:
            Dictionary mapping discussion URLs to lists of posts
        """
        all_discussions = {}
        page = 0
        
        while True:
            url = f"{self.base_url}&page={page}"
            logging.info(f"Scraping page {page}")
            
            soup = self.get_page_content(url)
            if not soup:
                break

            discussion_links = self.get_discussion_links(soup)
            if not discussion_links:
                break

            for discussion_url in discussion_links:
                logging.info(f"Scraping discussion: {discussion_url}")
                posts = self.extract_posts_from_discussion(discussion_url)
                if posts:
                    all_discussions[discussion_url] = posts
                time.sleep(1)  # Be nice to the server

            page += 1

        return all_discussions

    def save_to_file(self, discussions: Dict[str, List[ForumPost]], output_file: str):
        """
        Save the scraped discussions to a text file
        
        Args:
            discussions: Dictionary of discussion URLs and their posts
            output_file: Path to the output file
        """
        output_path = OUTPUT_DIR / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            for url, posts in discussions.items():
                f.write(f"\n{'='*80}\n")
                f.write(f"Discussion URL: {url}\n")
                f.write(f"{'='*80}\n\n")
                
                for post in posts:
                    f.write(f"Title: {post.title}\n")
                    f.write(f"Author: {post.author}\n")
                    f.write(f"Date: {post.date}\n")
                    f.write(f"Content:\n{post.content}\n")
                    f.write(f"\n{'-'*40}\n\n")
        logging.info(f"Forum content has been saved to {output_path}")

def main():
    """
    Main entry point for the Moodle forum scraper.
    
    This function:
    1. Prompts for a MoodleSession cookie value
    2. Allows the user to input multiple Moodle forum URLs
    3. Scrapes all discussions and posts from each forum
    4. Combines all content into a single output file
    5. Shows statistics about total discussions and posts scraped
    
    The output file location is determined by:
    - The OUT_FILE environment variable if set
    - The DEFAULT_OUTPUT_FILE value if not set
    
    Keyboard interrupt (Ctrl+C) can be used to stop the scraping process.
    """
    try:
        moodle_session = input("Enter your MoodleSession cookie value: ")
        if not moodle_session:
            logging.error("MoodleSession cookie is required")
            return

        output_file = os.getenv('OUT_FILE', DEFAULT_OUTPUT_FILE)
        all_discussions = {}

        while True:
            forum_url = input("Enter the Moodle forum URL (or press Enter to finish): ")
            if not forum_url:  # Empty input means we're done
                break

            if not forum_url.startswith(('http://', 'https://')):
                logging.error("Invalid URL. Please enter a complete URL starting with http:// or https://")
                continue

            logging.info(f"Starting forum scraping for URL: {forum_url}")
            scraper = MoodleForumScraper(forum_url, moodle_session)
            discussions = scraper.scrape_forum()

            if not discussions:
                logging.error(f"No discussions were found for {forum_url}. This could mean:")
                logging.error("1. The MoodleSession cookie is invalid or expired")
                logging.error("2. The URL is not a valid Moodle forum")
                logging.error("3. The forum is empty")
                logging.error("4. The forum requires additional permissions")
                continue

            all_discussions.update(discussions)

        if not all_discussions:
            logging.error("No discussions were scraped from any forum")
            return

        # Save all discussions to a single file
        scraper = MoodleForumScraper("", moodle_session)  # Create a scraper instance just for saving
        scraper.save_to_file(all_discussions, output_file)
        
        logging.info(f"Total discussions scraped: {len(all_discussions)}")
        total_posts = sum(len(posts) for posts in all_discussions.values())
        logging.info(f"Total posts scraped: {total_posts}")

    except KeyboardInterrupt:
        logging.info("Scraping cancelled by user")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
