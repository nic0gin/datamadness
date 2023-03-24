import pandas as pd
import numpy as np
# Accessing IMDB API
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

def get_demographics_row(episode, season, epnr):
    row = []
    if 'demographics' in episode.keys():
        row.append(season)
        row.append(epnr)
        if 'ttrt fltr imdb users' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr imdb users']['votes'])
            row.append(episode['demographics']['ttrt fltr imdb users']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr aged under 18' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr aged under 18']['votes'])
            row.append(episode['demographics']['ttrt fltr aged under 18']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr aged 18 29' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr aged 18 29']['votes'])
            row.append(episode['demographics']['ttrt fltr aged 18 29']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr aged 30 44' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr aged 30 44']['votes'])
            row.append(episode['demographics']['ttrt fltr aged 30 44']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr aged 45 plus' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr aged 45 plus']['votes'])
            row.append(episode['demographics']['ttrt fltr aged 45 plus']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr males' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr males']['votes'])
            row.append(episode['demographics']['ttrt fltr males']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr males aged under 18' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr males aged under 18']['votes'])
            row.append(episode['demographics']['ttrt fltr males aged under 18']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr males aged 18 29' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr males aged 18 29']['votes'])
            row.append(episode['demographics']['ttrt fltr males aged 18 29']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr males aged 30 44' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr males aged 30 44']['votes'])
            row.append(episode['demographics']['ttrt fltr males aged 30 44']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr males aged 45 plus' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr males aged 45 plus']['votes'])
            row.append(episode['demographics']['ttrt fltr males aged 45 plus']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr females' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr females']['votes'])
            row.append(episode['demographics']['ttrt fltr females']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr females aged under 18' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr females aged under 18']['votes'])
            row.append(episode['demographics']['ttrt fltr females aged under 18']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr females aged 18 29' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr females aged 18 29']['votes'])
            row.append(episode['demographics']['ttrt fltr females aged 18 29']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr females aged 30 44' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr females aged 30 44']['votes'])
            row.append(episode['demographics']['ttrt fltr females aged 30 44']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr females aged 45 plus' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr females aged 45 plus']['votes'])
            row.append(episode['demographics']['ttrt fltr females aged 45 plus']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr top 1000 voters' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr top 1000 voters']['votes'])
            row.append(episode['demographics']['ttrt fltr top 1000 voters']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr us users' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr us users']['votes'])
            row.append(episode['demographics']['ttrt fltr us users']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)
        if 'ttrt fltr non us users' in episode['demographics'].keys():
            row.append(episode['demographics']['ttrt fltr non us users']['votes'])
            row.append(episode['demographics']['ttrt fltr non us users']['rating'])
        else:
            row.append(np.nan)
            row.append(np.nan)

    return row

def create_Dataset(series):

    df = pd.DataFrame(columns=['season', 'episode',
                               'total_counts', 'total_rating',
                               '<18_counts', '<18_rating',
                               '18-29_counts', '18-29_rating',
                               '30-44_counts', '30-44_rating',
                               '45+_counts', '45+_rating',
                               'male_counts', 'male_rating',
                               'male_<18_counts', 'male_<18_rating',
                               'male_18-29_counts', 'male_18-29_rating',
                               'male_30-44_counts', 'male_30-44_rating',
                               'male_45+_counts', 'male_45+_rating',
                               'female_counts', 'female_rating',
                               'female_<18_counts', 'female_<18_rating',
                               'female_18-29_counts', 'female_18-29_rating',
                               'female_30-44_counts', 'female_30-44_rating',
                               'female_45+_counts', 'female_45+_rating',
                               'top1000_counts', 'top1000_rating',
                               'us_users_counts', 'us_users_rating',
                               'non-us_users_counts', 'non-us_users_rating'
                               ])

    for ssn in series['episodes'].keys():
        for ep in series['episodes'][int(ssn)].keys():
            episode = series["episodes"][int(ssn)][int(ep)]
            episode = add_demographics(episode)
            episode_entry = get_demographics_row(episode, int(ssn), int(ep))
            print('Season', int(ssn), 'Episode', int(ep))
            if episode_entry:
                df.loc[len(df)] = episode_entry

    df.reset_index()
    return df




series = retrieve_Series()
series = add_episodes(series)
voting_demographics_data = create_Dataset(series)

voting_demographics_data.fillna(np.mean)
voting_demographics_data.to_csv('./voting_demographics.csv')
