import json


def read_file(filename):
    '''Read in json data file

    Parameters
    ----------
    filename : string
        Name of a json file to read in

    Returns
    -------
    dict
        A dictionary containing the file data
    '''
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)

    return data


def radiant_wins(data):
    '''Given dataset, determine radiant win statistics

    Loops through the matches, tallies the statistics and displays them for the
    user.

    Parameters
    ----------
    data : dict
        A dictionary containing DotA 2 match data
    '''
    win_count = 0
    loss_count = 0
    error_count = 0

    for match in data:
        try:
            if match['result']['radiant_win']:
                win_count += 1
            else:
                loss_count += 1

        except(KeyError) as e:
            error_count += 1
            pass

    print('Wins: {}'.format(win_count))
    print('Losses: {}'.format(loss_count))
    print('Errors: {}'.format(error_count))
    print('Total: {}'.format(win_count + loss_count + error_count))


def filter_by_gamemode(data, mode):
    '''Given dataset filter on a game mode

    Parameters
    ----------
    data : dict
        A dictionary containing DotA 2 match data
    mode : int
        Int corresponding to a game mode

    Returns
    -------
    list
        A list containing match dictionaries
    '''
    return [match for match in data if match['result']['game_mode'] == mode]


def game_mode_stats(data):
    '''Display game mode distribution

    Parameters
    ----------
    data : dict
        A dictionary containing DotA 2 match data
    '''
    mode_stats = {
        0: {'name': 'Unknown', 'count': 0},
        1: {'name': 'All pick', 'count': 0},
        2: {'name': 'Captains mode', 'count': 0},
        3: {'name': 'Random draft', 'count': 0},
        4: {'name': 'Single draft', 'count': 0},
        5: {'name': 'All random', 'count': 0},
        6: {'name': 'Intro', 'count': 0},
        7: {'name': 'The Diretide', 'count': 0},
        8: {'name': 'Reverse captains mode', 'count': 0},
        9: {'name': 'Greeviling', 'count': 0},
        10: {'name': 'Tutorial', 'count': 0},
        11: {'name': 'Mid only', 'count': 0},
        12: {'name': 'Least played', 'count': 0},
        13: {'name': 'New player pool', 'count': 0},
        14: {'name': 'Compendium matchmaking', 'count': 0},
        15: {'name': 'Custom', 'count': 0},
        16: {'name': 'Captains draft', 'count': 0},
        17: {'name': 'Balanced draft', 'count': 0},
        18: {'name': 'Ability draft', 'count': 0},
        19: {'name': 'Event', 'count': 0},
        20: {'name': 'All random death match', 'count': 0},
        21: {'name': '1 vs. 1 solo mid', 'count': 0},
        22: {'name': 'Ranked all pick', 'count': 0},
        23: {'name': 'Ranked Roles', 'count': 0}
    }

    for match in data:
        mode_stats[match['result']['game_mode']]['count'] += 1

    total = 0
    for stats in mode_stats.values():
        print('{}: {}'.format(stats['name'], stats['count']))
        total += stats['count']

    print('total {}'.format(total))


def filter_by_hero(data, hero_id):
    '''Filter out matches where selected hero did not appear

    Parameters
    ----------
    data : dict
        A dictionary containing DotA 2 match data
    hero_id : int
        Int corresponding to a hero

    Returns
    -------
    list
        List of match dictionaries
    '''
    return [match for match in data
            for player in match['result']['players']
            if player['hero_id'] == hero_id]


def extract_duration_data(data, display=False):
    '''Extract data based on game duration.

    Match duration is stored in secondsso we define the categories as the
    following:
        early      --> 0-19 mins  (0-1199 sec)
        mid        --> 20-39 mins (1200-2399 sec)
        late       --> 40-59 mins (2400-3599 sec)
        ultra-late --> 60+ mins   (3600+ sec)

    Parameters
    ----------
    data : dict
        A dictionary containing DotA 2 match data
    display : bool
        Whether or not the user wishes to display the data distribution
        (defaulted to false).

    Returns
    -------
    list
        Four lists are returned each containing match dictionaries
    '''
    early = []
    mid = []
    late = []
    ultra_late = []

    for match in data:
        if match['result']['duration'] <= 1199:
            early.append(match)
        elif match['result']['duration'] <= 2399:
            mid.append(match)
        elif match['result']['duration'] <= 3599:
            late.append(match)
        else:
            ultra_late.append(match)

    # display to user
    if display:
        print('Early matches: {}'.format(len(early)))
        print('Mid matches: {}'.format(len(mid)))
        print('Late matches: {}'.format(len(late)))
        print('Ultra Late matches: {}'.format(len(ultra_late)))

    return early, mid, late, ultra_late


def did_hero_win_match(match, hero_id):
    '''Take a hero and a match and determine victory

    Given a hero ID we need to determine which side they were on. `player_slot`
    tells us which team the player is on:
        Radiant --> 0-4
        Dire --> 128-132

    Parameters
    ----------
    match : dict
        A match dictionary containing match and player statistics
    hero_id : int
        Int corresponding to a hero

    Returns
    -------
    bool
        True if hero won, False if they lost
    '''
    player_slot = None
    for player in match['result']['players']:
        if player['hero_id'] == hero_id:
            player_slot = player['player_slot']

    if player_slot == None:
        print('hero {} not in match {}'.format(hero_id, match['result']['match_id']))

    try:
        if player_slot <= 4:
            return match['result']['radiant_win']
        else:
            return not match['result']['radiant_win']
    except:
        print('Match_id: {}, does not have \'radiant_win\''.format(match['result']['match_id']))
        pass


def calculate_win_percent(total_matches, wins):
    '''Calculate win percentage

    Parameters
    ----------
    total_matches : int
        Number of matches played
    wins : int
        Number of wins

    Returns
    -------
    float
        Win percentage
    '''
    return (float(wins) / float(total_matches)) * 100


def filter_bad_data(data):
    '''Filter out data with no win condition

    There are some cases where there is no `radiant_win` key.  This is generally
    caused by a match aborted during the draft phase.  In any case we want to
    make sure we clean up these cases before processing the data.

    Parameters
    ----------
    data : dict
        A dictionary containing DotA 2 match data

    Returns
    -------
    list
        List of match dictionaries
    '''
    return [match for match in data if 'radiant_win' in match['result'].keys()]


def determine_teams(match):
    '''Determines which players are on radiant or dire

    Parameters
    ----------
    match : dict
        A match dictionary containing match and player statistics

    Returns
    -------
    dict
       A dictionary with `radiant` and `dire` keys with lists of player
       dictionaries as values.
    '''
    radiant = []
    dire = []

    for player in match['players']:
        # print('Player ID: {}'.format(player['hero_id']))
        if player['player_slot'] <= 4:
            radiant.append(player)
        else:
            dire.append(player)

    return {'radiant_roster': radiant, 'dire_roster': dire}


def calculate_per_min_metrics(team_roster, duration, metric):
    '''Calculates team per minutes metrics given a team and a metric

    Parameters
    ----------
    team_roster : list
        A list of the heroes on a team
    duration : int
        match duration in seconds
    metric : string
        Metric to total

    Returns
    -------
    float
        Team total of the metric
    '''
    metric_total = 0

    for player in team_roster:
        mps = float(player[metric]) / float(60)
        metric_total += (mps * duration)

    return metric_total


def get_team_scores(match):
    '''Get the scores for both teams

    Parameters
    ----------
    match : dict
        A match dictionary containing match and player statistics

    Returns
    -------
    dict
        Contains the `radiant` and `dire` team scores
    '''
    return {'radiant_score': match['radiant_score'], 'dire_score': match['dire_score']}


def get_hero_winrates(data):
    '''Calculate hero winrates given dataset

    This method uses the dataset given and calculates the win rate of each of
    the heroes.  It uses a `heroes.json` which contains all the hero IDs.

    data : dict
        A dictionary containing DotA 2 match data

    Returns
    -------
    dict
        Hero IDs as keys and their win rates as the value
    '''
    heroes = read_file('data/heroes.json')

    winrates = {}
    for hero in heroes['result']['heroes']:
        hero_data = filter_by_hero(data, hero['id'])
        wins = 0
        for match in hero_data:
            if did_hero_win_match(match, hero['id']):
                wins += 1

        winrates[hero['id']] = get_win_percent(len(hero_data), wins)

    return winrates


def calculate_winrate_average(team_roster, winrates):
    '''Calculates winrate average of given team

    Parameters
    ----------
    team_roster : list
        A list of the heroes on a team
    winrates: dict
        Dictionary containing hero IDs as keys and their win rates as the value
    '''
    winrate = 0
    for player in team_roster:
        winrate += winrates[player['hero_id']]

    return winrate/float(5)
