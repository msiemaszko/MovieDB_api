import asyncio
import pandas as pd

from src.crud import crud_movie
from src.services.omdb import load_data_from_omdb
from src.database import db_base, db_engine, db_session
from src.utilities import query_util

ses = db_session()


async def update_posters_url(movies_count: int):
    db_movies = crud_movie.get_movies_without_posters(db=ses, count=movies_count)

    if db_movies:
        df = pd.DataFrame(query_util.query_to_dict(db_movies))

        # data from omdb
        results = await load_data_from_omdb(df['imdb_id'])

        # transpose array
        url_list = {}
        for i in results:
            if i['Response'] == 'True':
                url_list[i['imdbID']] = i['Poster']

        # update each movies
        (row_success, row_error) = (0, 0)
        for movie in db_movies:
            poster_url = url_list[movie.imdb_id]
            if crud_movie.update_movie_poster_url(db=ses, movie_obj=movie, poster_url=poster_url):
                row_success += 1
            else:
                row_error += 1
        print(f"Posters update: success: {row_success}, failed: {row_error}")

    else:
        print("Nothing to update.. :)")


def update_posters():
    print("Updating posters from remote API: ")
    asyncio.run(update_posters_url(250))


if __name__ == "__main__":
    update_posters()
