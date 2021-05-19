from ast import literal_eval
import pandas as pd

# movie_csv = "data/movies.csv"
movie_csv = "data/movies_metadata_top10.csv"
rating_csv = "data/ratings_top.csv"
users_csv = "data/users.csv"

def read_clear_movies():
    df = pd.read_csv(movie_csv)
    df = pd.DataFrame(df, columns=['id', 'imdb_id', 'title', 'genres', 'release_date', 'overview', 'poster_path'])

    df = df.sort_values('id')

    df['genres'] = df['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    df['genres'] = df['genres'].str.join("|")

    df['release_date'] = df['release_date'].apply(pd.to_datetime)
    df['year'] = pd.DatetimeIndex(df['release_date']).year

    df['title'] = df['title'] + " (" + df['year'].astype(str) + ")"

    # df.drop('release_date', axis='columns', inplace=True);
    df.drop('year', axis='columns', inplace=True);
    return df


def read_rating():
    df = pd.read_csv(rating_csv)
    return df

def read_users():
    df = pd.read_csv(users_csv, sep=';')
    return df;

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
