# UNIVERSIDAD CATÓLICA BOLIVIANA "SAN PABLO"

## DEPARTAMENTO DE INGENIERÍA EN INTELIGENCIA ARTIFICIAL

| | |
|---|---|
| **DOCENTE:** | SUÁREZ PEDRAZA FRANCISCO JAVIER (DOCENTE TITULAR) |
| **PERIODO ACADÉMICO:** | 1-2026 |
| **ASIGNATURA:** | [LIA-241] PROCESAMIENTO DEL LENGUAJE NATURAL (1) |
| **PARALELO:** | 1 |
| **FECHA INICIO:** | 02/02/2026 |
| **FECHA FIN:** | 24/06/2026 |

### HORARIO PARALELO

| Día | Horario |
|-----|---------|
| Martes | 14:05 - 14:50 |
| Martes | 15:00 - 15:45 |
| Miércoles | 14:05 - 14:50 |
| Miércoles | 15:00 - 15:45 |
| Sábado | 10:50 - 12:20 |

### HORAS Y CRÉDITOS

| Carga horaria | Créditos Académicos |
|:---:|:---:|
| 6 | 6 |

### PRERREQUISITOS

| Sigla | Nombre |
|-------|--------|
| — | — |

---

## 1. JUSTIFICACIÓN

El Procesamiento del Lenguaje Natural (NLP) es una disciplina central de la Inteligencia Artificial que permite a las máquinas comprender, interpretar y generar lenguaje humano. En un contexto donde los Modelos de Lenguaje de Gran Escala (LLMs), los sistemas de Generación Aumentada por Recuperación (RAG) y los asistentes conversacionales están transformando la industria, la academia y la sociedad, esta asignatura aporta competencias esenciales para el profesional en Ingeniería en Inteligencia Artificial.

La asignatura abarca desde los fundamentos lingüísticos y estadísticos del lenguaje (expresiones regulares, tokenización, modelos n-gram) hasta las arquitecturas neuronales más avanzadas (Transformers, BERT, GPT), pasando por representaciones vectoriales (TF-IDF, Word2Vec, GloVe) y técnicas de aprendizaje profundo (RNNs, LSTMs, CNNs). Además, se incorporan temas de ética en IA, ingeniería de prompts, fine-tuning eficiente en parámetros (LoRA, PEFT) y aplicaciones prácticas con herramientas como Hugging Face, LangChain y bases de datos vectoriales.

Esta formación permite al estudiante diseñar, implementar y evaluar soluciones de software basadas en NLP para aplicaciones reales en automatización, búsqueda semántica, generación de texto, análisis de sentimiento y sistemas conversacionales, considerando estándares de calidad, eficiencia, sostenibilidad y ética.

---

## 2. COMPETENCIAS A DESARROLLAR

### 2.1. COMPETENCIA DE LA ASIGNATURA

Diseñar, implementar y evaluar soluciones de software basadas en Procesamiento de Lenguaje Natural, aplicando modelos estadísticos, representaciones vectoriales y arquitecturas de aprendizaje profundo (Transformers, BERT, GPT) para resolver problemas reales de análisis, generación y comprensión del lenguaje humano, considerando estándares de calidad, eficiencia computacional y principios éticos.

### 2.2. COMPETENCIAS GENÉRICAS

- Desarrollar la capacidad de analizar problemas complejos de procesamiento de texto, formular hipótesis y aplicar métodos computacionales y de investigación científica para diseñar soluciones de NLP eficientes y evaluables.
- Fomentar el uso responsable de la tecnología y los modelos de lenguaje en el desarrollo de sistemas de IA, considerando el impacto social, los sesgos algorítmicos, las alucinaciones y las implicaciones éticas de las soluciones tecnológicas.
- Aplicar metodologías de trabajo colaborativo para el desarrollo de proyectos de NLP interdisciplinarios, promoviendo la comunicación efectiva, la revisión de código entre pares y el respeto por diferentes perspectivas.
- Fomentar la capacidad de identificar oportunidades de mejora en la industria y la sociedad, aplicando NLP y modelos de lenguaje para desarrollar soluciones innovadoras en análisis de texto, generación de contenido, búsqueda semántica y sistemas conversacionales.
- Fortalecer la capacidad de adaptación a nuevas herramientas, frameworks y paradigmas de NLP (Hugging Face, LangChain, PEFT), promoviendo el aprendizaje continuo en un entorno tecnológico en constante evolución.

---

### 2.3. DERIVACIÓN/DESAGREGACIÓN DE LA COMPETENCIA

| Elementos de Competencia | Saberes Procedimentales | Saberes Conceptuales | Saberes Actitudinales | Unidades de Aprendizaje |
|---|---|---|---|---|
| **Elemento 1:** Aplicar técnicas de preprocesamiento, representación vectorial y modelado de lenguaje estadístico y neuronal para transformar, analizar y clasificar datos lingüísticos, utilizando modelos clásicos (n-gramas, TF-IDF) y redes neuronales recurrentes (RNN, LSTM, GRU). | - Implementar pipelines de preprocesamiento: tokenización, normalización, stemming y lematización. - Construir representaciones vectoriales de texto (BoW, TF-IDF, PMI). - Calcular similitud entre documentos usando similitud coseno. - Construir modelos de lenguaje n-gram con técnicas de suavizado. - Implementar redes neuronales (MLP, RNN, LSTM, GRU) para clasificación de texto. - Entrenar y evaluar modelos secuencia a secuencia (Seq2Seq) y CNNs 1D para texto. | - Fundamentos de expresiones regulares y su aplicación en NLP. - Modelos de representación de texto: One-hot, BoW, TF-IDF. - Conceptos de coocurrencia, PMI y n-gramas. - Modelos de lenguaje n-gram y la regla de la cadena. - Perplejidad como métrica de evaluación. - Técnicas de suavizado (Laplace, interpolación, Kneser-Ney). - Word2Vec, GloVe y FastText. - Arquitecturas RNN, LSTM, GRU, Seq2Seq y CNNs 1D. - Mecanismo de atención y arquitectura Transformer básica. | - Precisión y rigor en la limpieza y normalización de datos textuales. - Actitud analítica para seleccionar representaciones y modelos adecuados. - Disciplina en la evaluación rigurosa de modelos. - Enfoque analítico para diagnosticar problemas de gradientes. - Disposición al aprendizaje iterativo y la experimentación. | 1, 2, 3 |
| **Elemento 2:** Implementar y adaptar modelos basados en Transformers (BERT, GPT), diseñar aplicaciones integradas de NLP utilizando RAG, ingeniería de prompts, fine-tuning eficiente y consideraciones éticas para resolver problemas del mundo real. | - Implementar mecanismos de auto-atención y atención multi-cabeza. - Realizar fine-tuning de modelos preentrenados (BERT, GPT) con Hugging Face. - Aplicar técnicas de fine-tuning eficiente (LoRA, cuantización). - Construir pipelines RAG con bases de datos vectoriales. - Aplicar técnicas de ingeniería de prompts (CoT, auto-consistencia). - Evaluar sesgos y alucinaciones en modelos de lenguaje. - Desplegar modelos usando ONNX/TensorRT. | - Arquitectura Transformer completa (residuales, normalización, codificación posicional). - Modelado de lenguaje enmascarado (MLM) vs. causal. - Leyes de escalamiento y RLHF. - Fine-tuning vs. aprendizaje zero-shot/few-shot. - NER, CRF y extracción de información. - Generación Aumentada por Recuperación (RAG). - Búsqueda semántica vs. búsqueda por palabras clave. - Ingeniería de prompts y aprendizaje en contexto. - Ética en NLP: sesgo, alucinaciones, red teaming. - NLP multimodal y para dominios especializados. | - Rigor en la implementación y evaluación de modelos de gran escala. - Responsabilidad en el uso de modelos preentrenados. - Actitud investigativa para comprender arquitecturas complejas. - Innovación y creatividad en el diseño de aplicaciones de NLP. - Responsabilidad ética en el desarrollo y despliegue de sistemas de IA. - Mentalidad crítica para evaluar el impacto social de los modelos de lenguaje. | 4, 5, Proyecto Final |

---

## 3. PLANIFICACIÓN Y CRONOGRAMA

### 3.1 PLANIFICACIÓN DEL PROCESO DE ENSEÑANZA - APRENDIZAJE

| Unidad de Aprendizaje | Saberes | Semana | Estrategias y actividades de enseñanza-aprendizaje |
|---|---|---|---|
| | | | **Presencial** | **Remota Síncrona** | **Remota Asíncrona** |
| **Unidad 1: Fundamentos de NLP y Representación de Texto** — Introducción al NLP, expresiones regulares, preprocesamiento de texto (tokenización, normalización, stemming, lematización), representaciones vectoriales (BoW, One-hot, TF-IDF, PMI, n-gramas), similitud entre documentos. | - Aplicar técnicas de preprocesamiento de texto y representación vectorial para transformar datos lingüísticos en representaciones computacionales. - Implementar pipelines de limpieza, tokenización y vectorización de texto con NLTK, spaCy y scikit-learn. | 1–4 | Clases expositivas con código en vivo. Laboratorio práctico de preprocesamiento. Ejercicios hands-on con Python (NLTK, spaCy, scikit-learn). | — | Lecturas introductorias. Quizzes 1 y 2. Tarea 1: Analizador de sentimiento con TF-IDF + Regresión Logística. |
| **Unidad 2: Modelos de Lenguaje y Redes Neuronales** — Modelos n-gram, perplejidad, suavizado, HMM/POS tagging, Word2Vec, GloVe, FastText, t-SNE/PCA, perceptrones, MLP para clasificación, descenso de gradiente, dropout, RNNs, LSTMs, GRUs, RNNs bidireccionales. | - Diseñar e implementar modelos de lenguaje estadísticos y neuronales para predicción, generación y clasificación de secuencias textuales. - Construir modelos n-gram con suavizado. Entrenar redes neuronales (MLP, RNN, LSTM) para tareas de NLP. | 3–6 | Clases magistrales con derivaciones matemáticas y demos en vivo. Laboratorios de implementación con PyTorch. | — | Quizzes 3, 4 y 5. |
| **Unidad 3: Seq2Seq, CNNs y Transformers** — Arquitecturas Codificador-Decodificador, traducción automática neuronal, atención, CNNs 1D para texto, max pooling, auto-atención, atención multi-cabeza, codificación posicional, bloque Transformer completo. | - Implementar arquitecturas de secuencia a secuencia con atención. - Construir e interpretar bloques Transformer. - Comparar RNNs vs. CNNs para clasificación de texto. | 7–9 | Clases expositivas con visualizaciones de atención. Talleres de implementación paso a paso del Transformer. | — | Quiz 6. Tarea 2: Generador de nombres con LSTM. |
| **Unidad 4: BERT, GPT y Modelos Preentrenados** — Modelado de lenguaje enmascarado (MLM), fine-tuning de BERT, variantes (RoBERTa, ALBERT, DistilBERT), modelado causal (GPT), zero-shot/few-shot learning, NER, CRF, extracción de información. | - Realizar fine-tuning de modelos preentrenados con Hugging Face. - Implementar tareas downstream (NER, clasificación, QA). - Comparar modelos autoregresivos vs. autoencoding. | 10–13 | Clases magistrales. Laboratorios con Hugging Face Transformers. Sesiones de revisión para examen parcial. | — | Quiz 7 y 8. Examen Parcial (Semana 11). Tarea 3: Fine-tuning BERT para clasificación de noticias. |
| **Unidad 5: LLMs, RAG, Ética y Despliegue** — Leyes de escalamiento, RLHF, ingeniería de prompts (CoT, auto-consistencia, árbol de pensamientos), RAG, bases de datos vectoriales (FAISS, Pinecone), búsqueda semántica, fine-tuning eficiente (LoRA, cuantización), despliegue (ONNX, TensorRT), ética, sesgo, alucinaciones, NLP multimodal. | - Diseñar aplicaciones integradas de NLP usando RAG, prompts y consideraciones éticas. - Construir pipelines RAG con LangChain. - Aplicar PEFT y técnicas de despliegue. | 14–18 | Clases expositivas y talleres prácticos. Construcción guiada de aplicaciones RAG. Sesiones de debate ético. | — | Quizzes 9 y 10. Tarea 4: Aplicación "Chat con tu PDF" usando RAG. Entrega de propuesta de proyecto final. |
| **Proyecto Final** | - Aplicar todos los conocimientos adquiridos para diseñar, implementar y presentar una solución de NLP innovadora que integre múltiples técnicas del curso. | 19–20 | Presentaciones de propuestas grupales. Sesiones de revisión de código. Presentaciones finales y demos. | — | Entrega final del proyecto (código + documentación). |

---

### 3.2 SISTEMA DE EVALUACIÓN

| Elemento de Competencia | Semana | Actividad de evaluación | Presencial | Remota Síncrona | Remota Asíncrona | Evidencias | Criterio de evaluación | Porcentaje |
|---|:---:|---|:---:|:---:|:---:|---|---|:---:|
| Elemento 1 | 4 | **Tarea 1:** Analizador de sentimiento usando TF-IDF + Regresión Logística | — | — | ✓ | Notebook con código, análisis de resultados y métricas de desempeño | Correcta implementación del pipeline de preprocesamiento y vectorización. Calidad del análisis y evaluación del modelo. | 10% |
| Elemento 1 | 8 | **Tarea 2:** Generador de nombres a nivel de caracteres con LSTM | — | — | ✓ | Notebook con código, ejemplos generados y análisis | Correcta implementación de la red LSTM. Calidad de la generación y análisis de resultados. | 10% |
| Elemento 1 | 1–10 | **Quizzes 1–5** | — | ✓ | — | Respuestas correctas en evaluaciones periódicas | Exactitud, comprensión conceptual y cumplimiento | 5% |
| Elemento 1 | 11 | **Examen Parcial** | — | ✓ | — | Respuestas de examen (opción múltiple y desarrollo) | Dominio teórico y práctico de fundamentos de NLP, modelos clásicos, RNNs y Transformers básicos. | 20% |
| Elemento 2 | 12 | **Tarea 3:** Fine-tuning de BERT para Clasificación de Noticias con Hugging Face | — | — | ✓ | Notebook con código, métricas de desempeño y análisis comparativo | Correcta aplicación de fine-tuning. Calidad de la evaluación y análisis de resultados. | 10% |
| Elemento 2 | 16 | **Tarea 4:** Aplicación "Chat con tu PDF" usando RAG y API de Llama-3 o GPT-4o | — | — | ✓ | Código funcional de la aplicación, documentación técnica | Correcta implementación del pipeline RAG. Funcionalidad y calidad de las respuestas generadas. | 10% |
| Elemento 2 | 11–17 | **Quizzes 6–10** | — | ✓ | — | Respuestas correctas en evaluaciones periódicas | Exactitud, comprensión conceptual y cumplimiento | 5% |
| Elemento 2 | 20 | **Proyecto Final (Capstone)** | ✓ | — | — | Código fuente, documentación, presentación oral y demo funcional | Integración de técnicas del curso. Originalidad, calidad técnica, presentación oral y documentación. | 30% |

---

## 4. BIBLIOGRAFÍA Y WEBGRAFÍA

### Bibliografía Básica

- Jurafsky, D. & Martin, J. H. (2024). *Speech and Language Processing* (3rd ed. draft). Stanford University. [https://web.stanford.edu/~jurafsky/slp3/](https://web.stanford.edu/~jurafsky/slp3/)
- Goldberg, Y. (2017). *Neural Network Methods for Natural Language Processing*. Morgan & Claypool Publishers.
- Tunstall, L., von Werra, L. & Wolf, T. (2022). *Natural Language Processing with Transformers: Building Language Applications with Hugging Face*. O'Reilly Media.

### Bibliografía Complementaria

- Bird, S., Klein, E. & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media. [https://www.nltk.org/book/](https://www.nltk.org/book/)
- Vaswani, A. et al. (2017). "Attention Is All You Need." *Advances in Neural Information Processing Systems*, 30.
- Devlin, J. et al. (2019). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." *NAACL-HLT*.
- Brown, T. et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS*.

### Webgrafía

- Hugging Face Documentation: [https://huggingface.co/docs](https://huggingface.co/docs)
- PyTorch Tutorials: [https://pytorch.org/tutorials/](https://pytorch.org/tutorials/)
- spaCy Documentation: [https://spacy.io/](https://spacy.io/)
- LangChain Documentation: [https://docs.langchain.com/](https://docs.langchain.com/)
- NLTK Documentation: [https://www.nltk.org/](https://www.nltk.org/)
