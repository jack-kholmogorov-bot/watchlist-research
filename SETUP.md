# Watchlist Research Skill - Setup Guide

## ✅ Что создано

### 1. Навык (Skill)
- **Location**: `~/.openclaw/skills/watchlist-research/`
- **Database**: `~/.openclaw/workspace/watchlist.db`
- **Scripts**:
  - `research_engine.py` - движок исследований
  - `watchlist.py` - управление watchlist

### 2. Cron Job
- **Schedule**: Вторник и Пятница в 8:00 AM (America/Phoenix)
- **Cron ID**: `ce3430ca-08d3-4c5e-8729-22b313837edd`
- **Job**: Автоматический запуск исследований

### 3. Топики на мониторинге
| Топик | Частота |
|-------|---------|
| Peter Steinberger | 30 дней |
| OpenClaw Features | 7 дней |
| IoT & Gadgets | 7 дней |
| Startup Ideas | 7 дней |
| B2B/B2C IoT Solutions | 7 дней |
| Business Problems for IoT | 7 дней |

---

## 🔑 Требуемые API Keys

### Обязательные:
```bash
export OPENROUTER_API_KEY=sk-...
export OPENAI_API_KEY=sk-...  # Опционально, для резервного поиска
```

### Опциональные:
```bash
export BRAVE_API_KEY=...  # Браузерный поиск
```

---

## 🐦 Twitter/X Search - Варианты

### 1. **Бесплатный (cookies)** - Рекомендуется
- Логин в x.com в браузере
- Скрипт читает cookies автоматически
- Не требует API key

### 2. **X API v2 (Official)**
- **Basic**: $100/мес, 10K tweets
- **Pro**: $5,000/мес, 1M tweets
- Apply at: https://developer.twitter.com/

### 3. **Third-party APIs** (Лучшее для большинства)
- **ScrapeOps**: scraperapi.com - от $49/мес
- **ScrapingBee**: scrapingbee.com - от $49/мес
- **Proxycurl**: nubela.co/proxycurl - от $49/мес
- **RapidAPI Twitter Scraper**: rapidapi.com
- **tweet-hunter.co**: специфично для твитов

### 4. **Nitter** (бесплатно, нестабильно)
- Инстансы часто падают
- Не рекомендуется для продакшена

### Рекомендация для вашего случая:
Использовать **Perplexity Sonar Pro** (через OpenRouter) - он уже ищет по X/Twitter и Reddit. Это бесплатно включено в результаты.

---

## 📺 YouTube API

### Вариант 1: YouTube Data API v3 (-FREE)
- **Квота**: 10,000 units/day (~100 поисков)
- **Регистрация**: https://console.cloud.google.com/
- **Как получить**:
  1. Создать проект в Google Cloud
  2. Включить YouTube Data API v3
  3. Создать API key

### Вариант 2: invidious (бесплатно, работает сейчас)
- Используется в скрипте по умолчанию
- Не требует API key
- Блокируется иногда

### Для транскриптов YouTube:
```bash
pip install yt-dlp
yt-dlp --extract-metadata --write-sub "https://youtube.com/watch?v=..."
```

---

## 🚀 Ручной запуск

```bash
# Список топиков
cd ~/.openclaw/skills/watchlist-research/scripts
python3 watchlist.py list

# Исследовать все топики
python3 watchlist.py run all

# Исследовать один топик
python3 watchlist.py run "IoT & Gadgets"

# Добавить новый топик
python3 watchlist.py add "My Topic" "keywords here" 7

# Генерация отчета
python3 watchlist.py report 7
```

---

## 📊 Использование через OpenClaw

```
/watchlist run all
/watchlist report
/watchlist list
```

---

## 🗄️ База данных

SQLite: `~/.openclaw/workspace/watchlist.db`

Таблицы:
- `topics` - настройка топиков
- `findings` - все найденные материалы

Запрос через SQL:
```sql
SELECT * FROM findings WHERE topic = 'IoT & Gadgets' ORDER BY found_at DESC LIMIT 10;
```

---

## 📈 API Ключи, которые нужны

| Сервис | Ключ | Стоимость | Где взять |
|--------|------|-----------|-----------|
| OpenRouter | OPENROUTER_API_KEY | ~$0.0025/1M tokens | openrouter.ai |
| Perplexity | Включено в OR | ~$1-5/запрос | через OpenRouter |
| YouTube API | YOUTUBE_API_KEY | Free 10K units/day | console.cloud.google.com |
| X API | X_API_KEY | $100-5000/мес | developer.twitter.com |
| Brave Search | BRAVE_API_KEY | Free 2K/mo | brave.com/search/api |

---

## 🎯 Что нужно сделать

1. **Добавить OPENROUTER_API_KEY**:
   ```bash
   echo 'export OPENROUTER_API_KEY=sk-...' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Запустить тест**:
   ```bash
   python3 ~/.openclaw/skills/watchlist-research/scripts/watchlist.py run "OpenClaw Features"
   ```

3. **Проверить cron статус**:
   ```bash
   cron status
   ```

---

Создано: 2026-03-04
Мастер: Eugine 🔧
