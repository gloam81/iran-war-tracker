// 自动生成的数据 - 更新时间: 2026-03-14
const siteData = {
    "metadata": {
        "title": "伊朗战争追踪",
        "lastUpdate": "2026-03-14T08:00:00.000Z",
        "totalEvents": 6,
        "sources": {
            "international": 4,
            "iranian": 2,
            "social": 2,
            "osm": 1
        }
    },
    "events": [
        {
            "id": "evt_001",
            "date": "2026-03-13T10:30:00Z",
            "title": "伊朗举行大规模军事演习",
            "summary": "伊朗伊斯兰革命卫队在南部波斯湾地区举行代号'伟大先知-19'的军事演习，测试新型导弹系统。伊朗方面称此举为防御性质，旨在展示威慑能力。",
            "category": "military",
            "location": {
                "lat": 26.5,
                "lng": 53.5,
                "name": "波斯湾, 伊朗"
            },
            "sources": [
                { "type": "iranian", "name": "IRNA", "url": "https://irna.ir" },
                { "type": "international", "name": "Reuters", "url": "https://reuters.com" }
            ],
            "languages": ["fa", "en"],
            "originalTexts": {
                "fa": "رزمایش بزرگ نظامی ایران در خلیج فارس",
                "en": "Iran holds large-scale military exercises in Persian Gulf"
            }
        },
        {
            "id": "evt_002",
            "date": "2026-03-12T14:15:00Z",
            "title": "国际原子能机构报告伊朗核活动进展",
            "summary": "IAEA 最新报告显示，伊朗铀浓缩活动继续推进，已接近武器级浓度。国际社会表达严重关切，呼吁伊朗恢复合作。",
            "category": "political",
            "location": {
                "lat": 48.2082,
                "lng": 16.3738,
                "name": "维也纳, 国际原子能机构"
            },
            "sources": [
                { "type": "international", "name": "AP News", "url": "https://apnews.com" },
                { "type": "international", "name": "BBC News", "url": "https://bbc.com" }
            ],
            "languages": ["en"],
            "originalTexts": {
                "en": "IAEA reports progress in Iran's nuclear activities"
            }
        },
        {
            "id": "evt_003",
            "date": "2026-03-11T09:45:00Z",
            "title": "伊朗社交媒体出现反政府抗议",
            "summary": "据多个社交媒体平台视频显示，德黑兰、伊斯法罕等城市出现小规模抗议活动，民众要求经济改革和释放政治犯。伊朗当局暂时未正式回应。",
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
                "fa": "تظاهرات ضد دولت در تهران",
                "en": "Anti-government protests in Tehran"
            }
        },
        {
            "id": "evt_004",
            "date": "2026-03-10T16:20:00Z",
            "title": "美国宣布对伊朗实施新制裁",
            "summary": "美国财政部宣布对伊朗多家实体和个人实施制裁，指控其支持地区武装组织并参与导弹项目。伊朗外交部称制裁'非法且无效'。",
            "category": "diplomatic",
            "location": {
                "lat": 38.9072,
                "lng": -77.0369,
                "name": "华盛顿, 美国"
            },
            "sources": [
                { "type": "international", "name": "Reuters", "url": "https://reuters.com" },
                { "type": "international", "name": "Al Jazeera", "url": "https://aljazeera.com" }
            ],
            "languages": ["en"],
            "originalTexts": {
                "en": "US announces new sanctions on Iran"
            }
        },
        {
            "id": "evt_005",
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
            "id": "evt_006",
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