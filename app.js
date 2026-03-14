// 应用主逻辑
document.addEventListener('DOMContentLoaded', function() {
    initTabs();
    initMap();
    renderTimeline();
    renderNews();
    renderStats();
    updateLastUpdate();
});

// 标签页切换
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');

            // 如果切换到地图，需要重新调整地图大小
            if (targetTab === 'map' && window.map) {
                setTimeout(() => window.map.invalidateSize(), 100);
            }
        });
    });

    // 时间线过滤
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderTimeline(btn.getAttribute('data-filter'));
        });
    });

    // 新闻过滤
    document.getElementById('sourceFilter').addEventListener('change', renderNews);
    document.getElementById('languageFilter').addEventListener('change', renderNews);
}

// 初始化地图
function initMap() {
    const mapContainer = document.getElementById('map-container');
    if (!mapContainer) return;

    window.map = L.map('map-container').setView([32.0, 53.0], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(window.map);

    // 添加事件标记
    siteData.events.forEach(event => {
        const color = getEventColor(event.category);
        const marker = L.circleMarker([event.location.lat, event.location.lng], {
            radius: 8,
            fillColor: color,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(window.map);

        const popupContent = `
            <div style="max-width: 300px;">
                <h4>${event.title}</h4>
                <p>${event.summary}</p>
                <small>${new Date(event.date).toLocaleString('zh-CN')}</small><br>
                <small>来源: ${event.sources.map(s => s.name).join(', ')}</small>
            </div>
        `;
        marker.bindPopup(popupContent);
    });
}

function getEventColor(category) {
    const colors = {
        military: '#e74c3c',
        political: '#3498db',
        diplomatic: '#27ae60',
        humanitarian: '#f39c12'
    };
    return colors[category] || '#95a5a6';
}

// 渲染时间线
function renderTimeline(filter = 'all') {
    const container = document.getElementById('timelineContainer');
    const filteredEvents = filter === 'all'
        ? siteData.events
        : siteData.events.filter(e => e.category === filter);

    const sortedEvents = [...filteredEvents].sort((a, b) =>
        new Date(b.date) - new Date(a.date)
    );

    container.innerHTML = sortedEvents.map(event => `
        <div class="timeline-item ${event.category}">
            <div class="timeline-date">${formatDate(event.date)}</div>
            <h3 class="timeline-title">${event.title}</h3>
            <div class="timeline-content">${event.summary}</div>
            <div class="timeline-sources">
                ${event.sources.map(s => `
                    <span class="timeline-source">
                        <a href="${s.url}" target="_blank">${s.name}</a>
                    </span>
                `).join('')}
            </div>
        </div>
    `).join('');
}

// 渲染新闻
function renderNews() {
    const container = document.getElementById('newsContainer');
    const sourceFilter = document.getElementById('sourceFilter').value;
    const languageFilter = document.getElementById('languageFilter').value;

    let filteredEvents = siteData.events;

    if (sourceFilter !== 'all') {
        filteredEvents = filteredEvents.filter(e =>
            e.sources.some(s => s.type === sourceFilter)
        );
    }

    if (languageFilter !== 'all') {
        filteredEvents = filteredEvents.filter(e =>
            e.languages.includes(languageFilter)
        );
    }

    container.innerHTML = filteredEvents.map(event => `
        <article class="news-card">
            <span class="news-source-badge ${event.sources[0].type}">
                ${translations.sourceTypes[event.sources[0].type] || event.sources[0].type}
            </span>
            <h3 class="news-title">${event.title}</h3>
            <p class="news-summary">${event.summary}</p>
            <div class="news-meta">
                <span>${formatDate(event.date)}</span>
                <a href="${event.sources[0].url}" target="_blank" class="news-link">
                    阅读原文 →
                </a>
            </div>
        </article>
    `).join('');
}

// 渲染统计
function renderStats() {
    const container = document.getElementById('statsContainer');

    const stats = {
        "总事件数": siteData.events.length,
        "国际媒体": siteData.events.filter(e =>
            e.sources.some(s => s.type === 'international')).length,
        "伊朗媒体": siteData.events.filter(e =>
            e.sources.some(s => s.type === 'iranian')).length,
        "社交媒体": siteData.events.filter(e =>
            e.sources.some(s => s.type === 'social')).length,
        "开源情报": siteData.events.filter(e =>
            e.sources.some(s => s.type === 'osm')).length
    };

    container.innerHTML = Object.entries(stats).map(([label, value]) => `
        <div class="stat-card">
            <div class="stat-number">${value}</div>
            <div class="stat-label">${label}</div>
            <div class="stat-detail">
                ${label === "总事件数"
                    ? `覆盖 ${siteData.events.length} 个事件`
                    : ''}
            </div>
        </div>
    `).join('');
}

// 工具函数
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleString('zh-CN', options);
}

function updateLastUpdate() {
    const element = document.getElementById('lastUpdate');
    if (element) {
        const now = new Date();
        element.textContent = `最后更新: ${now.toLocaleString('zh-CN')}`;
    }
}