# Визуализатор — Memory (append-only)

## Studio Profile

**Специализация:** архитектура, дизайн интерьеров, объекты
**Сегменты:** жилое / HoReCa / реставрация
**Стиль студии:** [заполнится после первых проектов]
**Предпочитаемые материалы:** [заполнится]
**Референсные студии:** [заполнится]

## Активные проекты

| Проект | Тип | Контекст | Статус |
|--------|-----|----------|--------|
| — | — | — | — |

## Visual Patterns
(что заходит — появится после первых сессий)

## Prompt Learnings

### Рабочая связка: 3D-модель → фотореализм

**Лучший режим для ArchiCAD/SketchUp → фотореализм:**
- Режим: `gpt` (GPT Image 2 через fal.ai endpoint `openai/gpt-image-2/edit`)
- Файлы: цветной экспорт из ArchiCAD + "Видимые рёбра" (Hidden Line) из того же ракурса
- Результат: фотореализм + геометрия держится лучше всех протестированных режимов

**FLUX-режимы исключены:**
- precise, edit, final — не справляются с cartoon→photo трансформацией ArchiCAD-моделей
- Даже на strength 0.40 меняют геометрию непредсказуемо

### Победный промпт — апскейл готового рендера

```
Upscale this interior render to 2x resolution with maximum photorealism. Enhance in these specific ways: (1) add ultra-detailed material textures — visible wood grain, fabric weave, stone pores, matte paint microstructure; (2) add volumetric lighting — light rays from fixtures, soft glow halos around ceiling lamps, warm light pools on surfaces, realistic shadows with penumbra; (3) add material edge detail — subtle shadow lines at material joints, baseboards, door frames, tile grout; (4) add surface imperfections — slight wall texture variation, minor reflection irregularities that make it look photographed not rendered. Keep the overall room layout, furniture placement, camera angle and major geometry intact. Small micro-adjustments to geometry detail (sharper corners, realistic material thickness at edges) are welcome if they increase realism.
```

Запуск: `--mode gpt --image render.jpg --count 2`

### Победный промпт — замена материалов с референс-фото

```
Transform this [bedroom/living room/etc.] render into a photorealistic interior photograph. Replace the floor with the exact flooring shown in the reference image — [описать текстуру]. Wall surfaces: replace with [описать стены]. Keep the overall room layout, furniture, color palette and proportions close to the original — small adjustments to lighting, shadows and material realism are welcome. Add: realistic fabric texture on upholstered furniture, warm soft glow from [источники света], photorealistic shadows and light pools on floor. Hasselblad H6D medium format, 28mm lens, f/8, Architectural Digest quality, 4K resolution.
```

Запуск: `--mode gpt --image source_render.jpg --control material_reference.jpg --count 2`

**Паттерн:** референс фото материала как второй файл (`--control`) = GPT Image 2 считывает стиль и применяет точнее чем словесное описание.

### Победный промпт — экстерьер с двумя файлами

Запуск: `--mode gpt --image lineart.jpg --control material_reference.jpg`

**Паттерн:** линейный чертёж как основной (`--image`) + фото материалов как референс (`--control`) = хорошее сохранение геометрии + правильная текстура.

### Материальные находки для промптов

- `cement-sand flat-profile tiles` + `drip edge flashing fascia` + `forged wrought iron balustrade` → кованая европейская атмосфера
- `slim-format clinker brick thin horizontal courses 5cm height` → ригельный кирпич
- txt2img не держит прямоугольный план (даёт восьмиугольник/круг) — для точной геометрии нужен img2img
