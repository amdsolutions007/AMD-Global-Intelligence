#!/usr/bin/env python3
"""
AMD Global Intelligence - Automated News Scraper
Collects AI and tech headlines from multiple sources
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys


def fetch_hackernews_ai():
    """Fetch AI-related stories from Hacker News"""
    print("🔍 Fetching Hacker News AI stories...")
    headlines = []
    
    try:
        response = requests.get("https://hacker-news.firebaseio.com/v0/beststories.json", timeout=10)
        story_ids = response.json()[:30]
        
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'ml', 'gpt', 'llm', 
                      'neural', 'deep learning', 'openai', 'anthropic', 'automation']
        
        for story_id in story_ids[:15]:
            story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=5)
            story = story_response.json()
            
            if story and 'title' in story:
                title_lower = story['title'].lower()
                if any(keyword in title_lower for keyword in ai_keywords):
                    url = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                    headlines.append({
                        'title': story['title'],
                        'url': url,
                        'source': 'Hacker News'
                    })
                    if len(headlines) >= 5:
                        break
    except Exception as e:
        print(f"⚠️ Error fetching Hacker News: {e}")
    
    return headlines


def fetch_arxiv_latest():
    """Fetch latest AI papers from ArXiv"""
    print("📚 Fetching ArXiv AI papers...")
    headlines = []
    
    try:
        url = "http://export.arxiv.org/rss/cs.AI"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'xml')
        
        items = soup.find_all('item', limit=5)
        for item in items:
            title = item.find('title').text.strip()
            link = item.find('link').text.strip()
            headlines.append({
                'title': title,
                'url': link,
                'source': 'ArXiv'
            })
    except Exception as e:
        print(f"⚠️ Error fetching ArXiv: {e}")
    
    return headlines


def fetch_techcrunch_ai():
    """Fetch AI news from TechCrunch"""
    print("🚀 Fetching TechCrunch AI news...")
    headlines = []
    
    try:
        url = "https://techcrunch.com/feed/"
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        soup = BeautifulSoup(response.content, 'xml')
        
        items = soup.find_all('item', limit=20)
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'openai', 'chatgpt', 
                      'anthropic', 'automation', 'llm', 'generative']
        
        for item in items:
            title = item.find('title').text.strip()
            title_lower = title.lower()
            
            if any(keyword in title_lower for keyword in ai_keywords):
                link = item.find('link').text.strip()
                headlines.append({
                    'title': title,
                    'url': link,
                    'source': 'TechCrunch'
                })
                if len(headlines) >= 5:
                    break
    except Exception as e:
        print(f"⚠️ Error fetching TechCrunch: {e}")
    
    return headlines


def update_news_file(all_headlines):
    """Update NEWS.md with new headlines"""
    print(f"📝 Updating NEWS.md with {len(all_headlines)} headlines...")
    
    current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    content = f"""# 📰 AI & Tech Intelligence Feed

**Automated News Collection - Updated Daily**

**Last Update:** {current_date}

---

## 🔥 Latest Headlines ({datetime.utcnow().strftime("%B %d, %Y")})

"""
    
    sources = {}
    for headline in all_headlines:
        source = headline['source']
        if source not in sources:
            sources[source] = []
        sources[source].append(headline)
    
    for source, headlines in sources.items():
        content += f"\n### {source}\n\n"
        for h in headlines:
            content += f"- [{h['title']}]({h['url']})\n"
    
    content += """
---

## 📊 Intelligence Summary

"""
    content += f"- **Total Headlines Collected:** {len(all_headlines)}\n"
    content += f"- **Sources Active:** {len(sources)}\n"
    content += f"- **Collection Time:** {current_date}\n"
    content += f"- **Status:** ✅ Operational\n"
    
    content += """
---

**🤖 This file is automatically updated daily at 09:00 UTC by GitHub Actions**
"""
    
    with open('NEWS.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ NEWS.md updated successfully!")


def main():
    """Main execution function"""
    print("🌐 AMD Global Intelligence - Starting news collection...")
    print("=" * 60)
    
    all_headlines = []
    all_headlines.extend(fetch_hackernews_ai())
    all_headlines.extend(fetch_arxiv_latest())
    all_headlines.extend(fetch_techcrunch_ai())
    
    if not all_headlines:
        print("⚠️ No headlines collected. Check network connectivity.")
        sys.exit(1)
    
    print("=" * 60)
    print(f"✅ Total headlines collected: {len(all_headlines)}")
    
    update_news_file(all_headlines)
    
    print("🎯 Mission complete!")


if __name__ == "__main__":
    main()
