import pandas as pd
from bogan.main.lib.event_analysis import get_game_list

import datetime

# Beispiel-Daten
event_name = "Spielewochenende 2024/1"
games_data = get_game_list(event_name)
# games_data = [
#     {'datum': datetime.date(2024, 6, 29), 'name': 'Twilight Imperium: Fourth Edition', 'playtime': 565, 'game_bgg_id': 86322669, 'img_small': 'https://cf.geekdo-images.com/_Ppn5lssO5OaildSE-FgFA__thumb/img/lfEukJE0JsoZZObaF9K9YnFp62E=/fit-in/200x150/filters:strip_icc()/pic3727516.jpg', 'players': [{'name': 'Jochen', 'punkte': 10.0}, {'name': 'Strähli', 'punkte': 9.0}, {'name': 'Simon D.', 'punkte': 8.0}, {'name': 'Uddi', 'punkte': 6.0}, {'name': 'Lasse', 'punkte': 5.0}]},
#     {'datum': datetime.date(2024, 6, 28), 'name': 'Magic: The Gathering – Jumpstart 2022', 'playtime': 122, 'game_bgg_id': 86269672, 'img_small': 'https://cf.geekdo-images.com/wmkDcusjk4a7E1xyIgAqbQ__thumb/img/T1iaY5THgba83EJi5dtSt0VOfi0=/fit-in/200x150/filters:strip_icc()/pic7225434.jpg', 'players': [{'name': 'Lasse', 'punkte': 12.0}, {'name': 'Simon D.', 'punkte': 9.0}, {'name': 'Uddi', 'punkte': 6.0}, {'name': 'Jochen', 'punkte': 3.0}, {'name': 'Strähli', 'punkte': 0.0}]},
#     {'datum': datetime.date(2024, 6, 28), 'name': 'New York Zoo', 'playtime': 45, 'game_bgg_id': 86273367, 'img_small': 'https://cf.geekdo-images.com/8vqr1uYik715mqDqy0W9vg__thumb/img/Bu97VesRjdbQO2PxfuOrdC6icd8=/fit-in/200x150/filters:strip_icc()/pic5673404.jpg', 'players': [{'name': 'Simon D.', 'punkte': 5.0}, {'name': 'Strähli', 'punkte': 4.0}, {'name': 'Lasse', 'punkte': 3.0}, {'name': 'Uddi', 'punkte': 2.0}, {'name': 'Jochen', 'punkte': 1.0}]},
#     {'datum': datetime.date(2024, 6, 28), 'name': 'Power Grid', 'playtime': 150, 'game_bgg_id': 86264487, 'img_small': 'https://cf.geekdo-images.com/yd6LuatytHRhcFCxCf-EEg__thumb/img/jWTonZ5oYNlPzpELKHIJGWSS0Y8=/fit-in/200x150/filters:strip_icc()/pic4459753.jpg', 'players': [{'name': 'Simon D.', 'punkte': 15.25}, {'name': 'Uddi', 'punkte': 15.25}, {'name': 'Strähli', 'punkte': 15.13}, {'name': 'Jochen', 'punkte': 14.25}, {'name': 'Lasse', 'punkte': 14.22}]},
#     {'datum': datetime.date(2024, 6, 28), 'name': 'Tapestry', 'playtime': 183, 'game_bgg_id': 86284150, 'img_small': 'https://cf.geekdo-images.com/7kqDmkUMGxXHr1wNPA7Gvg__thumb/img/1najF3Bh3QI7k2c9sJeTXznbvPU=/fit-in/200x150/filters:strip_icc()/pic4884996.jpg', 'players': [{'name': 'Simon D.', 'punkte': 201.0}, {'name': 'Uddi', 'punkte': 192.0}, {'name': 'Lasse', 'punkte': 170.0}, {'name': 'Strähli', 'punkte': 159.0}, {'name': 'Jochen', 'punkte': 95.0}]},
#     {'datum': datetime.date(2024, 6, 27), 'name': 'Cartographers', 'playtime': 64, 'game_bgg_id': 86251818, 'img_small': 'https://cf.geekdo-images.com/GifbnAmsA4lfEcDkeaC9VA__thumb/img/TTxZzwbna07hMcPQ0xaFtT10egE=/fit-in/200x150/filters:strip_icc()/pic4397932.png', 'players': [{'name': 'Lasse', 'punkte': 83.0}, {'name': 'Strähli', 'punkte': 64.0}, {'name': 'Simon D.', 'punkte': 53.0}, {'name': 'Uddi', 'punkte': 47.0}, {'name': 'Jochen', 'punkte': 27.0}]},
#     {'datum': datetime.date(2024, 6, 27), 'name': 'Cartographers', 'playtime': 51, 'game_bgg_id': 86253552, 'img_small': 'https://cf.geekdo-images.com/GifbnAmsA4lfEcDkeaC9VA__thumb/img/TTxZzwbna07hMcPQ0xaFtT10egE=/fit-in/200x150/filters:strip_icc()/pic4397932.png', 'players': [{'name': 'Jochen', 'punkte': 65.0}, {'name': 'Lasse', 'punkte': 64.0}, {'name': 'Strähli', 'punkte': 63.0}, {'name': 'Uddi', 'punkte': 59.0}, {'name': 'Simon D.', 'punkte': 55.0}]}
# ]


# Helper function to calculate the points based on position
def calculate_position_points(n, positions, weight=1, playtime=60):
    base_points = [(n - (i * 2 * n) / (n - 1)) * weight * (playtime/60) for i in range(n)]
    final_points = []
    i = 0
    while i < len(positions):
        current_rank = positions[i]
        same_rank_count = positions.count(current_rank)
        if same_rank_count > 1:
            avg_points = sum(base_points[i : i + same_rank_count]) / same_rank_count
            final_points.extend([avg_points] * same_rank_count)
            i += same_rank_count
        else:
            final_points.append(base_points[i])
            i += 1
    return final_points


# Prepare a list to store the final scores
all_scores = []

# Process each game
for game in games_data:
    players = game["players"]
    n = len(players)
    points = [player["punkte"] for player in players]

    # Sort players by their points in descending order
    sorted_players = sorted(players, key=lambda x: x["punkte"], reverse=True)
    sorted_positions = [p["punkte"] for p in sorted_players]

    # Calculate position points
    position_points = calculate_position_points(n, sorted_positions)
    position_points_playtime = calculate_position_points(n, sorted_positions, playtime=game["playtime"])
    position_points_weight = calculate_position_points(n, sorted_positions, weight=game["weight"])

    # Assign the calculated points to the players
    for i, player in enumerate(sorted_players):
        player["tabellenpunkte"] = position_points[i]
        player["tabellenpunkte_playtime"] = position_points_playtime[i]
        player["tabellenpunkte_weight"] = position_points_weight[i]

    # Add the points to the all_scores list
    for player in sorted_players:
        all_scores.append(
            {
                "name": player["name"],
                "tabellenpunkte": player["tabellenpunkte"],
                "tabellenpunkte_playtime": player["tabellenpunkte_playtime"],
                "tabellenpunkte_weight": player["tabellenpunkte_weight"],
                "datum": game["datum"],
            }
        )

# Create a DataFrame from the all_scores list
df_scores = pd.DataFrame(all_scores)

# Summarize the points for each player
df_summary = df_scores.groupby("name")["tabellenpunkte"].sum().reset_index()
df_summary = df_summary.sort_values(by="tabellenpunkte", ascending=False).reset_index(drop=True)


# Summarize the points with weight
df_summary_weight = df_scores.groupby("name")["tabellenpunkte_weight"].sum().reset_index()
df_summary_weight = df_summary_weight.sort_values(by="tabellenpunkte_weight", ascending=False).reset_index(
    drop=True
)

# Summarize the points with playtime
df_summary_playtime = df_scores.groupby("name")["tabellenpunkte_playtime"].sum().reset_index()
df_summary_playtime = df_summary_playtime.sort_values(by="tabellenpunkte_playtime", ascending=False).reset_index(
    drop=True
)

print(f"==={event_name}===")
print("Normal calculation:")
print(df_summary)
print("Weight calculation")
print(df_summary_weight)
print("Duration calculation")
print(df_summary_playtime)

# # Plot the ranking over time
# import matplotlib.pyplot as plt

# # Calculate cumulative points over time for each player
# df_scores['cumulative_points'] = df_scores.groupby('name')['tabellenpunkte'].cumsum()

# # Pivot the DataFrame to get a time series for each player
# df_pivot = df_scores.pivot(index='datum', columns='name', values='cumulative_points').fillna(0)

# # Plot the cumulative points for each player
# plt.figure(figsize=(12, 8))

#######################################################################################################################

# event_name = "Spielewochenende 2024/1"
# x = get_game_list(event_name)
# print(f"============{event_name}=====================")
# print(x)
# print(f"============{event_name}=====================")
# df = pd.DataFrame(x)

# df.to_html()

# # print(df)
