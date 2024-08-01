from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pyarrow.parquet as pq


app = FastAPI()

app.title = 'Movies'

# Ruta al archivo parquet
data_credits = pd.read_parquet("Data/data_credits.parquet")
data_movies = pd.read_parquet("Data/data_movies.parquet")


data_movies['release_year'] = pd.to_datetime(data_movies['release_date'], format='%Y-%m-%d', errors='coerce')
data_credits = data_credits.drop('crew', axis=1)


# Desarrollo de las funciones para los endpoints
@app.get('/mes', tags=['Películas por mes'])
def cantidad_filmaciones_mes(Mes):
    #Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset

    # Mapeo de nombres de meses en español a números de mes
    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }
    
    # Obtener el número del mes a partir del nombre en español
    mes_numero = meses.get(Mes.lower())

    if mes_numero is None:
        raise ValueError(f"Nombre de mes en español no válido: {Mes}")
    
    # Conversión del df a datetime
    data_movies['release_year'] = pd.to_datetime(data_movies['release_date'], format='%Y-%m-%d', errors='coerce')
    
    # Filtrar el DataFrame por el mes especificado
    peliculas_en_mes = data_movies[data_movies['release_year'].dt.month == mes_numero]
    
    # Contar la cantidad de películas
    cantidad_peliculas = peliculas_en_mes.shape[0]
    
    #return cantidad_peliculas
    return f'se estrenaron {cantidad_peliculas} en el mes de {Mes}'

# Ejemplo de uso
mes_consultado = 'julio'
cantidad = cantidad_filmaciones_mes(mes_consultado)
print(f'Cantidad de películas estrenadas en {mes_consultado.capitalize()}: {cantidad}')




@app.get('/dia', tags=['Películas por día'])
def cantidad_filmaciones_dia(Dia):
# Verifica que el día en español esté en el diccionario

    # Mapeo de días de la semana en español a inglés
    dias_espanol_a_ingles = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sábado': 'Saturday',
        'domingo': 'Sunday'
    }

    if Dia.lower() not in dias_espanol_a_ingles:
        raise ValueError("Día de la semana no válido en español.")
    
    # Convierte el día en español al día en inglés
    dia_ingles = dias_espanol_a_ingles[Dia.lower()]
    
    # Asegúrate de que la columna de fecha en el DataFrame esté en formato de fecha
    data_movies['release_year'] = pd.to_datetime(data_movies['release_date'], format='%Y-%m-%d', errors='coerce')
    
    # Crea una columna de día de la semana en inglés
    data_movies['day_of_week'] = data_movies['release_year'].dt.day_name()
    
    # Filtra el DataFrame por el día de la semana en inglés
    peliculas_dia = data_movies[data_movies['day_of_week'] == dia_ingles]
    
    # Devuelve la cantidad de películas estrenadas en ese día
    return f'Se estrenaron {len(peliculas_dia)} en el día {Dia}'





@app.get('/puntaje', tags=['Puntaje de película'])
def score_titulo(Titulo):
    # Buscar la fila que coincide con el título proporcionado
    movie_info = data_movies[data_movies['title'].str.lower() == Titulo.lower()]
    
    if not movie_info.empty:
        # Extraer la información del DataFrame
        movie_title = movie_info.iloc[0]['title']
        release_year = movie_info.iloc[0]['release_year']
        score = movie_info.iloc[0]['popularity']
        return movie_title, release_year, score
    else:
        return None, None, None

# Ejemplo de uso de la función
title_input = 'toy story'
movie_title, release_year, score = score_titulo(title_input)

if movie_title:
    print(f"La película: {movie_title} estrenada en el año {release_year} tiene un puntaje de {score}")
else:
    print("Movie not found.")




@app.get('/promedio', tags=['Promedio de votos'])
def votos_titulo(Titulo):
    """
    La función devuelve el título de una película, la cantidad y el promedio de los votos, siempre y cuando tenga más de 2000 votos
    """
    # Filtrar el DataFrame para la película especificada
    pelicula = data_movies[data_movies['title'] == Titulo]
    
    if pelicula.empty:
        return f"No se encontró la película con el título '{Titulo}'."
    
    # Suponiendo que cada fila en 'data_movies' representa una valoración,
    # contamos las valoraciones y calculamos el promedio
    total_votos = pelicula.shape[0]
    
    if total_votos < 2000:
        return "La película debe tener al menos 2000 valoraciones."
    
    # Calcular el valor promedio de las votaciones
    valor_promedio = pelicula['vote_average']
    
    # Obtener la cantidad de votos (esto es redundante porque igual es el total de filas, pero puede ser útil)
    cantidad_votos = pelicula['vote_count'].sum()  # Si 'votes' es la columna de conteo de votos, de lo contrario, usar 'total_votos'
    
    return {
        'title': Titulo,
        'cantidad_votos': cantidad_votos,
        'valor_promedio': valor_promedio
    }





@app.get('/actor', tags=['Actor'])
def actor_success(nombre_actor: str):
    # Filtrar el DataFrame para obtener solo las películas en las que el actor ha participado
    actor_movies = data_credits[data_credits['actors'] == nombre_actor]
    
    # Verificar si el actor ha participado en alguna película
    if actor_movies.empty:
        return {
            'actor': nombre_actor,
            'num_movies': 0,
            'average_return': None,
            'total_return': None
        }
    
    # Calcular la cantidad de películas
    num_movies = len(actor_movies)
    
    # Calcular el promedio de retorno
    average_return = actor_movies['return'].mean()
    
    # Calcular el retorno total
    total_return = actor_movies['return'].sum()
    
    return {
        'actor': nombre_actor,
        'num_movies': num_movies,
        'average_return': average_return,
        'total_return': total_return
    }





@app.get('/director', tags=['Director'])
def get_director_success(nombre_director):
    # Filtrar las películas del director especificado en data_credits
    director_movies = data_credits[data_credits['director'] == nombre_director]
    
    if director_movies.empty:
        return f"No se encontraron películas para el director {nombre_director}."
    
    # Obtener IDs de las películas del director
    movie_ids = director_movies['id'].unique()
    
    # Filtrar las películas en data_movies usando los IDs obtenidos
    director_movies_details = data_movies[data_movies['id'].isin(movie_ids)]
    
    # Calcular el éxito total del director basado en los retornos
    total_success = data_movies['return'].sum()
    
    # Crear una lista con la información detallada de cada película
    movies_details = data_movies[['title', 'release_date', 'return']].to_dict(orient='records')
    
    return total_success, movies_details






@app.get('/recomendador', tags=['Recomendador de películas'])
def recomendacion(Titulo):

    # Certeza de que la película de destino esté en el df
    if Titulo not in data_movies['title'].values:
        raise ValueError(f"La película '{Titulo}' no se encuentra")

    # Pivotar el df para obtener una tabla de usuario-película
    user_movie_matrix = data_movies.pivot_table(index='id', columns='title', values='popularity')
    
    # Verifica que haya datos suficientes para calcular la similitud
    if user_movie_matrix.empty or len(user_movie_matrix.columns) < 2:
        return []

    # Calcula la similitud del coseno entre películas
    similarity_matrix = cosine_similarity(user_movie_matrix.fillna(0).T)

    # Convierte la matriz de similitud en un df
    similarity_df = pd.DataFrame(similarity_matrix, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

    # Obtiene las similitudes de la película objetivo con otras películas
    target_movie_similarities = similarity_df[Titulo]

    # Ordena las películas por similitud en orden descendente, excluyendo la película objetivo
    similar_movies = target_movie_similarities.drop(Titulo).sort_values(ascending=False)

    # Obtiene los 5 títulos de películas más similares
    top_5_similar_movies = similar_movies.head(5).index.tolist()

    return top_5_similar_movies
