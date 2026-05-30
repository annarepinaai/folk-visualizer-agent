# Architectural Visualizer Agent

AI-агент для архитектурной визуализации на базе GPT Image 2 (через fal.ai).

Берёт экспорт из ArchiCAD или SketchUp и превращает в фотореалистичный рендер с сохранением геометрии.

## Что умеет

- **ArchiCAD / SketchUp → фотореализм** — цветной экспорт + Hidden Line → GPT Image 2 → рендер
- **Апскейл готового рендера** — +детализация материалов, объёмный свет, без изменения геометрии
- **Замена материала с референсом** — передаёшь фото ламината/камня/ткани, агент применяет точно
- **Концепт из текста** — быстрые наброски атмосферы без модели (Nano Banana 2)
- **Точечная правка** — изменить один материал на готовом рендере

## Структура

```
folk-visualizer-agent/
├── scripts/
│   └── viz_render.py       ← Python-скрипт, вызывает fal.ai API
└── agent/
    ├── CLAUDE.md            ← точка входа агента (Claude Code)
    ├── core.md              ← логика и алгоритм агента
    ├── overrides.md         ← твои кастомизации (заполни под свою студию)
    ├── memory.md            ← накопленный опыт (агент ведёт сам)
    ├── failures.md          ← журнал ошибок
    ├── knowledge/           ← база знаний
    │   ├── prompt-library.md      — шаблоны промптов (жилое / HoReCa / реставрация)
    │   ├── studio-digests.md      — принципы топ-студий мира (MIR, Forbes Massie и др.)
    │   ├── styles-catalog.md      — каталог визуальных стилей
    │   ├── fal-api.md             — документация fal.ai + troubleshooting
    │   ├── source-prep-guide.md   — как готовить исходники из SketchUp/ArchiCAD
    │   └── source-prep-guide.html — то же, красиво
    └── skills/
        ├── setup/SKILL.md         — интерактивный онбординг нового пользователя
        ├── viz/SKILL.md           — главный скилл: изображение → рендеры
        └── viz-project/SKILL.md   — онбординг нового проекта
```

## Быстрый старт — онбординг

После установки просто напиши в Claude Code:

```
привет
```

или

```
/setup
```

Агент проведёт тебя через:
1. Несколько вопросов про твои задачи (архитектура / интерьеры / HoReCa)
2. Регистрацию на fal.ai и получение ключа (2 минуты)
3. Настройку `.env` с ключом
4. Заполнение профиля студии
5. Тест-рендер чтобы убедиться что всё работает

---

## Установка

### 1. Зависимости

```bash
pip install requests
```

### 2. Ключ fal.ai

Получи API ключ на [fal.ai/dashboard](https://fal.ai/dashboard).

Создай `.env` в корне проекта:

```
FAL_KEY=your_fal_key_here
```

### 3. Подключить агента к Claude Code

Скопируй папку `agent/` в свой проект:

```
your-project/
└── office/agents/visualizer/   ← скопируй сюда содержимое agent/
```

Добавь в корневой `CLAUDE.md` своего офиса:

```
@office/agents/visualizer/core.md
```

## Использование скрипта напрямую

```bash
# Концепт из текста (быстро, 30 сек)
python scripts/viz_render.py --mode concept --count 3 \
  --prompt "cozy restaurant interior, warm amber light, oak and brick, evening"

# ArchiCAD/SketchUp → фотореализм (лучший результат)
python scripts/viz_render.py --mode gpt --count 2 \
  --image model_color.jpg \
  --control model_lineart.jpg \
  --prompt "Convert to photorealistic interior. Preserve exact room layout and all furniture positions."

# Апскейл готового рендера
python scripts/viz_render.py --mode gpt --count 2 \
  --image render.jpg \
  --prompt "Enhance photorealism: detailed textures, volumetric lighting, realistic shadows. Keep geometry unchanged."

# Замена материала с референс-фото
python scripts/viz_render.py --mode gpt --count 2 \
  --image render.jpg \
  --control floor_reference.jpg \
  --prompt "Replace floor with material shown in reference image. Keep everything else identical."
```

## Режимы

| Режим | Модель | Для чего |
|-------|--------|----------|
| `gpt` | GPT Image 2 | ArchiCAD/SketchUp → фотореализм. **Основной режим.** |
| `concept` | Nano Banana 2 | Быстрый набросок атмосферы из текста (~30 сек) |
| `precise` | FLUX + ControlNet | (отключён — хуже GPT для cartoon→photo) |
| `edit` | FLUX Kontext | (отключён) |
| `final` | FLUX Pro Ultra | (отключён) |

## Параметры viz_render.py

| Параметр | Описание |
|----------|----------|
| `--prompt` | Текстовое описание (обязательный) |
| `--image` | Исходное изображение (экспорт модели, рендер) |
| `--control` | Второй файл — референс геометрии или материала |
| `--mode` | Режим генерации (default: concept) |
| `--count` | Количество вариантов (default: 3) |
| `--strength` | Сила трансформации 0.5–1.0 |

## Расширить через MCP

Агент работает из коробки, но становится мощнее с MCP-серверами.

**Минимальный апгрейд (10 минут):**

```bash
# 1. Официальный fal MCP — агент сам выбирает лучшую модель из 1000+ каталога
claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp \
  --header "Authorization: Bearer YOUR_FAL_KEY"

# 2. Показывает рендеры прямо в чате
npm install -g image-viewer-mcp
```

**Стратегически:**
- `tapir-archicad-MCP` — прямой доступ к открытой модели ArchiCAD (читает геометрию, материалы без ручного экспорта)
- `SketchUp Connector` — официальный MCP от Trimble для `.skp`-файлов (апрель 2026)
- `Higgsfield MCP` — видео из рендера: Sora 2, Veo 3.1, Kling 3.0 (flythrough-презентации клиентам)

Полный гайд с установкой → [agent/knowledge/mcp-integrations.md](agent/knowledge/mcp-integrations.md)

---

## Победные промпты

Готовые проверенные промпты — в [agent/memory.md](agent/memory.md):
- Апскейл готового рендера
- Замена материала с референс-фото
- Экстерьер/фасад с двумя файлами
