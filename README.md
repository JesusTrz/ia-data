# IA Data Analyzer

Pipeline de datos que analiza un dataset, lo almacena en Supabase y usa la API de OpenAI para extraer patrones, tendencias y predicciones.

## Cómo funciona

1. **Carga del dataset** — Lee y procesa el dataset con Pandas
2. **Almacenamiento** — Envía los datos procesados a una base de datos en Supabase
3. **Análisis con IA** — Consulta los datos y los envía a la API de OpenAI (ChatGPT)
4. **Resultados** — Devuelve patrones, tendencias y predicciones basadas en los datos

## Tecnologías

- **Python** — Lenguaje principal
- **Pandas** — Procesamiento y análisis del dataset
- **Supabase** — Base de datos y backend
- **OpenAI API** — Análisis con inteligencia artificial

## Instalación

1. Clona el repositorio
```bash
   git clone https://github.com/JesusTrz/ia-data.git
   cd ia-data
```

2. Instala las dependencias
```bash
   pip install -r requirements.txt
```

3. Configura las variables de entorno
```bash
   cp .env.example .env
```

   Llena tu archivo `.env`:
```env
   SUPABASE_URL=tu_supabase_url
   SUPABASE_KEY=tu_supabase_key
   OPENAI_API_KEY=tu_openai_api_key
```

4. Ejecuta el proyecto
```bash
   python main.py
```

## Resultados

El análisis con IA devuelve patrones recurrentes en los datos, tendencias a lo largo del tiempo y predicciones basadas en el historial.
