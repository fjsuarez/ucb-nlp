# Proceso: Crear, Renderizar y Publicar Slides

Checklist para cada nueva sesión de slides. Seguir en orden.

---

## 1. Crear el archivo `.qmd`

**Ubicación:** `slides/semanaN/sX_topic.qmd`

**Naming convention:** `s{sesión}_{tema_en_snake_case}.qmd`  
Ejemplos: `s1_ngram_lm.qmd`, `s2_perplejidad_suavizado.qmd`

**YAML front matter (copiar exacto, cambiar solo lo marcado):**

```yaml
---
title: "TEMA PRINCIPAL"                          # ← Cambiar
subtitle: "SX: Título de la Sesión"              # ← Cambiar
author: "Prof. Francisco Suárez"
institute: "Universidad Católica Boliviana"
date: "YYYY-MM-DD"                              # ← Fecha de la sesión
format:
  revealjs:
    theme: sky
    transition: slide
    slide-number: true
    chalkboard: true
    code-fold: true
    code-tools: true
    highlight-style: github
    footer: "NLP y Análisis Semántico | Semana N" # ← Cambiar N
    logo: ""
    incremental: false
    scrollable: true
execute:
  echo: true
  warning: false
---
```

### Estructura de contenido típica

```markdown
## Agenda de Hoy {.smaller}
# Bloque 1: Título {background-color="#0077b6"}   ← Azul oscuro
# Bloque 2: Título {background-color="#023e8a"}   ← Azul más oscuro
## Slide normal {.smaller}
## Resumen / Lo Que Aprendimos Hoy {.smaller}
## Para la Próxima Sesión {.smaller}
```

**Paleta de colores para bloques:** `#0077b6`, `#023e8a`, `#0096c7`  
**Paleta para mermaid/gráficos:** `#0077b6`, `#90e0ef`, `#cfe2ff`, `#00b4d8`

---

## 2. Actualizar `index.qmd`

Agregar el link bajo la semana correspondiente:

```markdown
### Semana N
- [Título de la sesión](slides/semanaN/sX_topic.qmd)
```

---

## 3. Actualizar `programa.qmd`

Cambiar la línea de texto plano a link. **Antes:**

```markdown
| | S2: Título de la sesión | Quiz N |
```

**Después:**

```markdown
| | [S2: Título de la sesión](slides/semanaN/sX_topic.qmd) | Quiz N |
```

---

## 4. Renderizar

```bash
cd /home/fjsuarez/ucb-nlp
quarto render slides/semanaN/sX_topic.qmd
```

Para renderizar todo el sitio:

```bash
quarto render
```

**Nota:** Asegúrate de tener el venv activado (`source .venv/bin/activate`) para que Quarto use el Python correcto.

---

## 5. Commit

```bash
git add .
git commit -m "Semana N - SX: título de la sesión"
```

Los archivos `_freeze/` se commitean (cachean outputs de código Python).  
Los archivos `_site/` y `*.html` están en `.gitignore`.

---

## 6. Deploy a GitHub Pages

```bash
quarto publish gh-pages --no-prompt --no-browser
```

Esto renderiza, pushea a la rama `gh-pages`, y actualiza https://fjsuarez.me.

---

## Resumen rápido (copypaste)

```bash
# Después de crear el .qmd y actualizar index.qmd + programa.qmd:
cd /home/fjsuarez/ucb-nlp
quarto render slides/semanaN/sX_topic.qmd
git add .
git commit -m "Semana N - SX: título"
quarto publish gh-pages --no-prompt --no-browser
```

---

## Estructura de directorios

```
slides/
  semana01/          # S1, S2, S3
  semana02/          # S1, S2, S3
  semana03/          # S1, S2, ...
  ...
_freeze/slides/      # Cached Python outputs (committed)
_site/               # Built HTML (gitignored, only on gh-pages)
```

## Notas

- `_quarto.yml` tiene `freeze: auto` — los slides con código Python solo re-ejecutan si el `.qmd` cambia
- Los `quizzes/` y `labs/` están excluidos del render en `_quarto.yml`
- Remote: `git@github.com:fjsuarez/ucb-nlp.git`
- Custom domain: `fjsuarez.me` (CNAME en raíz del proyecto)
