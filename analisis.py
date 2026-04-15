import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai import OpenAI

# Cargar credenciales
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analizar_y_graficar():
    print("Comprimiendo datos históricos con Pandas...")
    df = pd.read_csv('./data/ICE_Detention_Trends new.csv')
    
    df['date'] = pd.to_datetime(df['date'])
    df['mes_anio'] = df['date'].dt.to_period('M')
    
    # Agrupación mensual
    resumen = df.groupby('mes_anio').agg(
        prom_poblacion=('daily_pop', 'mean'),
        total_ingresos=('book_in', 'sum'),
        total_salidas=('book_out', 'sum')
    ).reset_index()
    
    resumen['prom_poblacion'] = resumen['prom_poblacion'].round(0)

    # --- CÁLCULO DE TOTALES GLOBALES ---
    promedio_global = resumen['prom_poblacion'].mean()
    gran_total_ingresos = resumen['total_ingresos'].sum()
    gran_total_salidas = resumen['total_salidas'].sum()

    # GRAFICAS
    print("Generando ventana interactiva con 3 gráficas...")
    eje_x = resumen['mes_anio'].dt.to_timestamp()
    
    # Crear un lienzo grande
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14))

    # --- GRÁFICA 1: TENDENCIAS ---
    ax1.plot(eje_x, resumen['prom_poblacion'], color='#1f77b4', linewidth=2)
    ax1.set_title('1. TENDENCIAS: Población Promedio Histórica', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Personas Detenidas')
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Etiqueta de Totales Gráfica 1
    texto_ax1 = f"Promedio Global: {promedio_global:,.0f} personas"
    ax1.text(0.02, 0.85, texto_ax1, transform=ax1.transAxes, fontsize=11,
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', boxstyle='round,pad=0.5'))

    # --- GRÁFICA 2: PATRONES ---
    ax2.plot(eje_x, resumen['total_ingresos'], color='green', label='Ingresos (Book In)', alpha=0.7, linewidth=1.5)
    ax2.plot(eje_x, resumen['total_salidas'], color='red', label='Salidas (Book Out)', alpha=0.7, linewidth=1.5)
    ax2.set_title('2. PATRONES: Flujos Mensuales (Picos y Caídas)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cantidad de Personas')
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle='--', alpha=0.6)

    # Etiqueta de Totales Gráfica 2
    texto_ax2 = f"TOTAL HISTÓRICO INGRESOS: {gran_total_ingresos:,.0f}\nTOTAL HISTÓRICO SALIDAS: {gran_total_salidas:,.0f}"
    ax2.text(0.02, 0.80, texto_ax2, transform=ax2.transAxes, fontsize=11,
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', boxstyle='round,pad=0.5'))

    # --- GRÁFICA 3: PREDICCIONES ---
    x_num = np.arange(len(eje_x))
    y_vals = resumen['prom_poblacion'].fillna(0).values
    z = np.polyfit(x_num, y_vals, 1)
    p = np.poly1d(z)
    
    x_futuro = np.arange(len(eje_x) + 6)
    fechas_futuras = pd.date_range(start=eje_x.iloc[0], periods=len(x_futuro), freq='MS')

    ax3.plot(eje_x, y_vals, color='#1f77b4', label='Datos Históricos')
    ax3.plot(fechas_futuras, p(x_futuro), color='orange', linestyle='--', linewidth=2.5, label='Pronóstico Matemático')
    ax3.set_title('3. PREDICCIONES: Proyección de Tendencia (Próximos 6 meses)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Personas Detenidas')
    ax3.legend(loc='upper right')
    ax3.grid(True, linestyle='--', alpha=0.6)

    # Etiqueta de Totales Gráfica 3
    prediccion_final = p(x_futuro[-1])
    texto_ax3 = f"Población total esperada\nen 6 meses: {prediccion_final:,.0f} personas"
    ax3.text(0.02, 0.80, texto_ax3, transform=ax3.transAxes, fontsize=11,
             bbox=dict(facecolor='#fff3e0', alpha=0.9, edgecolor='orange', boxstyle='round,pad=0.5'))

    # Mostrar
    plt.tight_layout()
    plt.show()

    # ==========================================
    # Análisis con IA
    # ==========================================
    resumen['mes_anio'] = resumen['mes_anio'].astype(str)
    datos_texto = resumen.to_csv(index=False)
    
    print("Enviando datos a la API de ChatGPT para el análisis cualitativo...")
    
    prompt_sistema = """
    Eres un analista de datos experto en políticas migratorias de EE. UU. 
    Te proporcionaré un resumen histórico mensual de la población en detención de ICE.
    Analiza las cifras e identifica:
    1. Patrones de estacionalidad (¿hay meses específicos con picos de ingresos o salidas?).
    2. Tendencias macro a lo largo de los años.
    3. Anomalías matemáticas o cambios drásticos repentinos.
    4. PREDICCIÓN: Basándote en la tendencia y estacionalidad, pronostica el comportamiento para los próximos 6 meses.
    Sé directo, utiliza viñetas y apóyate estrictamente en los números proporcionados.
    """

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Aquí están los datos:\n\n{datos_texto}"}
        ],
        temperature=0.3 
    )
    
    print("\n" + "="*40)
    print(" ANÁLISIS DE LA IA")
    print("="*40 + "\n")
    print(respuesta.choices[0].message.content)

if __name__ == "__main__":
    analizar_y_graficar()