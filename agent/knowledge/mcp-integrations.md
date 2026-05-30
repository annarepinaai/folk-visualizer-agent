# MCP-интеграции для визуализатора

Список проверенных MCP-серверов и скиллов, которые усиляют агента.
Разбиты по приоритету — от "поставь сразу" до "стратегически".

---

## Приоритет 1 — Поставь сразу (быстрый результат)

### Официальный fal MCP Server
**GitHub / Docs:** https://fal.ai/docs/documentation/setting-up/mcp  
**Что даёт:** 9 инструментов — поиск по 1000+ моделям каталога, запуск любой модели, проверка цен, схемы параметров. Агент сам выбирает оптимальную модель по описанию задачи вместо хардкодированных режимов.

**Установка (одна команда):**
```bash
claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp --header "Authorization: Bearer YOUR_FAL_KEY"
```

**Что меняется в агенте:** вместо `--mode gpt` / `--mode concept` агент запрашивает `recommend_model("photorealistic interior from ArchiCAD")` и получает актуальную лучшую модель из каталога. Никаких ручных обновлений при выходе новых моделей.

---

### image-viewer-mcp (показывает рендеры прямо в чате)
**GitHub:** https://github.com/itrimble/image-viewer-mcp  
**Что даёт:** Отображает локальные файлы (JPG, PNG, WebP, SVG) inline прямо в разговоре с Claude. Если терминал поддерживает Kitty/Ghostty — картинка в чате. Если нет — кликабельный путь.

**Установка:**
```bash
npm install -g image-viewer-mcp
# Добавить в .claude/settings.json:
# "mcpServers": { "image-viewer": { "command": "image-viewer-mcp" } }
```

**Что меняется:** после каждой генерации агент сразу показывает результат без переключения в файловый менеджер. Итерация вдвое быстрее.

---

### RamboRogers fal-image-video-mcp (авто-скачивание + авто-открытие)
**GitHub:** https://github.com/RamboRogers/fal-image-video-mcp  
**Что даёт:** Скачивает все результаты напрямую в `DOWNLOAD_PATH`, `AUTOOPEN: true` открывает результат в системном просмотрщике сразу после генерации. Инструмент `execute_custom_model` запускает любой fal-эндпоинт.

**Конфиг:**
```json
{
  "FAL_KEY": "ваш_ключ",
  "DOWNLOAD_PATH": "output/renders/",
  "AUTOOPEN": "true"
}
```

**Что меняется:** рендеры автоматически идут в папку проекта и сразу открываются. Убирает ручной шаг.

---

## Приоритет 2 — Меняет базовый workflow

### tapir-archicad-MCP (прямой доступ к открытой модели ArchiCAD)
**GitHub:** https://github.com/SzamosiMate/tapir-archicad-MCP  
**Оригинал:** https://github.com/lgradisar/archicad-mcp  
**Требования:** ArchiCAD 27+, Tapir add-on, Python 3.12+, Claude Desktop 0.9+

**Что даёт:** Claude напрямую работает с открытой моделью в ArchiCAD — читает материалы, геометрию, ориентации стен, находит конкретные элементы ("все окна с южной ориентацией"). Семантический поиск по элементам модели.

**Что меняется в workflow:**
```
СЕЙЧАС: архитектор вручную экспортирует JPG → описывает материалы → агент угадывает
БУДЕТ:  агент читает ArchiCAD напрямую → сам извлекает материалы → строит точный промпт
```

Шаг ANALYZE в алгоритме становится автоматическим.

---

### SketchUp Connector for Claude (официальный от Trimble, апрель 2026)
**Анонс:** https://news.trimble.com/2026-04-28-Trimble-Links-SketchUp-with-Anthropics-Claude  
**Что даёт:** Официальный MCP-коннектор от Trimble. Claude читает `.skp`-файлы, видит геометрию, создаёт объекты по описанию, экспортирует превью. Включается в настройках Claude через MCP-директорию.

**Что меняется:** файл `.skp` вместо PNG-экспорта. Агент видит настоящую геометрию, не картинку. Точнее ставит промпт — меньше итераций.

---

## Приоритет 3 — Следующий уровень

### Higgsfield MCP (видео из рендеров: Sora 2, Veo 3.1, Kling 3.0)
**Сайт:** https://higgsfield.ai/mcp  
**Эндпоинт:** `https://mcp.higgsfield.ai`  
**Что даёт:** 30+ видео-моделей через один hosted MCP. Sora 2, Veo 3.1, Kling 3.0, Wan 2.6. Видео до 15 секунд, до 4K. Авторизация через Higgsfield-аккаунт — без отдельных API-ключей.

**Что добавляет:** режим `/viz --video` — из готового рендера делает flythrough-видео для презентации клиенту. Архитектурное видео за 15 секунд. Ценность: показать клиенту пространство в движении, не стоп-кадр.

**Установка:**
```bash
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai \
  --header "Authorization: Bearer YOUR_HIGGSFIELD_KEY"
```

---

## Полезные скиллы-коллекции (референсы)

### AlpacaLabsLLC/skills-for-architects
**GitHub:** https://github.com/AlpacaLabsLLC/skills-for-architects  
**Что есть:** 37 скиллов для архитекторов. Из интересного: `product-and-materials-researcher` (5 скиллов) — ищет референсы материалов с реальными спецификациями. Можно адаптировать в `/viz-materials` — агент сам ищет правильные описания для промпта (тип дерева, камня, штукатурки).

### imsaif/design-with-claude
**GitHub:** https://github.com/imsaif/design-with-claude  
**Что есть:** 37 дизайн-специалистов как Claude Code агенты. `color-specialist` — подбирает точные hex-коды. Полезно для финального промпта когда нужна конкретика цвета материала.

---

## Каталоги для мониторинга

| Ресурс | URL | Что смотреть |
|--------|-----|-------------|
| awesome-claude-code-toolkit | https://github.com/rohitg00/awesome-claude-code-toolkit | 135+ агентов, раздел image/design |
| awesome-agent-skills | https://github.com/VoltAgent/awesome-agent-skills | 1000+ скиллов |
| mcpcat.io | https://mcpcat.io/guides/best-mcp-servers-for-claude-code/ | Рейтинг MCP по категориям |

---

## Что добавить первым (рекомендация)

```
День 1 (5 минут):
  claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp \
    --header "Authorization: Bearer $FAL_KEY"

День 1 (+ 5 минут):
  npm install -g image-viewer-mcp
  → рендеры видны прямо в чате

Следующий шаг:
  archicad-mcp / tapir — если ArchiCAD 27+
  Higgsfield MCP — когда нужны видео-презентации
```
