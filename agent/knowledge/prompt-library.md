# Библиотека архитектурных промптов

Шаблоны под три сегмента Folk Studio. Заполняй [ПЕРЕМЕННЫЕ] из viz-context.md проекта.

---

## Структура хорошего архитектурного промпта

```
[ТИП ИЗОБРАЖЕНИЯ] [ОБЪЕКТ] [МАТЕРИАЛЫ] [СВЕТ] [АТМОСФЕРА] [СТИЛЬ СЪЁМКИ] [КАЧЕСТВО]
```

**Правило:** каждое слово зарабатывает своё место. Нет "красиво", "уютно", "современно" — только конкретика.

---

## СЕГМЕНТ 1: ЖИЛОЕ

### Интерьер — жилая гостиная

```
architectural interior photography, [СТИЛЬ: scandinavian / japandi / wabi-sabi / mediterranean],
living room, [МАТЕРИАЛ_ПОЛ: oak herringbone parquet / concrete polished / travertine tiles],
[МАТЕРИАЛ_СТЕНЫ: white plaster / exposed concrete / lime wash / natural wood cladding],
[МЕБЕЛЬ: linen sofa / leather armchair / built-in bookshelves],
[СВЕТ: soft morning light through floor-to-ceiling windows / warm evening ambient /
overcast diffused daylight], [ВРЕМЯ: golden hour 17:00 / morning 9:00],
inhabited minimalism, human presence, fresh flowers on coffee table,
Hasselblad H6D, 35mm lens, f/4, architectural magazine quality,
ultra-realistic, 8K resolution
```

### Интерьер — жилая спальня

```
architectural interior photography, bedroom, serene atmosphere,
[МАТЕРИАЛ: linen bedding / natural wood headboard / terrazzo floor],
[СВЕТ: soft morning diffused light / bedside warm glow / moonlight through sheer curtains],
tactile materials, layered textiles, minimal clutter,
Leica Q2 Monochrom, 28mm wide, lifestyle photography,
ultra-realistic photorealistic render
```

### Экстерьер — частный дом

```
architectural photography, residential house exterior,
[МАТЕРИАЛ_ФАСАД: board-formed concrete / dark cedar cladding / white plastered / brick],
[ОЗЕЛЕНЕНИЕ: mature oak trees / ornamental grass / hedge / lavender garden],
[СВЕТ: overcast soft daylight / golden hour sunset / blue hour dusk],
contextual surroundings, human scale with person entering,
Hasselblad medium format, wide angle 24mm, MIR studio style,
photorealistic, award-winning architectural photography
```

---

## СЕГМЕНТ 2: HoReCa (ресторан, отель, спа)

### Ресторан — зал

```
architectural interior photography, restaurant dining room,
[КОНЦЕПЦИЯ: fine dining / casual bistro / industrial loft / mediterranean terrace],
[МАТЕРИАЛ_ПОЛ: herringbone terracotta / polished concrete / dark oak],
[МАТЕРИАЛ_СТЕНЫ: exposed brick / zellige tiles / textured plaster / panelled wood],
[МЕБЕЛЬ: natural rattan chairs / leather banquettes / marble-top tables],
warm evening ambient light, pendant lamps casting pools of light,
guests dining, atmospheric, Forbes Massie style,
Architectural Digest quality, 50mm lens, f/2.8, ultra-realistic
```

### Спа / велнес

```
architectural interior photography, luxury spa interior,
[ТИП: hammam / japanese onsen / nordic sauna / meditation room],
[МАТЕРИАЛ: tadelakt plaster / cedar wood / black slate / travertine],
[СВЕТ: candles and low ambient / zenithal skylight / steam-diffused light],
tranquil atmosphere, water element, human figure for scale,
sensory experience render, Neoscape style,
ultra-realistic photorealistic, 8K, magazine quality
```

### Отель — лобби / reception

```
architectural interior photography, boutique hotel lobby,
[СТИЛЬ: contemporary / art deco revival / wabi-sabi / mediterranean],
[МАТЕРИАЛ: marble floors / sculptural reception desk / feature wall],
[СВЕТ: natural light through grand windows / dramatic pendant installation],
guests arriving, concierge present, sense of arrival,
Dbox studio lifestyle approach, warm and welcoming,
Wallpaper* magazine quality, 24mm, ultra-realistic
```

---

## СЕГМЕНТ 3: РЕСТАВРАЦИЯ / НАСЛЕДИЕ

### Интерьер исторического здания

```
architectural interior photography, heritage building interior restoration,
[ТИП: 19th century apartment / industrial loft conversion / manor house / merchants house],
preserved [ЭЛЕМЕНТ: ornate ceiling / original parquet / arched windows / stone walls],
contemporary intervention [ЧТО НОВОЕ: minimal furniture / glass partition / steel staircase],
dialogue between old and new, patina and age as beauty,
[СВЕТ: raking sunlight revealing texture / soft diffused heritage lighting],
historical authenticity, Forbes Massie contextual approach,
Leica M10, 28mm, architectural documentary style, ultra-realistic
```

### Фасад — реставрация

```
architectural photography, building facade restoration,
[ПЕРИОД: neoclassical / constructivist / art nouveau / stalinist],
[МАТЕРИАЛ: restored stucco / cleaned brick / repaired stone / original details],
before-and-after quality reveal, respectful intervention,
contextual street setting, warm afternoon light raking across texture,
photorealistic, urban context, heritage preservation photography
```

---

## ANTI-SLOP GUARD (добавлять всегда в конец промпта)

```
NOT: glossy CGI render, artificial lighting, generic furniture, stock photo style,
overly saturated, plastic materials, empty soulless space, generic interior design,
futuristic unrealistic, AI-generated look
```

---

## Быстрые модификаторы (добавлять к любому промпту)

| Что хочешь | Добавить в промпт |
|-----------|------------------|
| Теплее | `warm amber tones, honey-colored light` |
| Холоднее | `cool north light, silver tones, morning clarity` |
| Минималистичнее | `essential elements only, negative space, breathing room` |
| Уютнее | `layered textiles, soft shadows, inhabited warmth` |
| Монументальнее | `grand scale, dramatic ceiling height, architectural gravitas` |
| Мягче свет | `overcast diffused, no hard shadows, soft wrap-around light` |
| Драматичнее | `chiaroscuro, strong shadows, single light source` |
| Летнее | `summer light, open windows, breeze implied` |
| Осеннее | `golden autumn light, warm palette, dry leaves visible` |
