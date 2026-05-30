# fal.ai — API документация + актуальные модели (обновлено 2026-04-25)

## Ключ

Хранится в `.env` → `FAL_KEY`. Никогда не вставлять в код напрямую.

---

## ВАЖНО: Nano-banana — что это на самом деле

Nano-banana — **не диффузионная модель**. Это Google Gemini Image:
- Nano Banana = Gemini 2.5 Flash Image
- Nano Banana 2 = Gemini 3.1 Flash Image
- Nano Banana Pro = Gemini 3 Pro Image

**Почему не работает для точного рендера из wireframe:**
ControlNet архитектурно невозможен для этой модели. Когда подаёшь wireframe в img2img — она воспринимает его как *подсказку*, не как жёсткое ограничение геометрии. Итог: красиво, но не тот проект.

**Когда nano-banana полезен:**
- Концептуальная идеация (быстрые атмосферы)
- Nano Banana Pro читает планы как архитектурную инструкцию
- Небольшие редактуры готовых изображений

**Когда nano-banana НЕ подходит:**
- Точное воспроизведение геометрии из SketchUp
- Контроль конкретных материалов и их размещения
- Финальный рендер "как в портфолио"

---

## Актуальная таблица моделей для архитектуры

| Endpoint | Что делает | Для чего |
|---|---|---|
| `fal-ai/flux-general/image-to-image` | FLUX.1 Dev + ControlNet img2img | **Главный инструмент** — точный рендер с контролем геометрии |
| `fal-ai/flux-general` | FLUX.1 Dev + ControlNet txt2img | Концепт из промпта с геометрическим контролем |
| `fal-ai/flux-pro/v1.1-ultra` | FLUX Pro максимальное качество | Финальные презентационные рендеры |
| `fal-ai/flux-kontext-pro` | Редактирование конкретных зон | Точечные правки (поменять цвет стены) |
| `fal-ai/nano-banana-pro` | Gemini 3 Pro, читает планы | Концептуальная идеация, чтение планов с клиентом |
| `fal-ai/nano-banana-2` | Gemini 3.1 Flash, быстрее | Быстрые итерации идей |
| `fal-ai/nano-banana/edit` | Gemini img2img | Мелкие редактуры готовых изображений |

---

## Главный рабочий запрос: FLUX img2img + ControlNet

```json
{
  "image_url": "[clean SketchUp monochrome render или depth map]",
  "prompt": "architectural exterior visualization, [материалы], [свет], professional architectural photography, 8K",
  "num_inference_steps": 30,
  "guidance_scale": 3.5,
  "strength": 0.65,
  "controlnets": [{
    "path": "InstantX/FLUX.1-dev-Controlnet-Canny",
    "control_image_url": "[lineart экспорт из SketchUp]",
    "conditioning_scale": 0.7
  }]
}
```

**Параметры для архитектуры:**
- `guidance_scale`: 3.5 (FLUX работает на низких значениях, не 7-12 как SD)
- `strength`: 0.60–0.75 (ниже = ближе к геометрии источника)
- `steps`: 28–35
- ControlNet `conditioning_scale`: 0.65–0.80

**Ограничение:** fal.ai поддерживает только ОДИН ControlNet за запрос.
Обходной путь: два прохода — сначала depth (0.7), потом lineart как img2img (0.4–0.5).

---

## Правильный пайплайн SketchUp → FLUX

**Шаг 1 — два экспорта одного вьюпорта:**
- Вид с линиями без текстур → **Lineart источник** для ControlNet Canny
- Вид Monochrome + Fog/Depth style → **Depth approximation** для ControlNet Depth

**Шаг 2 — запрос:**
- Endpoint: `fal-ai/flux-general/image-to-image`
- Источник: monochrome рендер (depth approximation)
- ControlNet: lineart экспорт, conditioning_scale 0.70
- strength: 0.65

**Шаг 3 — постобработка:**
- Adobe Firefly Generative Fill — убрать артефакты
- Цветокоррекция в Lightroom/Camera Raw

---

## PowerShell запрос (рабочий шаблон)

```powershell
$FAL_KEY = $env:FAL_KEY  # из .env
$headers = @{
    "Authorization" = "Key $FAL_KEY"
    "Content-Type"  = "application/json"
}

$body = @{
    image_url            = "data:image/jpeg;base64,..."  # ваш SketchUp render
    prompt               = "architectural exterior..."
    num_inference_steps  = 30
    guidance_scale       = 3.5
    strength             = 0.65
    controlnets          = @(@{
        path               = "InstantX/FLUX.1-dev-Controlnet-Canny"
        control_image_url  = "data:image/jpeg;base64,..."  # lineart
        conditioning_scale = 0.70
    })
} | ConvertTo-Json -Depth 4

$resp = Invoke-RestMethod -Uri "https://fal.run/fal-ai/flux-general/image-to-image" `
    -Method POST -Headers $headers -Body $body -TimeoutSec 180
$resp.images[0].url
```

---

## Troubleshooting

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `401 Unauthorized` | Неверный ключ | Проверь FAL_KEY в .env |
| `402 Payment Required` | Нет кредитов | Пополни на fal.ai/dashboard |
| Геометрия плывёт | strength слишком высокий | Снизь до 0.55–0.65 |
| Игнорирует промпт | guidance_scale слишком низкий | Подними до 5–7 |
| Нет ControlNet support | Неверный endpoint | Используй flux-general, не nano-banana |
| Материалы "галлюцинируют" | Нет depth source | Сделай monochrome export из SketchUp |

---

## Альтернативы без API (для Folk Studio)

**Veras (SketchUp плагин)** — [evolvelab.io/veras](https://www.evolvelab.io/veras)
- Работает прямо в SketchUp, не нужен API
- Захватывает вьюпорт, держит геометрию
- Параметр "Geometry override" — насколько строго следовать модели
- ~$49/мес, есть триал
- Лучший выбор для быстрого старта

**ComfyUI + RealArchvis XL** — для максимального контроля (локально или облако)
- Checkpoint: RealArchvis XL v5.0 (Civitai)
- Двойной ControlNet: Depth (0.75) + Lineart (0.60)
- SD/SDXL guidance: 7–9, steps: 28–35
