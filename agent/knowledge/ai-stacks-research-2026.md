# AI-визуализация в архитектуре — Исследование апрель 2026

*Источники: CGArchitect forums, Chaos/Architizer survey, PAACADEMY, Brick Visual, Ravelin3D, Softculture, fal.ai, Reddit, Domestika*

---

## Реальное положение дел (данные опросов)

**Chaos + Architizer State of ArchViz 2025** (1000+ дизайнеров):
- 44% используют AI для концептов и ранних идей
- 35% создают быстрые вариации дизайна
- Только 11% фирм формально интегрировали AI в основной workflow
- Реальная экономия времени: **20-35%**, не 80-90% из маркетинга (Ravelin3D)

**Честная цитата от Brick Visual** (ведущая студия мира):
> "Реальное применение AI в производстве — лишь несколько процентов. 99% творческого процесса по-прежнему ручная работа."

---

## Рабочие стеки — матрица задач

| Инструмент | Задача | Скорость | Контроль геометрии | Порог входа | Стоимость |
|-----------|--------|----------|-------------------|-------------|-----------|
| **Midjourney V7** | Концепты, mood | 30-60 сек | Низкий | Низкий | $10-120/мес |
| **FLUX Dev + ControlNet** | Скетч→рендер | 10-15 сек | Высокий | Высокий | Бесплатно + GPU |
| **FLUX Kontext** | Редактирование рендера | 3-5 сек | Средний | Средний | Облако |
| **Veras (SketchUp плагин)** | BIM→AI рендер | 20-30 сек | Высокий (из модели) | Низкий | Подписка Chaos |
| **D5 Render** | Реалтайм + AI атмосфера | Реалтайм | Максимальный | Средний | Подписка |
| **V-Ray + AI деноизер** | Финальный рендер | -70% времени | Максимальный | Низкий | В V-Ray |
| **Adobe Firefly** | Постпродакшн | 5-10 сек | N/A | Низкий | В Photoshop |
| **fal.ai Nano Banana** | API-интеграция | 30 сек | Средний | Высокий (API) | $0.03-0.1/img |

---

## Стек A: Midjourney V7 — концепты и клиентские презентации

**Когда использовать:** ранняя стадия проекта, поиск направления, материалы для Behance/соцсетей

**Что нового в V7 (апрель 2025):**
- Draft Mode: ~10x быстрее и ~50% дешевле
- Персонализация через рейтинг 200 пар изображений
- Видеогенерация из изображений

**Шаблон промта для Folk Studio:**
```
Architectural interior photography, warm residential living space,
exposed timber beams, tadelakt plaster walls warm beige tone,
travertine flooring herringbone pattern, afternoon light through
tall windows, Scandinavian-folk warmth, minimalist composition,
shot on Phase One XF IQ4, 8K photorealistic,
architectural magazine quality, --ar 16:9 --style raw --v 7
```

**Ограничения:** слабый контроль конкретной геометрии, нельзя "сохранить эту стену"

---

## Стек B: FLUX.1 Dev + ControlNet — контролируемые рендеры

**Когда использовать:** конвертация скетчей и 3D-моделей в фотореализм, эксперименты с материалами при фиксированной форме

**Версии FLUX:**
| Версия | Скорость | Когда |
|--------|----------|-------|
| FLUX Schnell | ~2 сек | Быстрые черновики |
| FLUX Dev | ~10-15 сек | Основная работа + ControlNet |
| FLUX Pro Ultra | Облако | Финальные 4K клиентские рендеры |
| **FLUX Kontext Dev** | ~5 сек | Редактирование: меняй материал/стиль сохраняя сцену |
| **FLUX.2** (ноябрь 2025) | Облако | Multi-reference (до 10 источников), 4 мегапикселя |

**Правильные параметры для FLUX (НЕ как Stable Diffusion!):**
- `guidance_scale`: **3.5–7.0** (не 7.5–15 как SD)
- `strength` для img2img: **0.60–0.75**
- `steps`: **28–35**
- ControlNet `conditioning_scale`: **0.65–0.80**

**Pipeline для архитектуры:**
```
1. Depth ControlNet (0.75–0.85) — сохраняет объём и пространство
2. Canny ControlNet (0.60–0.65) — сохраняет границы и детали
3. FLUX Dev как основная модель
4. strength 0.65 — баланс между источником и стилизацией
```

**Путь через fal.ai (без ComfyUI):** `fal-ai/flux-general/image-to-image` + ControlNet

---

## Стек C: Veras (EvolveLAB / Chaos) — для SketchUp пользователей

**Когда использовать:** есть 3D-модель в SketchUp/Revit/Rhino, нужно быстро показать клиенту варианты

**Как работает:**
1. Открываешь проект в SketchUp
2. Veras захватывает текущий viewport
3. Промт: "скандинавский интерьер, дерево, штукатурка"
4. AI рендер за 20-30 секунд, геометрия сохранена
5. Итерируешь не выходя из SketchUp

**Veras 4.0 (2025):** работает на Nano Banana Pro (Gemini 3 Pro) — выше качество, меньше артефактов

---

## Стек D: FLUX Kontext — редактирование готовых рендеров

**Killer feature для Folk Studio:**
- "Сделай эту стену из дуба" → меняет только стену, остальное сохраняется
- "Измени освещение на вечернее"
- Скорость: 3-5 секунд

**ComfyUI workflow:** [docs.comfy.org/tutorials/flux/flux-1-kontext-dev](https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev)

---

## Стек E: Adobe Firefly — постпродакшн

**Когда использовать:** после финального рендера, убрать артефакты, заменить небо, добавить растительность

**Pipeline:**
```
Готовый рендер →
Photoshop + Firefly Generative Fill:
  — Выделить небо → "dramatic sunset sky"
  — Убрать строительный мусор
  — Добавить средиземноморский сад
→ Готово за 10-15 минут
```

**Доступен:** если есть Photoshop — Firefly включён

---

## Топовые студии — что они делают с AI

**Brick Visual** (Будапешт): собственный AI-ассистент для вдохновения + финальных деталей. Принципиально: 99% — ручная работа специалистов.

**Neoscape** (Бостон): Unreal Engine 5 + RealityCapture, AI как часть tech-стека. "AI — соавтор, не создатель."

**Ravelin3D**: Chaos Vantage + AI-denoising + Firefly для постпродакшн + Veras для концептов.

**Общий паттерн всех топ-студий:** AI в постпродакшне и концептуальной фазе, **не** как "wireframe → финал одним шагом".

---

## Курсы — рейтинг по практичности

### Приоритет 1 — для Folk Studio сейчас

**Domestika — AI for Architectural and Interior Visualization with ComfyUI**
- Ведёт: Mohamed Abdellatif (архитектор, Гонконг)
- Облачный ComfyUI через RunningHub (не нужна мощная GPU)
- Специально для архитекторов без технического бэкграунда
- [domestika.org](https://www.domestika.org/en/courses/6458-ai-for-architectural-and-interior-visualization-with-comfyui)

**PAACADEMY — The Diffusion Architect 3.0: Flux Era**
- Ведёт: Ismail Seleit (Foster + Partners)
- ComfyUI + FLUX Schnell/Dev/Kontext + ControlNet + Kling AI (видео)
- 100 EUR, 2 дня, 8 часов, Zoom
- [paacademy.com](https://paacademy.com/course/the-diffusion-architect-3-0-flux-era)

### Русскоязычные

**Softculture — Нейросети. Прототипирование архитектуры**
- Midjourney + PromeAI + постпродакшн, для архитекторов
- [softculture.cc](https://softculture.cc/courses/architects/artificial-intel)

**Softculture — Stable Diffusion для тестирования идей и работы с рендером**
- [softculture.cc](https://softculture.cc/courses/interior-design/stable-diffusion)

**МАРШ — Нейросети в архитектуре**
- Техническое понимание + промтинг + документация
- [march.ru](https://march.ru/courses/neural-networks-in-architecture/)

### Удеми (бюджетно)

- [AI Visualization: FLUX Kontext in Architecture](https://www.udemy.com/course/ai-visualization-course-flux-kontext-in-architecture/)
- [MidJourney for Architects 2026 (A-Z)](https://www.udemy.com/course/midjourney-for-architects-2025-project-based-ai-design-a-z/)

---

## Emerging tools 2025 — что набирает traction

**FLUX Kontext Dev** — главный новый инструмент. Меняешь материалы в готовом рендере текстом за 5 сек.

**FLUX.2** (ноябрь 2025) — multi-reference: до 10 источников-изображений. "Сделай как у проекта 1, с материалами из проекта 2, в свете из проекта 3."

**Kling AI** — image-to-video: статичный рендер → анимация (панорамирование, смена света, люди). Без 3D-анимации.

**Hunyuan 2.5** — 2D-изображение → 3D-модель. Связка: концепт в FLUX → 3D → обратно в рендер.

---

## Форумы и сообщества для мониторинга

| Площадка | Что там |
|----------|---------|
| [CGArchitect Forums](https://forums.cgarchitect.com/topic/80127-ai-in-arch-viz/) | Профессиональные архвиз обсуждения |
| Reddit r/StableDiffusion | Реальные workflow, ControlNet примеры |
| Reddit r/architecture | AI с позиции практикующих |
| [Civitai](https://civitai.com) | Архитектурные LoRA и чекпоинты |
| [Softculture Blog](https://softculture.cc/blog/entries/articles/comparing-ai-testdrive) | Русский тест-драйв инструментов |
| [Brick Academy](https://academy.brickvisual.com) | Материалы от ведущей студии |

---

## Рекомендации для Folk Studio — что делать когда

### Сейчас (этот месяц, 0 технических знаний)
1. **Midjourney V7** ($30/мес) — концепты для лендинга, Behance, клиентских презентаций
2. **Veras в SketchUp** — если есть 3D-модели, быстрые вариации с клиентом в реальном времени
3. **Adobe Firefly** — постпродакшн готовых рендеров (если есть Photoshop)

### 1-3 месяца (освоение контролируемого pipeline)
- Пройти курс Abdellatif на Domestika (облачный, без GPU)
- Освоить FLUX Dev + ControlNet для точного контроля геометрии
- Создать первую LoRA под стиль Folk Studio

### 3-6 месяцев (конкурентное преимущество)
- FLUX Kontext: редактирование материалов в клиентских сессиях
- FLUX.2 Multi-reference: собирать рендеры из нескольких референсных проектов студии
- Kling AI: анимации из статичных рендеров для презентаций

---

*Обновить через 3 месяца. Инструменты меняются быстро.*
