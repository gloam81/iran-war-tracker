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
import hashlib
import time
from urllib.parse import urljoin

# 配置
OUTPUT_DIR = "."
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "data.js")

# RSS 源列表
RSS_FEEDS = {
    "international": [
        "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
        # "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id",  # 格式特殊
        # "https://apnews.com/hub/apf-topnews/rss",  # 可能被屏蔽
    ],
    "iranian": [
        "https://www.irna.ir/rss",
        "https://www.tehrantimes.com/rss",
        "https://www.tasnimnews.com/rss",
        "https://www.mehrnews.com/rss",
        "https://www.isna.ir/rss",
        "https://www.presstv.ir/rss",  # PressTV
        # "https://www.hamshahrionline.ir/rss",  #  Hamshahri（可能无效）
    ],
    # 备用伊朗源（网页抓取）
    "iranian_scrape": [
        {"url": "https://www.irna.ir/", "name": "IRNA", "selector": "article"},
        {"url": "https://www.tehrantimes.com/", "name": "Tehran Times", "selector": ".article"},
        {"url": "https://www.tasnimnews.com/", "name": "Tasnim", "selector": "article"},
        {"url": "https://www.mehrnews.com/", "name": "Mehr", "selector": ".news-list"},
    ],
    # Telegram 频道（通过 RSS 聚合，待配置）
    "telegram": [
        # 示例：需要替换为实际的 RSS 链接
        # "https://rss.app/convert/telegram-channel-to-rss?channel=...
    ],
    # GDELT 事件源（API）
    "gdelt": {
        "enabled": False,  # 默认关闭
        "api_url": "https://api.gdeltproject.org/api/v2/events/search"
    }
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
        # MyMemory Translation API（免费，无需密钥）
        self.translate_api_url = "https://api.mymemory.translated.net/get"

    def translate_text(self, text: str, source_lang: str = 'en', target_lang: str = 'zh') -> str:
        """使用 MyMemory API 翻译文本"""
        if not text or not text.strip():
            return text
        
        # 如果已经是中文，跳过
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            return text
        
        try:
            # API 限制：每段最多 500 字符
            text = text[:500]
            params = {
                'q': text,
                'langpair': f'{source_lang}|{target_lang}'
            }
            response = requests.get(self.translate_api_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('responseStatus') == 200:
                    translated = data['responseData']['translatedText']
                    return translated
        except Exception as e:
            print(f"⚠️  翻译失败: {str(e)[:50]}")
        
        return text  # 失败时返回原文

    def fetch_rss(self, url: str, source_type: str, source_name: str) -> List[Dict]:
        """从 RSS 源获取新闻"""
        articles = []
        try:
            # 添加 User-Agent 避免被屏蔽
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; IranWarTracker/1.0)'}
            feed = feedparser.parse(url, agent='IranWarTracker/1.0', request_headers=headers)
            
            for entry in feed.entries[:15]:  # 限制数量，避免太多
                if entry.link in self.seen_urls:
                    continue

                title = entry.title
                summary = self.clean_html(entry.summary if hasattr(entry, 'summary') else entry.title)
                
                # 过滤：只保留与伊朗/中东相关的新闻
                if not self.is_relevant(title + " " + summary):
                    continue
                
                # 翻译成中文
                title_zh = self.translate_text(title)
                summary_zh = self.translate_text(summary)
                
                # 检测原文语言（简单判断）
                has_fa = any('\u0600' <= c <= '\u06FF' for c in title + summary)  # 阿拉伯/波斯字符
                has_en = any('a' <= c.lower() <= 'z' for c in title + summary)
                
                article = {
                    "id": self.generate_id(entry.link),
                    "title": title_zh,
                    "summary": summary_zh,
                    "date": self.parse_date(entry.published_parsed),
                    "url": entry.link,
                    "sources": [{"type": source_type, "name": source_name, "url": entry.link}],
                    "category": self.categorize(title + " " + summary),
                    "location": self.extract_location(title + " " + summary),
                    "languages": ["zh", "fa"] if has_fa else ["zh", "en"],
                    "originalTexts": {
                        "fa": title if has_fa else None,
                        "en": title if has_en and not has_fa else None
                    }
                }
                articles.append(article)
                self.seen_urls.add(entry.link)
        except Exception as e:
            print(f"⚠️  RSS源错误 {url}: {str(e)[:100]}")
        return articles

    def fetch_news_api(self) -> List[Dict]:
        """使用 NewsAPI 获取新闻"""
        if not NEWS_API_KEY:
            print("ℹ️  NEWS_API_KEY 未设置，跳过 NewsAPI 数据源")
            return []

        articles = []
        for keyword in SEARCH_KEYWORDS[:3]:  # 限制关键词数量
            try:
                url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&pageSize=10&apiKey={NEWS_API_KEY}"
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
                            "sources": [{"type": "international", "name": article["source"]["name"], "url": article["url"]}],
                            "category": self.categorize(article["title"]),
                            "location": {"lat": 32.0, "lng": 53.0, "name": "伊朗/中东"},
                            "languages": ["en"],
                            "originalTexts": {"en": article["title"]}
                        }
                        articles.append(article_data)
                        self.seen_urls.add(article["url"])
                else:
                    print(f"⚠️  NewsAPI 错误: {data.get('message', '未知错误')}")
            except Exception as e:
                print(f"⚠️  NewsAPI 请求失败 {keyword}: {str(e)[:100]}")
        return articles

    def scrape_website(self, url: str, source_name: str, selector: str = None) -> List[Dict]:
        """从网站抓取新闻（当RSS失败时）"""
        articles = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"  ⚠️  抓取失败 {source_name}: HTTP {response.status_code}")
                return []
            
            # 简单的 HTML 解析（提取链接和标题）
            html = response.text
            
            # 尝试提取新闻链接（多种模式）
            # 模式1: <a href="...">标题</a>
            links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', html)
            articles_found = 0
            
            for href, title in links[:20]:
                # 过滤非新闻链接
                if any(skip in href.lower() or skip in title.lower() for skip in ['/login', '/register', '/advert', '/contact', 'javascript:', '#']):
                    continue
                
                # 补全相对URL
                if href.startswith('/'):
                    href = urljoin(url, href)
                if not href.startswith('http'):
                    continue
                    
                if href in self.seen_urls:
                    continue
                    
                # 简单的去重和长度检查
                title = title.strip()
                if len(title) < 10 or len(title) > 200:
                    continue
                    
                # 翻译
                title_zh = self.translate_text(title)
                
                article = {
                    "id": self.generate_id(href),
                    "title": title_zh,
                    "summary": title_zh,  # 抓取的通常没有摘要
                    "date": datetime.utcnow().isoformat() + "Z",
                    "url": href,
                    "sources": [{"type": "iranian", "name": source_name, "url": url}],
                    "category": self.categorize(title),
                    "location": {"lat": 32.0, "lng": 53.0, "name": "伊朗/中东"},
                    "languages": ["zh", "fa"],  # 假设是波斯语源
                    "originalTexts": {"fa": title}
                }
                articles.append(article)
                self.seen_urls.add(href)
                articles_found += 1
                
            print(f"    ✅ 抓取到 {articles_found} 条新闻")
            return articles
            
        except Exception as e:
            print(f"  ⚠️  抓取异常 {source_name}: {str(e)[:80]}")
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
        # 军事相关关键词
        if any(word in text_lower for word in ['attack', 'missile', 'military', 'strike', 'bomb', 'war', 'conflict', 'iran', 'israel', 'houthi', 'hezbollah', 'gaza']):
            return 'military'
        # 政治相关关键词
        elif any(word in text_lower for word in ['protest', 'government', 'minister', 'election', 'parliament', 'president', ' supreme leader', 'political']):
            return 'political'
        # 外交相关关键词
        elif any(word in text_lower for word in ['un', 'talks', 'diplomat', 'agreement', 'peace', 'negotiation', 'sanction', 'foreign ministry']):
            return 'diplomatic'
        # 人道相关关键词
        elif any(word in text_lower for word in ['humanitarian', 'refugee', 'civilian', 'casualty', 'aid', 'medical', 'food shortage']):
            return 'humanitarian'
        else:
            return 'political'  # 默认

    def is_relevant(self, text: str) -> bool:
        """判断新闻是否与伊朗/中东冲突相关"""
        text_lower = text.lower()
        # 必须包含至少一个关键词
        keywords = [
            'iran', 'israel', 'middle east', 'persian', 'gulf', 'tehran',
            ' Baghdad', 'dubai', 'riyadh', 'ankara', 'damascus', 'beirut',
            'gaza', 'palestine', 'hamas', 'hezbollah', 'houthi', 'iraq',
            'syria', 'lebanon', 'jordan', 'saudi', 'uae', 'qatar', 'bahrain',
            'kuwait', 'oman', 'yemen', 'afghanistan', 'pakistan'
        ]
        return any(keyword in text_lower for keyword in keywords)

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

        print("🔍 开始收集新闻数据...")
        
        # RSS 收集（只处理字符串类型的源）
        print("📡 正在从 RSS 源获取新闻...")
        for source_type, feeds in RSS_FEEDS.items():
            # 跳过非RSS配置（如iranian_scrape, telegram, gdelt）
            if source_type in ['iranian_scrape', 'telegram', 'gdelt']:
                continue
            for feed_url in feeds:
                source_name = feed_url.split('/')[2]
                print(f"  - 读取 {source_name} ({source_type})")
                articles = self.fetch_rss(feed_url, source_type, source_name)
                print(f"    ✅ 获取到 {len(articles)} 条新闻")
                all_articles.extend(articles)

        # 如果伊朗源没获取到，尝试备用RSS源
        iranian_count = sum(1 for e in all_articles if any(s['type'] == 'iranian' for s in e['sources']))
        if iranian_count == 0:
            print("⚠️  主伊朗源未获取到数据，尝试备用RSS源...")
            for feed_url in RSS_FEEDS.get("iranian_backup", []):
                source_name = feed_url.split('/')[2]
                print(f"  - 尝试备用RSS源 {source_name}")
                articles = self.fetch_rss(feed_url, "iranian", source_name)
                print(f"    ✅ 获取到 {len(articles)} 条新闻")
                all_articles.extend(articles)
        
        # 如果还是没伊朗源，尝试网页抓取
        iranian_count = sum(1 for e in all_articles if any(s['type'] == 'iranian' for s in e['sources']))
        if iranian_count == 0:
            print("⚠️  RSS 伊朗源全部失败，尝试网页抓取...")
            for site in RSS_FEEDS.get("iranian_scrape", []):
                print(f"  - 抓取 {site['name']} ({site['url']})")
                articles = self.scrape_website(site['url'], site['name'], site.get('selector'))
                all_articles.extend(articles)
        
        # Telegram 频道（未来实现）
        # telegram_articles = self.fetch_telegram()
        # all_articles.extend(telegram_articles)
        
        # Telegram 频道（未来实现）
        # telegram_articles = self.fetch_telegram()
        # all_articles.extend(telegram_articles)

        # NewsAPI 收集
        print("📰 正在从 NewsAPI 获取新闻...")
        api_articles = self.fetch_news_api()
        print(f"    ✅ 获取到 {len(api_articles)} 条新闻")
        all_articles.extend(api_articles)

        # GDELT 收集
        print("🌍 正在从 GDELT 获取数据...")
        gdelt_articles = self.fetch_gdelt()
        print(f"    ✅ 获取到 {len(gdelt_articles)} 条数据")
        all_articles.extend(gdelt_articles)

        # 按日期排序
        all_articles.sort(key=lambda x: x['date'], reverse=True)

        # 限制总数（最近 100 条）
        result = all_articles[:100]
        print(f"📊 总共收集到 {len(result)} 条事件")
        return result

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




    def fetch_gdelt(self) -> List[Dict]:
        """获取 GDELT 事件数据"""
        return []

    def fetch_telegram(self) -> List[Dict]:
        """从 Telegram 频道获取新闻"""
        return []

def main():
    collector = NewsCollector()
    print("=" * 60)
    print("🔍 伊朗战争追踪 - 数据收集器")
    print("=" * 60)
    
    try:
        events = collector.collect()
        
        if not events:
            print("⚠️  未收集到任何新闻，使用示例数据...")
            events = get_sample_data()
        
        collector.save_data_js(events)
        print("=" * 60)
        print("✅ 数据收集完成！")
        print("=" * 60)
        
    except Exception as e:
        print("=" * 60)
        print("❌ 收集过程中出现错误:")
        print(f"   {type(e).__name__}: {e}")
        print("📝 使用示例数据作为回退...")
        print("=" * 60)
        
        events = get_sample_data()
        collector.save_data_js(events)
        print("✅ 已保存示例数据")
        sys.exit(0)  # 成功退出，避免工作流失败

def get_sample_data():
    """返回示例数据（当收集失败时使用）"""
    return [
        {
            "id": "evt_sample_001",
            "date": "2026-03-13T10:30:00Z",
            "title": "示例：伊朗举行军事演习（自动回退数据）",
            "summary": "这是数据收集失败时的示例事件。请检查 RSS 源连接或配置 NewsAPI_KEY。",
            "category": "military",
            "location": {"lat": 32.0, "lng": 53.0, "name": "伊朗"},
            "sources": [{"type": "international", "name": "Sample", "url": "#"}],
            "languages": ["zh"],
            "originalTexts": {"zh": "示例数据"}
        }
    ]


if __name__ == "__main__":
    main()