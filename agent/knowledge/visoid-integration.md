# Visoid — интеграция и workflow

Visoid — AI-рендеринг специально для архитектуры. Сильные стороны: ArchiCAD/SketchUp/Revit/Rhino плагины, загрузка .DAE/.GLB напрямую, хорошее сохранение геометрии, 4K вывод.

**API:** REST, ключ на `app.visoid.com/docs`  
**MCP:** нет  
**Сайт:** visoid.com

---

## Вариант А — скрипт viz_render.py

Добавлен режим `--mode visoid` в `scripts/viz_render.py`.

**Требования:**
```
VISOID_KEY=твой_ключ  # в .env
```

**Примеры:**

```bash
# Из скриншота модели
python scripts/viz_render.py --mode visoid --count 2 \
  --image model_screenshot.jpg \
  --prompt "photorealistic interior, warm oak, concrete ceiling, evening light"

# Из 3D-модели напрямую (.DAE из ArchiCAD, .GLB из SketchUp)
python scripts/viz_render.py --mode visoid --count 2 \
  --image model_export.dae \
  --prompt "photorealistic render, preserve exact geometry, natural materials"

# Только из текста
python scripts/viz_render.py --mode visoid --count 3 \
  --prompt "modern HoReCa interior, restaurant, warm amber light, oak and brick"
```

**Если получаешь 422 ошибку:**
Зайди на `app.visoid.com/docs` → проверь:
1. Точный URL endpoint (обнови `VISOID_API_URL` в скрипте)
2. Название поля для изображения (`image` / `image_url` / `file`)
3. Доступные параметры стиля (`style` / `preset` / `material`)

---

## Вариант Б — ArchiCAD Add-On (встроенный workflow)

Самый быстрый путь: кнопка прямо внутри ArchiCAD, без скриптов.

### Установка

1. Зайди на `visoid.com/render/archicad`
2. Скачай Add-On под свою версию ArchiCAD (26/27)
3. Установи: `Options → Add-On Manager → Load Add-On`
4. Перезапусти ArchiCAD

### Использование

```
1. Открой вид (план, разрез, 3D)
2. Нажми вкладку Visoid в боковой панели
3. Авторизуйся (email/пароль от app.visoid.com)
4. Введи промпт стиля
5. Нажми Render → результат в браузере через ~30 сек
```

### Экспорт для нашего скрипта

Если нужна дополнительная обработка через GPT Image 2 или FLUX:

```
В ArchiCAD: File → Save a Copy As → .DAE (Collada) или .GLB
Потом:
python scripts/viz_render.py --mode gpt --image exported.dae \
  --prompt "finish render, add materials, photorealistic..."
```

---

## Когда что использовать

| Задача | Инструмент |
|--------|-----------|
| Быстрый концепт для клиента | `--mode visoid` (Add-On прямо из ArchiCAD) |
| Максимальный контроль промпта | `--mode gpt` (GPT Image 2 через fal.ai) |
| Замена конкретного материала по референсу | `--mode gpt` с двумя изображениями |
| Финальный рендер 4K для Behance/презентации | `--mode visoid` или `--mode final` |
| Дешёвые итерации на этапе эскиза | `--mode concept` |

---

## Цены Visoid (актуально на июнь 2026)

| Plan | $/мес | Кредиты | Разрешение |
|------|-------|---------|------------|
| Free | 0 | базовые | 1K |
| Pro | 29 | 500/мес | 2K + видео |
| Premium | 79 | 2000/мес | 4K + 3D upload |

Для тестирования: Free plan → достаточно для 20-30 рендеров.

---

## Известные ограничения

- Иногда меняет цвет отдельных объектов (компенсируй через `--mode edit` потом)
- Мелкие детали (раковины, декоративные элементы) могут выглядеть неубедительно
- Нет офлайн-режима — нужен интернет
- Кредиты кончаются быстрее чем кажется при интенсивной итерации
