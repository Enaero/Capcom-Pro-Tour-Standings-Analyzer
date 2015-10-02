from copy import deepcopy


class Player(object):

    def __init__(self, name, points):
        self.name = name
        self.points = points


class Tournament(object):

    """
    List of points available in a tournament.
    Popping and removing can be optimized if a more sophisticated ordered
    data structure is used, but given the small nature of the data set
    I didn't think it was important.
    """

    def __init__(self, points):
        self.points = deepcopy(points)
        self.points.sort()

    def peek(self):
        return self.points[-1] if self.points else 0

    def pop(self):
        return self.points.pop() if self.points else 0

    def find(self, value):
        """
        Finds the first element that is greater than value.
        """
        for i in range(len(self.points)):
            if self.points[i] > value:
                return self.points[i]

    def remove(self, value):
        """
        Removes the first element that is greater than value.
        """
        for i in range(len(self.points)):
            if self.points[i] > value:
                removed = self.points[i]
                del self.points[i]
                return removed

    def __str__(self):
        return str(self.points)


class TournamentList(object):

    """
    Container for tournaments.
    Can be optimized if using an ordered structure.
    Currently has to sort after each potentiall disruptive operation.
    """

    def __init__(self, tournaments):
        self.tournaments = deepcopy(tournaments)
        self.sort()

    def peek(self, index=0):
        if self.tournaments:
            return self.tournaments[index].peek()

    def sort(self):
        """
        Sorts the tournaments but the highest 1st place points available.
        NOT by total points.
        """
        self.tournaments.sort(key=lambda tourney: tourney.peek())

    def pop(self, index=0):
        if self.tournaments:
            result = self.tournaments[index].pop()
            self.sort()
            return result

    def remove(self, value, index=0):
        """
        Removes the smallest prize greater than value.
        """
        if not self.tournaments:
            raise ValueError("Nothing in list")

        smallest = self.tournaments[index]
        smallest_value = smallest.find(value)

        for tourney in self.tournaments[index:]:
            candidate = tourney.find(value)
            if candidate < smallest_value:
                smallest = tourney
                smallest_value = candidate
        removed = smallest.remove(value)
        self.sort()
        return removed

    def __str__(self):
        result = ''
        for i in self.tournaments:
            result += str(i)
            result += '\n'
        return result


def worst_case_rank(ranking_list, player_index, tournaments):
    """
    Returns the worst possible ranking for a player by the end of
    the year given their current ranking.
    """
    player = ranking_list[player_index]
    worst_rank = player_index

    for other in ranking_list[player_index+1:]:
        surpass = player.points - other.points
        points = other.points

        count = 0
        while (
            count < len(tournaments.tournaments) and
            tournaments.peek(count) + points < player.points
        ):
            points += tournaments.pop(count)
            count += 1

        if count == len(tournaments.tournaments):
            return worst_rank

        surpass = player.points - points
        removed = tournaments.remove(surpass, count)
        points += removed
        worst_rank += 1
        print(
            other.name, other.points, 'surpasses',
            player.name, 'by gaining', points-other.points
        )
    return worst_rank


if __name__ == "__main__":
    ranking = []
    with open("standings.txt", 'rt') as fp:
        for line in fp:
            data = line.split(' ')
            if len(data) > 2 and data[2].strip() == 'Qualified':
                continue  # skip players who qualified
            name = data[0]
            points = int(data[1])
            ranking.append(Player(name, points))

    tournament_tiers = {}
    with open("Ranking Point Matrix.txt", 'rt') as fp:
        for line in fp:
            data = line.split(' ')
            tier = data[0].lower().strip()
            tournament_tiers[tier] = []
            if tier == 'premier' or tier == 'evoloution':
                start = 2
            else:
                start = 1
            for value in data[start:]:  # Skip 1st place
                tournament_tiers[tier].append(int(value))

    tournaments = []
    with open("schedule.txt", 'rt') as fp:
        for tier in fp:
            tier = tier.lower().strip()
            tournaments.append(Tournament(tournament_tiers[tier]))

    tlist = TournamentList(tournaments)
    index = 0
    print(
        "The lowest ranking", ranking[index].name,
        "can get is", worst_case_rank(ranking, index, tlist)+1
    )
