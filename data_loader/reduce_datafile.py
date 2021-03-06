import pandas as pd
from data_loader.dump_params import *


def reduce_data_file():
    # movie datafile
    df = pd.read_csv(full_movie_csv, usecols=movies_metadata_use_cols, low_memory=False)
    df['id'] = pd.to_numeric(df['id'], errors='coerce', downcast='integer')
    df = df[df['id'] < reduce_movie_id_to]
    df.to_csv(reduced_movie_csv, sep=',', encoding='utf-8', index=False)

    # rate datafile
    df = pd.read_csv(full_rating_csv, low_memory=False)
    df['movieId'] = pd.to_numeric(df['movieId'], errors='coerce', downcast='integer')
    df = df[df['movieId'] < reduce_movie_id_to]
    df.to_csv(reduced_rating_csv, sep=',', encoding='utf-8', index=False)

    print("OK")


if __name__ == "__main__":
    reduce_data_file()
