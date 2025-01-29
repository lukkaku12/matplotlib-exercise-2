import requests
from pandas import DataFrame
import matplotlib.pyplot as plt

try:
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    reponseParsed = response.json()
    name = []
    for row in reponseParsed:
        name.append({
            'id_usuario': row['userId'],
            'tarea': row['title'],
            'completada': row['completed']
        })

    df = DataFrame(name)
    df = df.dropna(subset=['tarea'])
    # tambien existe fillna() y adentro de los corchetes el string o el valor que reemplazara las celdas que tengan valores nulos
    # df = df.fillna('Sin tarea')
    df['completada'] = df['completada'].replace({
    True: "Sí",
    False: "No"
})
    grouped_df = df.groupby('completada')['tarea'].count()
    
    # print(grouped_df)
    # print(len(df))
    tareas_pendientes = df[df['completada'] == 'No']  # Filtrar pendientes
    tareas_hechas = df[df['completada'] == 'Sí']  # Filtrar hechas
    print(tareas_pendientes)
    
    porcentaje_tareas_pending = round((len(tareas_pendientes) / len(df)) * 100, 0)
    print(porcentaje_tareas_pending)
    porcentaje_tareas_hechas = round((len(tareas_hechas) / len(df)) * 100,0)
    print(f"porcentaje del: {porcentaje_tareas_hechas:.0f}%")
    conteo_por_usuario = tareas_pendientes['id_usuario'].value_counts() 
    # print(conteo_por_usuario)
    usuario_con_mas_pendientes = conteo_por_usuario.idxmax()
    # print(usuario_con_mas_pendientes)


    # Grafico de barras

    top_usuarios = tareas_hechas.groupby('id_usuario')['tarea'].count().nlargest(5)
    print(top_usuarios)
    plt.figure(figsize=(7, 8))
    top_usuarios.plot(kind='bar')

    plt.title('Top 5 usuarios con más tareas completadas')
    plt.xlabel('Id de Usuario')
    plt.ylabel('Cantidad de tareas completadas')

    plt.show()

    

except Exception as e:
    print(e)
