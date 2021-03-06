# table.py
import pandas as pd
import numpy as np
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

teams = {'Liverpool': 'LIV',
         'Manchester City': 'MCI',
         'Leicester City': 'LEI',
         'Chelsea': 'CHE',
         'Manchester United': 'MUN',
         'Wolverhampton Wanderers': 'WOL',
         'Sheffield United': 'SHU',
         'Tottenham Hotspur': 'TOT',
         'Arsenal': 'ARS',
         'Burnley': 'BUR',
         'Crystal Palace': 'CRY',
         'Everton': 'EVE',
         'Newcastle United': 'NEW',
         'Southampton': 'SOU',
         'Brighton and Hove Albion': 'BHA',
         'West Ham United': 'WHU',
         'Watford': 'WAT',
         'Bournemouth': 'BOU',
         'Aston Villa': 'AVL',
         'Norwich City': 'NOR'}


def parse_table(table):
    table_list = table.split('\n')
    parsed_list = [' '.join(x.split()) for x in table_list]
    parsed_table = '\n'.join(parsed_list)
    return parsed_table


def get_table():
    """
    get_table() requests a premier league table from the website and
    returns it in the string format
    """

    try:
        skysports_table = pd.read_html(
            "https://www.skysports.com/premier-league-table")
    except ConnectionError as e:
        logger.ERROR(e)

    df = pd.DataFrame(skysports_table[0])
    teams_code = np.array([teams[team] for team in df.Team])
    pl_table = pd.DataFrame({'#': df['#'],
                             'team': teams_code,
                             'pts': df['Pts']})

    # return pl_table.to_string(header=False, index=False)
    pl_table_parsed = parse_table(
        pl_table.to_string(header=False, index=False))

    return pl_table_parsed
