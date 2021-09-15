from ast import literal_eval

import pandas as pd

from data_loader.dump_params import *


def read_clear_movies(file_path: str):
    df = pd.read_csv(file_path)
        # , sep=",",
        # usecols=moviesMetadataUsecols,
        # date_parser=pd.datetools.to_datetime,
        # dtype={
        #         # 'adult': 'bool',
        #        # 'belongs_to_collection': 'object',
        #        # 'budget': 'int64',
        #        'genres': 'object',
        #        # 'homepage': 'object',
        #        'id': 'int64',
        #        'imdb_id': 'string',
        #        # 'original_language': 'string',
        #        # 'original_title': 'string',
        #        'overview': 'string',
        #        'popularity': 'float64',
        #        # 'poster_path': 'object',
        #        # 'production_companies': 'object',
        #        # 'production_countries': 'object',
        #        # 'release_date': 'date',
        #        # 'revenue': 'float64',
        #        # 'runtime': 'float64',
        #        # 'spoken_languages': 'object',
        #        # 'status': 'object',
        #        # 'tagline': 'string',
        #        # 'title': 'string',
        #        # 'video': 'object',
        #        # 'vote_average': 'float64',
        #        # 'vote_count': 'float64'
        # }

    df = pd.DataFrame(df, columns=movies_metadata_use_cols)  # filter and order columns

    df = df.drop_duplicates(keep='first')  # removes the duplicates
    df.dropna(how='all', inplace=True)  # drop empty row
    df.dropna(subset=['title'], inplace=True)  # drop rows without title

    # cast types
    df['id'] = pd.to_numeric(df['id'], errors='coerce', downcast='integer')
    df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce', downcast='float')
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce', downcast='float')
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['release_year'] = df['release_date'].dt.year

    # TODO: sprawdzić ten order
    df = df.sort_values("id")  # sort by id
    df = df.reset_index(drop=True)

    # genres transform
    df["genres"] = (
        df["genres"]
        .fillna("[]")
        .apply(literal_eval)
        .apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])
    )
    df["genres"] = df["genres"].str.join("|")

    # df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').apply(lambda x: x.date())

    # dodaj rok do tytułu
    # df["release_date"] = df["release_date"].apply(pd.to_datetime) if df["release_date"] else None
    # df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    # df["year"] = pd.DatetimeIndex(df["release_date"]).year
    # df["title"] = df["title"] + " (" + df["year"].astype(str) + ")"

    # df.drop('release_date', axis='columns', inplace=True);
    # df.drop("year", axis="columns", inplace=True)
    return df

def reduce_movies_columns(data_frame):
    data_frame = data_frame.rename(columns={"id": "movieId", "vote_average": "vote"})
    data_frame = pd.DataFrame(data_frame, columns=["movieId", "title", "genres", "vote"])
    return data_frame

def read_rating(file_path: str):
    df = pd.read_csv(file_path)
    return df


def read_users(file_path: str):
    df = pd.read_csv(file_path, sep=",")
    return df




# pp = read_clear_movies("movies_metadata_top10.csv")
# pp = pp.values
# print(pp[6])


# from datetime import datetime
# print(type(pp[4]))
# xx = datetime.strptime(pp[4], '%d-%b-%y %h:%m:%s').date()
# print(xx)


# conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='myappdb')
# cursor = conn.cursor()
# # excel_data = pd.read_excel(r'[filepath]',sep=',', quotechar='\'')
#
# for row in df.iterrows():
#     testlist = row[1].values
#     cursor.execute("INSERT INTO movies(id, title, genres)"
#                    " VALUES('%s','%s','%s')" % tuple(testlist))
#
# conn.commit()
# cursor.close()
# conn.close()


# for (lp, row) in df.iterrows():
#     id = row['id']
#     genres = '|'.join(row['genres'])
#     year =  row['release_date'].year
#     title = row['title'] + " (" + str(year) + ")"
