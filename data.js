// 自动生成的数据 - 更新时间: 2026-03-14T12:46:58.982801Z
const siteData = {
  "metadata": {
    "title": "伊朗战争追踪",
    "lastUpdate": "2026-03-14T12:46:58.982789Z",
    "totalEvents": 1,
    "sources": {
      "international": 1,
      "iranian": 0,
      "social": 0,
      "osm": 0
    }
  },
  "events": [
    {
      "id": "evt_sample_001",
      "date": "2026-03-13T10:30:00Z",
      "title": "示例：伊朗举行军事演习（自动回退数据）",
      "summary": "这是数据收集失败时的示例事件。请检查 RSS 源连接或配置 NewsAPI_KEY。",
      "category": "military",
      "location": {
        "lat": 32.0,
        "lng": 53.0,
        "name": "伊朗"
      },
      "sources": [
        {
          "type": "international",
          "name": "Sample",
          "url": "#"
        }
      ],
      "languages": [
        "zh"
      ],
      "originalTexts": {
        "zh": "示例数据"
      }
    }
  ]
};

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
