import numpy as np
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
# nltk.download(["punkt", "stopwords", "wordnet"])

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from src.crud import crud_movie

from src.database import db_base, db_engine, get_db, db_session
from data_loader.load_data import *
from data_loader.dump_params import *


class Recommendation:
    def __init__(self):
        self.similarities = []
        self.loadData()

    def loadData(self):
        self.movies = read_clear_movies(reduced_movie_csv)
        self.ratings = read_rating(reduced_movie_csv)
        self.count_similarities()

    def count_similarities(self):
        # In [3]:
        lemmatizer = WordNetLemmatizer()
        genres = self.movies["genres"]
        li = []
        for i in range(len(genres)):
            temp = genres[i].lower()
            temp = temp.split("|")
            temp = [lemmatizer.lemmatize(word) for word in temp]
            li.append(" ".join(temp))

        # In [4]:
        movies_dataset = pd.DataFrame(li, columns=["genres"], index=self.movies["title"])
        print("movies_dataset")
        print(movies_dataset)

        # In [5]: Finding based on similar movies
        cv = CountVectorizer()
        count_vector = cv.fit_transform(movies_dataset["genres"]).toarray()
        # X

        # In [9]:
        print("Count Vector : \n", count_vector)
        print("\nNote: First row of above count vector: ", count_vector[0])
        print("\nColumns Coresponding to above count vector is :\n", cv.get_feature_names())

        # In [10]:
        # output = self.movies.loc[:, ['movieId', 'title']]
        # output = output.join(pd.DataFrame(X))
        # output

        # In [19]: Row corresponds to a movie name
        # from sklearn.metrics.pairwise import cosine_similarity

        self.similarities = cosine_similarity(count_vector)
        # Each row of matrix coressponds to similarity of a movie with all other movies (row len = 10329)
        # print(self.similarities)

    def get_recommended(self, db: Session, movie_id: int, count: int):
        # In [21]: For user_id lets recommend movies based on his recent watched movie
        # time = self.ratings.loc[self.ratings["userId"] == user_id, ["movieId", "timestamp"]]
        # latest_movieId_watched_by_user = time.sort_values(by="timestamp", ascending=False)["movieId"].values[0]
        # latest_movieId_watched_by_user
        # latest_movie_id_watched_by_user = crud_movie.latest_movie_id_watched_by_user(db=db, user_id=user_id)
        latest_movie_id_watched_by_user = movie_id

        # In [22]:
        # movie_index = self.movies.loc[self.movies['id'] == latest_movieId_watched_by_user2, ["title"]].index[0]
        # output.loc[output['movieId'] == 8798, :]
        # powtrzone

        # In [23]:
        # movie_index, "for movie id", latest_movieId_watched_by_user

        # In [24]:
        # we need index but we are using id to find which row is crct in similarities matrix
        movie_index = self.movies.loc[self.movies['id'] == latest_movie_id_watched_by_user, ["title"]].index[0]
        similarity_values = pd.Series(self.similarities[movie_index])

        # In [26]:
        # We converted list into series in order to preserve the actual indexes of dataset even after sorting
        similarity_values.sort_values(ascending=False)

        # In [27]:
        similar_movie_indexes = list(similarity_values.sort_values(ascending=False).index)

        # In [60]: Remove the already watched movie from index list
        similar_movie_indexes.remove(movie_index)

        print("Since u watched --->", latest_movie_id_watched_by_user, "<--- We recommend you", similar_movie_indexes[:10])
        return similar_movie_indexes[:count]


service_recommend = Recommendation()
