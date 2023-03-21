from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

links_df_original = pd.read_csv('simpsons_fandom_wiki_links.csv')
links_df = links_df_original.sort_values(['season', 'episode'], ascending=[True, True])
links_df.index = np.arange(1, len(links_df)+1)

ref_types = ['Trivia', 'Cultural references', 'Continuity', 'Goofs', 'Cultural References', 'References',
             'Appearances in other media', 'Trivia/Goofs', 'Goofs/Trivia', 'Previous Episode References',
             'Production Notes', 'Citation', 'Connections to future episodes', "Krusty's Birthday Buddies",
             'Movie Moment', 'Citations', 'Trivia/Cultural References', 'Censorship', 'Cultural Reference',
             'U.S. Syndication Cuts', 'Beatles references', 'Notes and references', 'Notes', 'Legacy', 'Running Gags:',
             'Seven Deadly Sins', 'Previous and Future Episode References', 'Goofs and Continuity Errors', 'Pants Goof',
             'Deleted scenes', 'DVD Release', 'Censorship and Bans', 'Reception and Legacy', 'Reception', 'Airings',
             'Pranks', 'Alternate Versions', 'Call-Backs', 'External Links',
             'Goofs in the "Italian-American-Mexican Standoff" scene', 'Premiere', 'Previous episode references',
             'Broadcast', 'Aerospace References', 'Awards', 'China References', 'Production', 'Goofs/errors',
             'Broadcasting Information', 'Errors', 'World War II references', 'Goof', 'Notes on Known Profiles',
             'Reference links', 'Songs', 'Differences from Lady and the Tramp', 'Confusion',
             'Differences from Snow White and The Seven Dwarfs', 'Lists', 'References to other episodes', 'Music',
             'Factual Errors', 'International premieres', 'Cuts', 'References to Toy Story in Condiments', "Goofs'",
             'Continuity Errors', 'In-show references', 'Culture References', 'Characters seen in the Advent Calendar',
             'Continually', 'Previous Episodes References']


# for all headers in the list find <ul> lists that may be separated with figures or smaller header
# count <li> elements in each list
def get_ref_counts(episode_id):
    ref_page_link = links_df['url'].iloc[episode_id-1] + '/References'
    req = requests.get(ref_page_link)
    ref_page = BeautifulSoup(req.text, 'html.parser')
    headers = ref_page.find_all('h2')
    counter_dict = {}
    h_pointer = headers[0]
    for header in headers:
        if header.text in ref_types:
            h_pointer = header
            break

    counter_dict[h_pointer.text] = 0
    breakers_list = []
    for sibling in h_pointer.next_siblings:
        if sibling.name in ['h2', 'ul']:
            # switch pointer to new header if it was encountered
            if sibling.name == 'h2':
                if sibling.text in ref_types:
                    h_pointer = sibling
                    counter_dict[h_pointer.text] = 0
            else:
                # count number of li elements in ul tag
                counter = 0
                for li in sibling.contents:
                    if li.name == 'li':
                        counter = counter + 1
                # increment total number of il elements of a pointed h2
                counter_dict[h_pointer.text] = counter_dict[h_pointer.text] + counter
        elif sibling.name in ['h3','figure',None]:
            # skip decorator elements
            continue
        else:
            breakers_list.append(sibling.name)
            break
    return counter_dict


counter_dicts = []
for i in range(len(links_df)):
    cd = get_ref_counts(i+1)
    counter_dicts.append(cd)


list_df = []
for i, cd in enumerate(counter_dicts):
    list_df.append(pd.DataFrame(cd, index=[i]))
joined_df = pd.concat(list_df)


new_joined_df = joined_df.fillna(0)
new_joined_df = new_joined_df.astype(int)
new_joined_df.to_csv('references.csv', index=False)
