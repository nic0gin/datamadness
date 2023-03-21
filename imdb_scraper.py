# Accessing IMDB API
import pandas as pd
import imdb

ia = imdb.Cinemagoer()


def retrieve_Series():
    series = ia.get_movie('0096697')

    return series


def add_episodes(series):
    ia.update(series, 'episodes')

    return series


def add_demographics(episode):
    ia.update(episode, 'vote details')

    return episode


series = retrieve_Series()
series = add_episodes(series)
episode = add_demographics(series['episodes'][1][1])
episode['demographics'].keys()
