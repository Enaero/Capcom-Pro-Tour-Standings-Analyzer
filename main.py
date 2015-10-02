import bisect


class Player(object):
    def __init__(self, name, points):
        self.name = name
        self.points = points


def worst_case_rank(ranking_list, player_index, points_left):
    reference_points = ranking_list[player_index].points

    worst_rank = player_index
    prev_points = reference_points
    points_left_index = len(points_left)-1
    max_points_gain = points_left[points_left_index]
    for player in ranking_list[player_index+1:]:
        # list needs to be in descending order
        if player.points > prev_points:
            raise ValueError("ranking_list not sorted"
                             "or sorted in wrong order.")
        prev_points = player.points
        
        # It is possible to be taken over by someone with equal points
        # Whatever tie breaker system they have, assume the worst outcome
        # for the player in question
        points_to_surpass = reference_points - player.points

        if points_to_surpass <= max_points_gain:
            points_left_index -= 1
            max_points_gain = points_left[points_left_index]
            worst_rank += 1
        else:
            return worst_rank
        if points_left_index < 0:
            return worst_rank

    return worst_rank
        
    
if __name__ == "__main__":
    ranking = []
    with open("October 2, 2015 Standings.txt", 'rt') as fp:
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
            for value in data[2:]:  #Skip 1st place
                tournament_tiers[tier].append(int(value))

    points_left = []
    with open("schedule.txt", 'rt') as fp:
        for tier in fp:
            tier = tier.lower().strip()
            points_left.extend(tournament_tiers[tier])

    points_left.sort()


    # Can do a binary search here
    # But who cares on a list this size...
    count = 0
    for i in range(len(ranking)):
        if worst_case_rank(ranking, i, points_left) < 16:
            print(ranking[i].name)
            count += 1
    print(count, "unqualified players are guaranteed a spot.")

