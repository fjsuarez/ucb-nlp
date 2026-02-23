# El Deber — Web Scraper & NLP Dataset

Scraper para recopilar artículos del diario [El Deber](https://eldeber.com.bo/) (Bolivia) y preparar un dataset para el curso de Procesamiento de Lenguaje Natural.

## Estructura del proyecto

```
├── pyproject.toml             # Proyecto uv con dependencias
├── programa.qmd               # Programa del curso
└── scraper/
    ├── config.py              # Configuración: categorías, delays, rutas
    ├── scrape_links.py        # Paso 1: recopilar URLs de artículos
    ├── scrape_articles.py     # Paso 2: extraer contenido de cada artículo
    ├── prepare_dataset.py     # Paso 3: limpiar y preparar dataset
    └── data/                  # Datos generados (no versionado)
        ├── article_links.jsonl
        ├── articles_raw.jsonl
        ├── eldeber_dataset.jsonl
        ├── eldeber_dataset.csv
        └── eldeber_chunks.jsonl   # (opcional, para RAG)
```

## Instalación

```bash
uv sync
```

## Uso

### Paso 1: Recopilar enlaces de artículos

```bash
# Todas las categorías (pais, economia, deportes, etc.)
uv run scraper/scrape_links.py

# Solo categorías específicas
uv run scraper/scrape_links.py --categories pais economia deportes

# Limitar páginas por categoría (cada página ≈ 30 artículos)
uv run scraper/scrape_links.py --max-pages 5
```

Genera `data/article_links.jsonl` con las URLs descubiertas.

### Paso 2: Descargar contenido de artículos

```bash
# Scrapear todos los enlaces recopilados
uv run scraper/scrape_articles.py

# Limitar a los primeros N artículos (útil para pruebas)
uv run scraper/scrape_articles.py --limit 50

# Si se interrumpe, reanudar sin repetir
uv run scraper/scrape_articles.py --resume
```

Genera `data/articles_raw.jsonl` con el contenido completo.

### Paso 3: Preparar dataset final

```bash
# Limpiar, deduplicar y generar JSONL + CSV
uv run scraper/prepare_dataset.py

# Solo ver estadísticas sin generar archivos
uv run scraper/prepare_dataset.py --stats

# Generar también chunks para RAG (proyecto final)
uv run scraper/prepare_dataset.py --chunked
uv run scraper/prepare_dataset.py --chunked --chunk-size 300 --chunk-overlap 50
```

## Formato del dataset

Cada artículo en `eldeber_dataset.jsonl`:

```json
{
  "id": "a1b2c3d4e5f6",
  "url": "https://eldeber.com.bo/economia/...",
  "title": "Título del artículo",
  "subtitle": "Bajada o descripción corta",
  "date": "2026-02-21T14:45:00",
  "author": "Nombre del Autor",
  "category": "economia",
  "category_label": "Economía",
  "body": "Texto completo del artículo...",
  "tags": ["ECONOMÍA", "YPFB"],
  "word_count": 450,
  "char_count": 2800
}
```

## Chunks para RAG

Con `--chunked`, se genera `eldeber_chunks.jsonl`:

```json
{
  "chunk_id": "a1b2c3d4e5f6_0",
  "article_id": "a1b2c3d4e5f6",
  "url": "https://eldeber.com.bo/economia/...",
  "title": "Título del artículo",
  "date": "2026-02-21T14:45:00",
  "category": "Economía",
  "author": "Nombre del Autor",
  "chunk_index": 0,
  "total_chunks": 3,
  "text": "Texto del fragmento..."
}
```

Cada chunk incluye la metadata del artículo original, lo que es ideal para RAG dado que el chatbot puede citar la fuente (URL, título, fecha, autor).

## Uso en el curso

| Semana | Tarea | Cómo usar el dataset |
|:------:|-------|----------------------|
| 1 | Preprocesamiento | Tokenización, lematización, regex sobre `body` |
| 2 | BoW, TF-IDF | Representación vectorial usando `body` y `category_label` |
| 4 | **Tarea 1: Sentimiento** | Clasificación con TF-IDF sobre artículos por categoría |
| 10 | Fine-tuning BERT | Clasificación de noticias con `category_label` |
| 12 | **Tarea 3: BERT** | Fine-tuning para clasificación usando el dataset |
| 13 | NER | Extracción de entidades nombradas del `body` |
| 16 | **Tarea 4: RAG** | Usar `eldeber_chunks.jsonl` como knowledge base |
| 19-20 | **Proyecto final** | Chatbot RAG con citación de fuentes |

## Categorías disponibles

| Categoría | Etiqueta | Contenido |
|-----------|----------|-----------|
| `pais` | País | Política nacional, gobierno |
| `economia` | Economía | Negocios, finanzas, agricultura |
| `santa-cruz` | Santa Cruz | Noticias locales de Santa Cruz |
| `deportes` | Deportes | Fútbol, deportes varios |
| `mundo` | Mundo | Noticias internacionales |
| `opinion` | Opinión | Columnas de opinión, editoriales |
| `sociales` | Sociales | Eventos sociales, entretenimiento |
| `cultura-y-entretenimiento` | Cultura | Arte, música, cine |
| `salud-y-bienestar` | Salud | Salud, nutrición |
| `educacion-y-sociedad` | Educación | Educación, universidades |
| `futbol` | Deportes | Fútbol boliviano |

## Notas

- El scraper incluye delays aleatorios entre peticiones (1–3s) para ser respetuoso con el servidor
- Se recomienda ejecutar durante horarios de baja demanda
- Los datos se guardan incrementalmente, por lo que se puede interrumpir y reanudar
- El dataset se genera exclusivamente con fines educativos para el curso de NLP
