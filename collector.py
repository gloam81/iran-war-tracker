#!/usr/bin/env python3
"""
伊朗战争追踪 - 数据收集器
从多个来源收集新闻事件，翻译成中文，生成数据文件
"""

import feedparser
import requests
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict
import os
import sys

# 配置
OUTPUT_DIR = "."
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "data.js")

# RSS 源列表
RSS_FEEDS = {
    "international": [
        "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
        "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id",
        "https://apnews.com/hub/apf-topnews/rss",
        "https://www.aljazeera.com/xml/rss/all.xml"
    ],
    "iranian": [
        "https://www.irna.ir/rss",
        "https://www.tehrantimes.com/rss"
    ]
}

# 新闻 API（需要注册免费 key）
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# 搜索关键词
SEARCH_KEYWORDS = [
    "Iran Israel war", "Iran conflict", "Iran military", "Tehran", "Iran news",
    "ایران اسرائیل", "جنگ ایران", "اخبار ایران"
]

class NewsCollector:
    def __init__(self):
        self.events = []
        self.seen_urls = set()

    def fetch_rss(self, url: str, source_type: str, source_name: str) -> List[Dict]:
        """从 RSS 源获取新闻"""
        articles = []
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:  # 限制数量
                if entry.link in self.seen_urls:
                    continue

                article = {
                    "id": self.generate_id(entry.link),
                    "title": entry.title,
                    "summary": self.clean_html(entry.summary if hasattr(entry, 'summary') else entry.title),
                    "date": self.parse_date(entry.published_parsed),
                    "url": entry.link,
                    "source": {"type": source_type, "name": source_name, "url": entry.link},
                    "category": self.categorize(entry.title + " " + entry.summary),
                    "location": self.extract_location(entry.title + " " + entry.summary),
                    "languages": ["en"] if source_type != "iranian" else ["fa"],
                    "originalTexts": {"en": entry.title}
                }
                articles.append(article)
                self.seen_urls.add(entry.link)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return articles

    def fetch_news_api(self) -> List[Dict]:
        """使用 NewsAPI 获取新闻"""
        if not NEWS_API_KEY:
            return []

        articles = []
        for keyword in SEARCH_KEYWORDS[:5]:  # 限制关键词数量
            try:
                url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&pageSize=20&apiKey={NEWS_API_KEY}"
                response = requests.get(url, timeout=10)
                data = response.json()

                if data.get("status") == "ok":
                    for article in data["articles"]:
                        if article["url"] in self.seen_urls:
                            continue

                        article_data = {
                            "id": self.generate_id(article["url"]),
                            "title": article["title"],
                            "summary": article["description"] or article["title"],
                            "date": article["publishedAt"],
                            "url": article["url"],
                            "source": {"type": "international", "name": article["source"]["name"], "url": article["url"]},
                            "category": self.categorize(article["title"]),
                            "location": {"lat": 32.0, "lng": 53.0, "name": "伊朗/中东"},
                            "languages": ["en"],
                            "originalTexts": {"en": article["title"]}
                        }
                        articles.append(article_data)
                        self.seen_urls.add(article["url"])
            except Exception as e:
                print(f"NewsAPI error for {keyword}: {e}")
        return articles

    def fetch_gdelt(self) -> List[Dict]:
        """获取 GDELT 事件数据（简化版）"""
        # 这里可以集成 GDELT API
        # 暂时返回空
        return []

    def generate_id(self, url: str) -> str:
        """从 URL 生成唯一 ID"""
        import hashlib
        return "evt_" + hashlib.md5(url.encode()).hexdigest()[:8]

    def parse_date(self, time_tuple) -> str:
        """解析日期为 ISO 格式"""
        if time_tuple:
            dt = datetime(*time_tuple[:6])
            return dt.isoformat() + "Z"
        return datetime.utcnow().isoformat() + "Z"

    def clean_html(self, text: str) -> str:
        """清理 HTML 标签"""
        if not text:
            return ""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()

    def categorize(self, text: str) -> str:
        """根据内容分类事件"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['attack', 'missile', 'military', 'strike', 'bomb']):
            return 'military'
        elif any(word in text_lower for word in ['protest', 'government', 'minister', 'election']):
            return 'political'
        elif any(word in text_lower for word in ['un', 'talks', 'diplomat', 'agreement', 'peace']):
            return 'diplomatic'
        else:
            return 'political'  # 默认

    def extract_location(self, text: str) -> Dict:
        """尝试提取地理位置"""
        # 简单的地理位置映射
        locations = {
            'tehran': {'lat': 35.6892, 'lng': 51.3890, 'name': '德黑兰, 伊朗'},
            'israel': {'lat': 31.7683, 'lng': 35.2137, 'name': '以色列'},
            'gaza': {'lat': 31.5, 'lng': 34.47, 'name': '加沙'},
            'lebanon': {'lat': 33.8938, 'lng': 35.5018, 'name': '黎巴嫩'},
            'yemen': {'lat': 15.5527, 'lng': 47.5198, 'name': '也门'},
            'syria': {'lat': 33.5138, 'lng': 36.2765, 'name': '叙利亚'},
            'iraq': {'lat': 33.3152, 'lng': 44.3661, 'name': '伊拉克'}
        }

        text_lower = text.lower()
        for key, loc in locations.items():
            if key in text_lower:
                return loc

        # 默认中东位置
        return {'lat': 32.0, 'lng': 53.0, 'name': '中东地区'}

    def collect(self) -> List[Dict]:
        """主收集函数"""
        all_articles = []

        # RSS 收集
        for source_type, feeds in RSS_FEEDS.items():
            for feed_url in feeds:
                source_name = feed_url.split('/')[2]
                articles = self.fetch_rss(feed_url, source_type, source_name)
                all_articles.extend(articles)

        # NewsAPI 收集
        api_articles = self.fetch_news_api()
        all_articles.extend(api_articles)

        # GDELT 收集
        gdelt_articles = self.fetch_gdelt()
        all_articles.extend(gdelt_articles)

        # 按日期排序
        all_articles.sort(key=lambda x: x['date'], reverse=True)

        # 限制总数（最近 100 条）
        return all_articles[:100]

    def save_data_js(self, events: List[Dict]):
        """保存为 JavaScript 数据文件"""
        data = {
            "metadata": {
                "title": "伊朗战争追踪",
                "lastUpdate": datetime.utcnow().isoformat() + "Z",
                "totalEvents": len(events),
                "sources": {
                    "international": len([e for e in events if any(s['type'] == 'international' for s in e['sources'])]),
                    "iranian": len([e for e in events if any(s['type'] == 'iranian' for s in e['sources'])]),
                    "social": len([e for e in events if any(s['type'] == 'social' for s in e['sources'])]),
                    "osm": len([e for e in events if any(s['type'] == 'osm' for s in e['sources'])])
                }
            },
            "events": events
        }

        # 生成 JS 文件内容
        js_content = f"""// 自动生成的数据 - 更新时间: {datetime.utcnow().isoformat()}Z
const siteData = {json.dumps(data, ensure_ascii=False, indent=2)};

const translations = {{
    categories: {{
        military: "军事行动",
        political: "政治发展",
        diplomatic: "外交反应",
        humanitarian: "人道状况"
    }},
    sourceTypes: {{
        international: "國際媒體",
        iranian: "伊朗媒體",
        social: "社交媒體",
        osm: "開源情報"
    }}
}};

if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ siteData, translations }};
}}
"""

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(js_content)

        print(f"✅ 数据已保存: {OUTPUT_FILE}")
        print(f"📊 事件总数: {len(events)}")
        print(f"🕐 最后更新: {data['metadata']['lastUpdate']}")

def main():
    collector = NewsCollector()
    print("🔍 开始收集新闻数据...")
    events = collector.collect()
    collector.save_data_js(events)
    print("✅ 完成!")

if __name__ == "__main__":
    main()