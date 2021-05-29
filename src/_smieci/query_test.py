# movies = db.query(Rating).join(User).all()
# movies = db.query(Rating).join(User).filter(User.id == 1).all()
#
# movies = db.query(Movie).join(Rating).all()
# st1 = db.query(Movie).join(Rating).filter(Rating.user_id == 1).all()


# .filter(Movie.title.contains('toy'))\
# .join(Rating.rating, and_(Rating.movie_id == Movie.id, Rating.user_id == 1))\
# my_user_id = 1
# st2 = db.query(Movie)\
#     .outerjoin(Rating, Rating.user_id == my_user_id)\
#     .all()
#
# st3 = db.query(Movie).join(Rating, Rating.user_id == my_user_id, isouter=True).all()
# st4 = db.query(Movie).join(Rating).filter(Rating.user_id == my_user_id).all
#
# query = db.query(Movie.title, Rating.rating).outerjoin(Rating, Rating.user_id == my_user_id)
# query2 = db.query(Movie.title, Rating.rating).outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == my_user_id))
# query25 = db.query(Movie.id, Movie.imdb_id, Movie.title, Movie.genres, Movie.release_date, Movie.overview, Movie.vote_count, Movie.vote_average, Rating.rating.label('user_rate')).outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == my_user_id))
# query3 = db.query(Movie, Rating.rating).outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == my_user_id))
# query35 = db.query(Movie, Rating.rating.label('user_rate')).outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == my_user_id))
# query4 = db.query(Movie).outerjoin(Rating, Rating.user_id == my_user_id)
#
# q1 = query.all()
# q2 = query2.all()
# q25 = query25.all()
# q3 = query3.all()
# q35 = query35.all()
# q4 = query4.all()
# .filter(Rating.user_id == my_user_id)\