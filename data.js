// 自动生成的数据 - 初始化版本
const siteData = {
    "metadata": {
        "title": "伊朗战争追踪",
        "lastUpdate": "2025-03-14T15:15:00.000Z",
        "totalEvents": 4,
        "sources": {
            "international": 3,
            "iranian": 1,
            "social": 1,
            "osm": 1
        }
    },
    "events": [
        {
            "id": "evt_001",
            "date": "2024-10-01T08:00:00Z",
            "title": "伊朗发射导弹袭击以色列",
            "summary": "伊朗伊斯兰革命卫队向以色列发射了数十枚弹道导弹，作为对早些时候袭击的报复。以色列国防军表示，大部分导弹被拦截。",
            "category": "military",
            "location": {
                "lat": 32.0853,
                "lng": 34.7818,
                "name": "特拉维夫, 以色列"
            },
            "sources": [
                { "type": "international", "name": "BBC News", "url": "https://bbc.com" },
                { "type": "iranian", "name": "IRNA", "url": "https://irna.ir" }
            ],
            "languages": ["en", "fa"],
            "originalTexts": {
                "en": "Iran launches missile attack on Israel",
                "fa": "ایران به اسرائیل حمله موشکی کرد"
            }
        },
        {
            "id": "evt_002",
            "date": "2024-10-02T12:30:00Z",
            "title": "联合国安理会召开紧急会议",
            "summary": "安理会就伊朗-以色列冲突召开紧急会议，多国呼吁克制。美国表示将加强与中东盟友的防御合作。",
            "category": "diplomatic",
            "location": {
                "lat": 40.7128,
                "lng": -74.0060,
                "name": "纽约, 联合国"
            },
            "sources": [
                { "type": "international", "name": "Reuters", "url": "https://reuters.com" },
                { "type": "international", "name": "Al Jazeera", "url": "https://aljazeera.com" }
            ],
            "languages": ["en"],
            "originalTexts": {
                "en": "UN Security Council holds emergency meeting on Iran-Israel conflict"
            }
        },
        {
            "id": "evt_003",
            "date": "2024-10-03T15:45:00Z",
            "title": "社交媒体上出现伊朗城市抗议活动",
            "summary": "据社交媒体视频显示，德黑兰、马什哈德等城市出现小规模抗议，反对政府对以色列的袭击。伊朗当局暂时未回应。",
            "category": "political",
            "location": {
                "lat": 35.6892,
                "lng": 51.3890,
                "name": "德黑兰, 伊朗"
            },
            "sources": [
                { "type": "social", "name": "Twitter/X", "url": "https://twitter.com" },
                { "type": "social", "name": "Telegram", "url": "https://telegram.org" }
            ],
            "languages": ["fa", "en"],
            "originalTexts": {
                "fa": "تظاهرات در تهران و مشهد",
                "en": "Protests in Tehran and Mashhad"
            }
        },
        {
            "id": "evt_004",
            "date": "2024-10-04T09:20:00Z",
            "title": "也门胡塞武装加入冲突，袭击红海船只",
            "summary": "也门胡塞武装宣布将扩大针对以色列关联船只的攻击范围，红海航运安全警报升级。",
            "category": "military",
            "location": {
                "lat": 15.5527,
                "lng": 47.5198,
                "name": "红海"
            },
            "sources": [
                { "type": "international", "name": "AP News", "url": "https://apnews.com" },
                { "type": "osm", "name": "Maritime Security", "url": "https://maritimesecurity.com" }
            ],
            "languages": ["en", "ar"],
            "originalTexts": {
                "en": "Houthis expand attacks in Red Sea",
                "ar": "الحوثيون يوسعون الهجمات في البحر الأحمر"
            }
        }
    ]
};

// 翻译字典 - 预翻译的常用术语
const translations = {
    categories: {
        military: "军事行动",
        political: "政治发展",
        diplomatic: "外交反应",
        humanitarian: "人道状况"
    },
    sourceTypes: {
        international: "國際媒體",
        iranian: "伊朗媒體",
        social: "社交媒體",
        osm: "開源情報"
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { siteData, translations };
}