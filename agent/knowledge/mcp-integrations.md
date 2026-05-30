# MCP-интеграции для визуализатора

Все четыре сервера уже описаны в `.mcp.json` — скопируй его в корень проекта и подставь ключи.

---

## 1. Официальный fal MCP — динамический выбор модели

**Docs:** https://fal.ai/docs/documentation/setting-up/mcp  
**Blog:** https://blog.fal.ai/connect-your-ai-to-1-000-models-with-the-fal-mcp-server/

**Что даёт:** 9 инструментов — поиск по 1000+ моделям каталога, запуск любой модели, проверка цен, схемы параметров. Агент сам выбирает лучшую модель по описанию задачи вместо хардкодированных режимов.

**Установка:**
```bash
claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp \
  --header "Authorization: Bearer YOUR_FAL_KEY"
```

**Что меняется:** вместо `--mode gpt` / `--mode concept` агент запрашивает актуальную лучшую модель из каталога. При выходе новых моделей — обновление автоматически, без правки кода.

---

## 2. image-viewer-mcp — рендеры прямо в чате

**GitHub:** https://github.com/itrimble/image-viewer-mcp

**Что даёт:** Отображает локальные файлы (JPG, PNG, WebP, SVG) inline в разговоре с Claude. Если терминал поддерживает Kitty/Ghostty — картинка в чате. Если нет — кликабельный путь.

**Установка:**
```bash
npm install -g image-viewer-mcp
```

Добавить в `.mcp.json` — уже есть.

**Что меняется:** после генерации агент сразу показывает результат без переключения в файловый менеджер. Итерация быстрее.

---

## 3. RamboRogers fal-image-video-mcp — авто-скачивание и авто-открытие

**GitHub:** https://github.com/RamboRogers/fal-image-video-mcp

**Что даёт:**
- Скачивает все результаты напрямую в `DOWNLOAD_PATH`
- `AUTOOPEN: true` — открывает результат в системном просмотрщике сразу после генерации
- `execute_custom_model` — запускает любой fal-эндпоинт за пределами встроенного реестра

**Установка:**
```bash
npm install fal-image-video-mcp
```

Конфиг уже в `.mcp.json`:
```json
"fal-local": {
  "env": {
    "FAL_KEY": "${FAL_KEY}",
    "DOWNLOAD_PATH": "output/renders/",
    "AUTOOPEN": "true"
  }
}
```

**Что меняется:** рендеры автоматически идут в папку проекта и сразу открываются. Ноль ручных шагов после генерации.

---

## 4. Higgsfield MCP — видео из рендеров

**Сайт:** https://higgsfield.ai/mcp  
**Гайд:** https://mcp.directory/blog/higgsfield-mcp-guide  
**Эндпоинт:** `https://mcp.higgsfield.ai`

**Что даёт:** 30+ видео-моделей через один hosted MCP:
- **Sora 2** — лучшее качество движения
- **Veo 3.1** — реалистичная физика
- **Kling 3.0** — быстро и дёшево
- Wan 2.6, Seedance 2.0, MiniMax Hailuo, Soul Cinema

Видео до 15 секунд, до 4K. Авторизация через Higgsfield-аккаунт.

**Установка:**
```bash
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai \
  --header "Authorization: Bearer YOUR_HIGGSFIELD_KEY"
```

Или через `.mcp.json` — уже есть.

**Зарегистрироваться:** https://higgsfield.ai — получи ключ, добавь в `.env` как `HIGGSFIELD_KEY`.

**Что добавляет:** из готового рендера — flythrough-видео для презентации клиенту. Архитектурное видео за 15 секунд без съёмочной группы.

**Пример запроса к агенту:**
```
Сделай видео из этого рендера — медленный облёт слева направо, 8 секунд
```

---

## Быстрый старт (всё сразу)

```bash
# 1. Скопируй .mcp.json в корень проекта (уже в репо)

# 2. Установи npm-пакеты
npm install -g image-viewer-mcp
npm install fal-image-video-mcp

# 3. Добавь ключи в .env
FAL_KEY=ваш_ключ
HIGGSFIELD_KEY=ваш_ключ  # опционально, для видео

# 4. Добавь fal MCP в Claude
claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp \
  --header "Authorization: Bearer $FAL_KEY"

# 5. Перезапусти Claude Code — все серверы подключатся автоматически
```

---

## Каталоги для мониторинга

| Ресурс | URL |
|--------|-----|
| awesome-claude-code-toolkit | https://github.com/rohitg00/awesome-claude-code-toolkit |
| awesome-agent-skills | https://github.com/VoltAgent/awesome-agent-skills |
| mcpcat.io | https://mcpcat.io/guides/best-mcp-servers-for-claude-code/ |
| fal.ai model catalog | https://fal.ai/models |
