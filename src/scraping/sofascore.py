import csv

import requests

headers = {'User-Agent': 'Mozilla/5.0'}

competition_id = 11653
season_id = 48017

round_api = "https://api.sofascore.com/api/v1/unique-tournament/{competition_id}/season/{season_id}/events/round/{round}"
statistics_api = "https://api.sofascore.com/api/v1/event/{match_id}/statistics"

stats_keys = [
    "round", "team_home", "team_away", "score_home", "score_away",
    "expected_goals_home", "expected_goals_away", "possesion_home", "possesion_away",
    "total_shots_home", "total_shots_away", "shots_on_target_home", "shots_on_target_away",
    "shots_off_target_home", "shots_off_target_away", "blocked_shots_home", "blocked_shots_away",
    "corners_home", "corners_away", "offsides_home", "offsides_away", "fouls_home", "fouls_away",
    "yellow_cards_home", "yellow_cards_away", "red_cards_home", "red_cards_away", "free_kicks_home",
    "free_kicks_away", "throw_ins_home", "throw_ins_away", "goal_kicks_home", "goal_kicks_away",
    "big_chances_home", "big_chances_away", "big_chances_missed_home", "big_chances_missed_away",
    "counter_attacks_home", "counter_attacks_away", "counter_attacks_shots_home", "counter_attacks_shots_away",
    "shots_inside_box_home", "shots_inside_box_away", "shots_outside_box_home", "shots_outside_box_away",
    "goalkeeper_saves_home", "goalkeeper_saves_away", "passes_home", "passes_away", "accurate_passes_home",
    "accurate_passes_away", "long_balls_home", "long_balls_away", "crosses_home", "crosses_away", "dribbles_home",
    "dribbles_away", "possesion_lost_home", "possesion_lost_away", "duels_won_home", "duels_won_away",
    "aerials_won_home", "aerials_won_away", "tackles_home", "tackles_away", "interceptions_home",
    "interceptions_away", "clearances_home", "clearances_away"
]


def getRoundData(competition_id, season_id, round):
    rounds = requests.get(round_api.format(
        competition_id=competition_id, season_id=season_id, round=round), headers=headers).json()
    events = rounds.get('events', [])
    return events


def getMatchScore(event):
    global stats
    stats["team_home"] = event.get('homeTeam').get('name', None)
    stats["score_home"] = event.get('homeScore').get('current', None)
    stats["team_away"] = event.get('awayTeam').get('name', None)
    stats["score_away"] = event.get('awayScore').get('current', None)


def getMatchId(event):
    return event.get('id', None)


def expectedGoals(statistics_items):
    for statistic in statistics_items:
        name = statistic.get('name')
        if name == "Expected goals":
            stats["expected_goals_home"] = statistic.get('homeValue')
            stats["expected_goals_away"] = statistic.get('awayValue')


def possession(statistics_items):
    for statistic in statistics_items:
        name = statistic.get('name')
        if name == "Ball possession":
            stats["possesion_home"] = statistic.get('homeValue')
            stats["possesion_away"] = statistic.get('awayValue')


def shots(statistics_items):
    for statistic in statistics_items:
        name = statistic.get('name')
        if name == "Total shots":
            stats["total_shots_home"] = statistic.get('homeValue')
            stats["total_shots_away"] = statistic.get('awayValue')
        elif name == "Shots on target":
            stats["shots_on_target_home"] = statistic.get('homeValue')
            stats["shots_on_target_away"] = statistic.get('awayValue')
        elif name == "Shots off target":
            stats["shots_off_target_home"] = statistic.get('homeValue')
            stats["shots_off_target_away"] = statistic.get('awayValue')
        elif name == "Blocked shots":
            stats["blocked_shots_home"] = statistic.get('homeValue')
            stats["blocked_shots_away"] = statistic.get('awayValue')


def tvData(statistics_items):
    for statistic in statistics_items:
        name = statistic.get('name')
        if name == "Corner kicks":
            stats["corners_home"] = statistic.get('homeValue')
            stats["corners_away"] = statistic.get('awayValue')
        elif name == "Offsides":
            stats["offsides_home"] = statistic.get('homeValue')
            stats["offsides_away"] = statistic.get('awayValue')
        elif name == "Fouls":
            stats["fouls_home"] = statistic.get('homeValue')
            stats["fouls_away"] = statistic.get('awayValue')
        elif name == "Yellow cards":
            stats["yellow_cards_home"] = statistic.get('homeValue')
            stats["yellow_cards_away"] = statistic.get('awayValue')
        elif name == "Red cards":
            stats["red_cards_home"] = statistic.get('homeValue')
            stats["red_cards_away"] = statistic.get('awayValue')
        elif name == "Free kicks":
            stats["free_kicks_home"] = statistic.get('homeValue')
            stats["free_kicks_away"] = statistic.get('awayValue')
        elif name == "Throw-ins":
            stats["throw_ins_home"] = statistic.get('homeValue')
            stats["throw_ins_away"] = statistic.get('awayValue')
        elif name == "Goal kicks":
            stats["goal_kicks_home"] = statistic.get('homeValue')
            stats["goal_kicks_away"] = statistic.get('awayValue')
    if stats["red_cards_home"] is None:
        stats["red_cards_home"] = 0
    if stats["red_cards_away"] is None:
        stats["red_cards_away"] = 0


def shotsExtra(statistics_items):
    for statistic in statistics_items:
        name = statistic.get('name')
        if name == "Big chances":
            stats["big_chances_home"] = statistic.get('homeValue')
            stats["big_chances_away"] = statistic.get('awayValue')
        elif name == "Big chances missed":
            stats["big_chances_missed_home"] = statistic.get('homeValue')
            stats["big_chances_missed_away"] = statistic.get('awayValue')
        elif name == "Counter attacks":
            stats["counter_attacks_home"] = statistic.get('homeValue')
            stats["counter_attacks_away"] = statistic.get('awayValue')
        elif name == "Counter attack shots":
            stats["counter_attacks_shots_home"] = statistic.get('homeValue')
            stats["counter_attacks_shots_away"] = statistic.get('awayValue')
        elif name == "Shots inside box":
            stats["shots_inside_box_home"] = statistic.get('homeValue')
            stats["shots_inside_box_away"] = statistic.get('awayValue')
        elif name == "Shots outside box":
            stats["shots_outside_box_home"] = statistic.get('homeValue')
            stats["shots_outside_box_away"] = statistic.get('awayValue')
        elif name == "Goalkeeper saves":
            stats["goalkeeper_saves_home"] = statistic.get('homeValue')
            stats["goalkeeper_saves_away"] = statistic.get('awayValue')


def passes(statistics_items):
    for statistic in statistics_items:
        name = statistic.get('name')
        if name == "Passes":
            stats["passes_home"] = statistic.get('homeValue')
            stats["passes_away"] = statistic.get('awayValue')
        elif name == "Accurate passes":
            stats["accurate_passes_home"] = statistic.get('homeValue')
            stats["accurate_passes_away"] = statistic.get('awayValue')
        elif name == "Long balls":
            stats["long_balls_home"] = statistic.get('homeValue')
            stats["long_balls_away"] = statistic.get('awayValue')
        elif name == "Crosses":
            stats["crosses_home"] = statistic.get('homeValue')
            stats["crosses_away"] = statistic.get('awayValue')


def duels(statistics_items):
    for statistic in statistics_items:
        name = statistic.get('name')
        if name == "Dribbles":
            stats["dribbles_home"] = statistic.get('homeValue')
            stats["dribbles_away"] = statistic.get('awayValue')
        elif name == "Possession lost":
            stats["possesion_lost_home"] = statistic.get('homeValue')
            stats["possesion_lost_away"] = statistic.get('awayValue')
        elif name == "Duels won":
            stats["duels_won_home"] = statistic.get('homeValue')
            stats["duels_won_away"] = statistic.get('awayValue')
        elif name == "Aerials won":
            stats["aerials_won_home"] = statistic.get('homeValue')
            stats["aerials_won_away"] = statistic.get('awayValue')


def defending(statistics_items):
    for statistic in statistics_items:
        name = statistic.get('name')
        if name == "Tackles":
            stats["tackles_home"] = statistic.get('homeValue')
            stats["tackles_away"] = statistic.get('awayValue')
        elif name == "Interceptions":
            stats["interceptions_home"] = statistic.get('homeValue')
            stats["interceptions_away"] = statistic.get('awayValue')
        elif name == "Clearances":
            stats["clearances_home"] = statistic.get('homeValue')
            stats["clearances_away"] = statistic.get('awayValue')


def getMatchStatistics(match_id):
    statistics = requests.get(statistics_api.format(
        match_id=match_id), headers=headers).json()

    all_period_data = next((item for item in statistics.get(
        'statistics', []) if item.get('period') == 'ALL'), None)
    if all_period_data is not None:
        # Acceder a los grupos dentro del periodo "ALL"
        groups = all_period_data.get('groups', [])

        # Iterar sobre cada grupo para obtener las estadísticas
        for group in groups:
            group_name = group.get('groupName')
            statistics_items = group.get('statisticsItems', [])

            if group_name == "Expected":
                expectedGoals(statistics_items)
            elif group_name == "Possession":
                possession(statistics_items)
            elif group_name == "Shots":
                shots(statistics_items)
            elif group_name == "TVData":
                tvData(statistics_items)
            elif group_name == "Shots extra":
                shotsExtra(statistics_items)
            elif group_name == "Passes":
                passes(statistics_items)
            elif group_name == "Duels":
                duels(statistics_items)
            elif group_name == "Defending":
                defending(statistics_items)
    else:
        print('No se encontró el periodo "ALL"')


def restartStats():
    global stats
    global stats_keys
    stats = {key: None for key in stats_keys}
    return stats


if __name__ == '__main__':
    competition_id = 17
    season_id = 41886
    year = "2022-23"

    # Abre un archivo CSV para escribir. Asegúrate de especificar el modo newline=''
    with open(f'stats/stats_{year}_premier.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=stats_keys)

        # Escribe los encabezados de columna
        writer.writeheader()

        for round in range(1, 39):
            print(f"Round {round}")
            events = getRoundData(competition_id, season_id, round)
            for event in events:
                stats = restartStats()
                stats["round"] = round
                status = event.get('status', {}).get('code', 0)
                if status == 100:
                    getMatchScore(event)
                    match_id = getMatchId(event)
                    getMatchStatistics(match_id)

                    # Escribe la fila actual en el archivo CSV
                    writer.writerow(stats)
