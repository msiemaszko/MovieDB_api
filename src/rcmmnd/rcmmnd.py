from typing import List

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from data_loader.read_from_file import *
from data_loader.dump_params import *

try:
    # from nltk import wordnet
    nltk.data.find('tokenizers/punkt')
    print('NLTK data found.')
except LookupError:
    print('Cant find NLTK data, starting download...')
    nltk.download(['punkt', 'stopwords', 'wordnet'])


class Recommendation:
    def __init__(self):
        self.movies = read_clear_movies(reduced_movie_csv)
        self.movies = reduce_movies_columns(self.movies)
        self.ratings = read_rating(reduced_rating_csv)

        self.rates_movies = self.movies.merge(self.ratings)
        self.count_vector, self.vectorizer, self.genres_list \
            = self.clean_feature_and_return_ndarray(self.movies["genres"])

    def clean_feature_and_return_ndarray(self, words_df):
        lemmatizer = WordNetLemmatizer()
        genres_list = []
        for i in range(len(words_df)):
            temp = words_df[i].lower()
            temp = temp.split("|")
            temp = [lemmatizer.lemmatize(word) for word in temp]
            genres_list.append(" ".join(temp))

        vectorizer = CountVectorizer()
        count_vector = vectorizer.fit_transform(genres_list).toarray()
        return count_vector, vectorizer, genres_list

    def content_based_filtering(self, movie_id: int, no_of_movies: int = 10) -> List[int]:
        """ Finding recommendations based on similar movies
        :param movie_id: movie to analyze
        :param no_of_movies: numbers of recommended movies
        :return:
        """

        movie_index = self.movies.loc[self.movies['movieId'] == movie_id, ["title"]].index[0]

        similarity_matrix = cosine_similarity(self.count_vector)
        similarity_for_current_movie = similarity_matrix[movie_index]

        df_similarity = pd.DataFrame(similarity_for_current_movie, columns=['cosine'])
        df_similarity = df_similarity[df_similarity.index != movie_index]  # remove current movie
        df_similarity = df_similarity.sort_values(by='cosine', ascending=False)  # sort by cosine
        df_similarity = df_similarity[:no_of_movies]  # take only top values

        # join movie details
        df_similarity = df_similarity.join(self.movies)
        return df_similarity['movieId'].to_list()

    def collaborative_filtering(self, user_id: int, no_of_movies: int = 15) -> List[int]:
        """ Finding recommendation based on similar users
        :param user_id: user to analyze
        :param no_of_movies: numbers of recommended movies
        :return:
        """
        #

        genres_vector = pd.DataFrame(self.count_vector, columns=self.vectorizer.get_feature_names())

        movies = self.movies[['movieId', 'title', 'vote']]
        movies_with_genres_vector = movies.join(genres_vector)

        # to co obejrzeli użytkownicy z podpiętym wektorem gatunków
        users_watched = pd.DataFrame(self.rates_movies[['movieId', 'userId']], columns=['userId', 'movieId'])
        users_watched_genres_vector = users_watched.merge(movies_with_genres_vector)
        users_watched_genres_vector = users_watched_genres_vector.drop(["movieId", "title", "vote"], axis=1)  # remove unnecessary columns

        # grupowanie wektorów
        users_watched_count = users_watched_genres_vector.groupby('userId', as_index=False).sum() # don't set userId as index
        users_ids = users_watched_count[['userId']]
        users_ids = users_ids.rename_axis('index').reset_index()  # dodaj kolumnę index
        users_watched_count = users_watched_count.drop('userId', axis=1)

        current_user_index = users_ids[users_ids['userId'] == user_id].index[0]
        count_vector = users_watched_count.values
        current_user_genres_vector = count_vector[current_user_index]

        # klasyfikacja
        classifier = NearestNeighbors()
        classifier.fit(count_vector)

        nearest_users_indices = classifier.kneighbors([current_user_genres_vector], n_neighbors=10, return_distance=False)[0]
        nearest_users_indices = nearest_users_indices[1:]  # remove current user

        # macierz ostatnio oglądanych
        nearest_users_indices = pd.DataFrame(nearest_users_indices, columns=['index'])  # turn into dataframe
        nearest_users_indices = nearest_users_indices.rename_axis('nearest_no').reset_index()  # add nearest number
        nearest_user_total = nearest_users_indices.merge(users_ids)

        # ostatnio oglądane filmy
        watched_by_similar_user = nearest_user_total.merge(self.rates_movies, on='userId')
        watched_by_similar_user = watched_by_similar_user.sort_values(['nearest_no', 'vote'], ascending=[True, False])
        id_watched_by_current_user = self.rates_movies[self.rates_movies['userId'] == user_id]['movieId']
        id_watched_by_similar_user = watched_by_similar_user['movieId']

        # remove differences: join 2 series, and drop duplicates - don't keep them
        rcm_list = pd\
            .concat([id_watched_by_current_user, id_watched_by_similar_user])\
            .drop_duplicates(keep=False) \
            .to_list()
        return list(rcm_list[:no_of_movies])

    def based_on_ratings(self, movie_id: int, no_of_movies: int = 15) -> List[int]:
        avg_ratings = self.rates_movies.groupby('movieId')['rating'].mean()
        count = self.rates_movies.groupby('movieId')['rating'].count()
        movies_ratings = pd.DataFrame({'rating': avg_ratings, 'count': count})

        # plotting
        # from my_plot import plt_hist, sns_jointplot
        # plt_hist(movies_ratings['count'], bins=50, xlabel='liczba ocen', ylabel='ilość filmów')
        # plt_hist(movies_ratings['rating'], bins=50, xlabel='średnia ocena filmu', ylabel='ilość ocen filmu')
        # sns_jointplot(data=movies_ratings, x='rating', y='count')
        # movie_index =
        df = self.rates_movies.loc[:, ["userId", "rating", "movieId"]]
        users_movie_matrix = pd.pivot_table(df, columns='movieId', index='userId', values='rating')

        # Remove users that have not rated that movie
        users_movie_matrix = users_movie_matrix[users_movie_matrix[movie_id].notnull()]

        # Remove movies that don't have at least 2 ratings.
        users_movie_matrix = users_movie_matrix.dropna(axis='columns', thresh=2)
        # After this, all movies will have at least 2 ratings from users that have also rated that movie,
        # because after the previous step everyone has rated that movie.

        correlation = users_movie_matrix.corrwith(users_movie_matrix[movie_id])
        correlation = pd.DataFrame(correlation, columns=['correlation'])

        correlation_current_movie = movies_ratings.merge(correlation, on='movieId')
        correlation_current_movie = correlation_current_movie[correlation_current_movie['count'] > 50]
        correlation_current_movie = correlation_current_movie.sort_values(by='correlation', ascending=False)

        # remove current movie
        correlation_current_movie = correlation_current_movie[correlation_current_movie.index != movie_id]

        # take only movieId from list
        out_list = correlation_current_movie.index.to_list()[:no_of_movies]
        return out_list


rcmmnd = Recommendation()

if __name__ == "__main__":
    movie_id_ = 3
    user_id_ = 55

    similarity_ids_ = rcmmnd.content_based_filtering(movie_id_)
    print("Recommendation: Similar movies to", movie_id_, "are", similarity_ids_)

    recommend_list_ = rcmmnd.collaborative_filtering(user_id_)
    print("Recommendation: Similar user watched", recommend_list_)

    similarity_ids_ = rcmmnd.based_on_ratings(movie_id_)
    print("Recommendation: similar ratings like movie", movie_id_, "are", similarity_ids_)

