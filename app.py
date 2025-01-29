"""
ANÁLISIS DE TAREAS - JSONPlaceholder API
Este script muestra un flujo completo de:
- Obtención de datos de una API
- Limpieza y transformación con Pandas
- Análisis estadístico básico
- Visualización con Matplotlib
"""

import requests
from pandas import DataFrame
import matplotlib.pyplot as plt

try:
    # ==============================================
    # 1. EXTRACCIÓN DE DATOS DE LA API
    # ==============================================
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    
    # Verificar respuesta exitosa (código 200)
    if response.status_code != 200:
        raise Exception(f"Error en la solicitud: Código {response.status_code}")
    
    reponseParsed = response.json()  # Convertir respuesta JSON a lista de diccionarios

    # ==============================================
    # 2. TRANSFORMACIÓN DE DATOS
    # ==============================================
    # Estructurar datos en formato plano
    name = []
    for row in reponseParsed:
        name.append({
            'id_usuario': row['userId'],     # Ej: 1
            'tarea': row['title'],           # Ej: "delectus aut autem"
            'completada': row['completed']   # Ej: False
        })

    # Crear DataFrame de Pandas
    # Estructura esperada:
    # | id_usuario | tarea               | completada |
    # |------------|---------------------|------------|
    # | 1          | "delectus aut..."   | False      |
    df = DataFrame(name)
    
    # Limpieza de datos: Eliminar filas sin título de tarea
    # dropna() - Elimina filas/columnas con valores faltantes
    # Parámetro subset: Columnas a verificar para valores nulos
    df = df.dropna(subset=['tarea'])
    
    # Alternativa: Rellenar valores nulos con fillna()
    # df = df.fillna({'tarea': 'Sin título'})

    # Convertir booleano a texto legible
    # replace() - Reemplaza valores según mapeo
    df['completada'] = df['completada'].replace({
        True: "Sí",
        False: "No"
    })

    # ==============================================
    # 3. ANÁLISIS DE DATOS
    # ==============================================
    # Agrupar por estado de completado y contar tareas
    # groupby() + count() → Series con conteos
    # Ejemplo de salida:
    # completada
    # No    90
    # Sí     10
    grouped_df = df.groupby('completada')['tarea'].count()
    
    # Filtrar datasets
    tareas_pendientes = df[df['completada'] == 'No']  # DataFrame filtrado
    tareas_hechas = df[df['completada'] == 'Sí']      # DataFrame filtrado
    
    # Calcular porcentajes
    # len() en DataFrame devuelve número de filas
    porcentaje_tareas_pending = round((len(tareas_pendientes) / len(df)) * 100, 0)
    porcentaje_tareas_hechas = round((len(tareas_hechas) / len(df)) * 100, 0)
    
    # value_counts() → Conteo de valores únicos
    # Ejemplo salida:
    # id_usuario
    # 5    12
    # 3    10
    conteo_por_usuario = tareas_pendientes['id_usuario'].value_counts()
    
    # Obtener usuario con más pendientes
    # idxmax() → Devuelve índice (valor) del máximo
    usuario_con_mas_pendientes = conteo_por_usuario.idxmax()

    # ==============================================
    # 4. VISUALIZACIÓN CON MATPLOTLIB
    # ==============================================
    # Top 5 usuarios con más tareas completadas
    # nlargest() → Devuelve los n valores más grandes
    top_usuarios = tareas_hechas.groupby('id_usuario')['tarea'].count().nlargest(5)
    
    # Configurar gráfico de barras
    plt.figure(figsize=(7, 8))  # Tamaño de figura (ancho, alto en pulgadas)
    
    # Crear gráfico
    top_usuarios.plot(
        kind='bar',
        color=['#4CAF50', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107'],  # Paleta verde/amarilla
        edgecolor='black'
    )
    
    # Personalización
    plt.title('Top 5 usuarios con más tareas completadas', fontweight='bold')
    plt.xlabel('ID de Usuario', fontsize=12)
    plt.ylabel('Tareas Completadas', fontsize=12)
    plt.xticks(rotation=45)  # Rotar etiquetas eje X
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Grid horizontal
    
    # Mostrar gráfico
    plt.tight_layout()  # Ajustar elementos
    plt.show()

except Exception as e:
    print(f"Error en el proceso: {str(e)}")