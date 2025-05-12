from forum_scraper import MoodleForumScraper
from bs4 import BeautifulSoup
import logging

def test_discussion_links():
    print("\nTesting discussion link extraction...")
    # Read the demo HTML file
    with open("demo.htlm", "r", encoding='utf-8') as f:
        html_content = f.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a scraper instance with dummy values
    scraper = MoodleForumScraper("https://aulas.ort.edu.uy", "dummy_session")

    # Test discussion link extraction
    links = scraper.get_discussion_links(soup)
    print("\nFound Discussion Links:")
    for link in links:
        print(f"- {link}")

def test_post_extraction():
    print("\nTesting post content extraction...")
    # Read the actual discussion page HTML file
    with open("src/demodisusionpage.html", "r", encoding='utf-8') as f:
        html_content = f.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a scraper instance with dummy values
    scraper = MoodleForumScraper("https://aulas.ort.edu.uy", "dummy_session")

    # Override the get_page_content method for testing
    scraper.get_page_content = lambda url: soup

    # Test post extraction
    posts = scraper.extract_posts_from_discussion("https://example.com/discussion")
    print("\nExtracted Posts:")
    for i, post in enumerate(posts, 1):
        print(f"\nPost {i}:")
        print(f"Title: {post.title}")
        print(f"Author: {post.author}")
        print(f"Date: {post.date}")
        print(f"Content: {post.content}")

if __name__ == "__main__":
    test_discussion_links()
    test_post_extraction()
