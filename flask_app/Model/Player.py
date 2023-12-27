class Player:
    def __init__(self, name, pos, nfl_team, projected_points, estimated_value, positional_rank):
        self.name = name
        self.pos = pos
        self.nfl_team = nfl_team
        self.projected_points = projected_points
        self.estimated_value = estimated_value
        self.positional_rank = positional_rank
        self.drafted = False

    def to_dict(self):
        return {
            'name': self.name,
            'pos': self.pos,
            'nfl_team': self.nfl_team,
            'projected_points': float(self.projected_points),
            'estimated_value': int(self.estimated_value),
            'positional_rank': int(self.positional_rank),
            'drafted': self.drafted
        }

    def __str__(self):
        return f"{self.name} ({self.pos}, {self.nfl_team})"

    def get_name(self):
        return self.name

    def get_position(self):
        return self.pos

    def get_team(self):
        return self.nfl_team

    def get_projected_points(self):
        return self.projected_points

    def mark_as_drafted(self):
        self.drafted = True

    def is_drafted(self):
        return self.drafted

    def get_value(self):
        return self.estimated_value

    def get_positional_rank(self):
        return self.positional_rank

