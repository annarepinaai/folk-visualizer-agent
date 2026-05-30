# AI-стеки для архитектурной визуализации — Исследование 2025

*Дата: 2026-04-25. Источник: глубокий поиск по Reddit, Civitai, CGArchitect, Architizer, студиям.*

---

## Правда о nano-banana

Nano-banana — это Google Gemini Image (НЕ диффузионная модель):
- Nano Banana = Gemini 2.5 Flash Image
- Nano Banana 2 = Gemini 3.1 Flash Image  
- Nano Banana Pro = Gemini 3 Pro Image

**Почему не работает для wireframe → точный рендер:** ControlNet архитектурно невозможен. Модель видит wireframe как подсказку, не как жёсткое ограничение. Геометрия плывёт всегда.

**Nano-banana полезен для:** концептуальной идеации, Nano Banana Pro читает планы, мелкие редактуры готовых рендеров.

---

## Что используют топовые студии мира

По опросу Chaos + Architizer (1000+ дизайнеров, 2024):
- 72.88% визуализаторов используют AI
- 62.43% считают AI ещё не готовым к полноценному production
- Реальное ускорение: 20–35% (не рекламные 80–90%)

**Brick Visual** (Будапешт): AI как усилитель постпродакшна, не замена. Используют Pulze Scene Manager + Project Dream.

**DBOX** (Нью-Йорк): Chaos Arena (ray-tracing в реальном времени). Не открытые AI-инструменты.

**Neoscape** (Бостон): Unreal Engine 5 + RealityCapture. «AI — соавтор, не создатель».

**Ravelin3D**: Chaos Vantage с AI-denoising + Adobe Firefly для постпродакшна + Veras для концептов.

**Общий паттерн:** AI в постпродакшне и концептуальной фазе, НЕ в "wireframe → финал" одним шагом.

---

## ТОП-3 рабочих стека

### 1. Veras + SketchUp (минимальный порог, старт за день)

**Плагин:** [evolvelab.io/veras](https://www.evolvelab.io/veras), ~$49/мес, есть триал.
**Работает прямо в SketchUp** — захватывает вьюпорт, держит геометрию.
- Geometry override слайдер — контроль следования геометрии
- Не нужен API, не нужен Python

**Пайплайн:** SketchUp вьюпорт → написать промпт в Veras → geometry strength 70% → итерация.

**Лучший первый шаг для Folk Studio.**

---

### 2. FLUX.1 Dev + ControlNet через fal.ai (качество + контроль)

**Endpoint:** `fal-ai/flux-general/image-to-image`

**Пайплайн SketchUp → FLUX:**
1. Экспорт с линиями без текстур → Lineart для ControlNet Canny
2. Экспорт Monochrome + Fog → приближение Depth map
3. fal.ai: depth как ControlNet вход, strength 0.65, guidance 3.5

**Параметры:**
- `guidance_scale`: 3.5 (FLUX, не SD — низкие значения)
- `strength`: 0.60–0.75
- `steps`: 28–35
- ControlNet `conditioning_scale`: 0.65–0.80

ControlNet модели для FLUX: `InstantX/FLUX.1-dev-Controlnet-Canny`, `XLabs-AI/flux-controlnet-collections`

---

### 3. ComfyUI + RealArchvis XL (максимальный контроль, локально)

**Checkpoint:** RealArchvis XL v5.0 (Civitai) — специально для архвиза.

**Двойной ControlNet:**
- Depth (Depth-Anything препроцессор): weight 0.75–0.85
- Lineart (AnyLine): weight 0.50–0.65

**Параметры:** CFG 5–7 (SDXL), steps 25–35, denoise 0.60–0.75.

Порог входа высокий — не первый шаг.

---

## Иерархия источников (что лучше подавать на вход AI)

1. **Готовый 3D рендер без текстур** — AI имеет точную геометрию и глубину ✅✅✅
2. **Depth map + edge export из SketchUp** — хороший ControlNet input ✅✅
3. **Фото существующего объекта** — для реставрации/редизайна ✅✅
4. **Sketch/wireframe** — наименее контролируемый результат ✅

---

## Курсы

### Международные:
- **PAACADEMY "Generative Architecture with AI 2.0"** — преподаватель из MVRDV, SD+FLUX для архитекторов [paacademy.com](https://paacademy.com/course/generative-architecture-with-ai-2-0-sd-flux)
- **PAACADEMY "The Diffusion Architect 3.0: Flux Era"** — продвинутый [paacademy.com](https://paacademy.com/course/the-diffusion-architect-3-0-flux-era)
- **Udemy "Master Stable Diffusion — Architecture & Interior AI"** — ForgeUI + FLUX + ControlNet

### Русскоязычные:
- **МАРШ "Нейросети в архитектуре"** — [march.ru](https://march.ru/courses/neural-networks-in-architecture/)
- **art.brodsky AI Intensive** — 15 мастер-классов [artbrodsky.ru](https://artbrodsky.ru/ai-intensive)

### Бесплатно:
- Civitai Education — ["Guide to ControlNet"](https://education.civitai.com/civitai-guide-to-controlnet/)
- [3ddd.ru — AI для архитектурной визуализации](https://3ddd.ru/blog/post/ai-dlia-arkhitekturnoi-vizualizatsii-razlozhil-po-polkam)

---

## Рекомендации для Folk Studio

**Сейчас (эта неделя):** установить Veras в SketchUp — первые точные рендеры за день без API.

**Следующий шаг:** перейти на `fal-ai/flux-general/image-to-image` с ControlNet вместо nano-banana.

**Для концептов с клиентом:** nano-banana Pro оставить — он читает планы и быстро даёт атмосферу.

**Не трогать пока:** ComfyUI локально — слишком высокий порог для старта.

**Курс:** PAACADEMY "Generative Architecture with AI 2.0" — системное понимание вместо экспериментов.
