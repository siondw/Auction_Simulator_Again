import pandas as pd
from .Player import Player


class PlayerImporter:
    @staticmethod
    def import_players_from_csv(file_path):
        data = pd.read_csv(file_path)
        players = [
            Player(
                name=row['Player Name'],
                pos=row['Position'],
                nfl_team=row['Team'],
                projected_points=row['Projected Points'],
                estimated_value=row['Adjusted Value'],
                positional_rank=row['Rank']
            ) for index, row in data.iterrows()
        ]
        return players