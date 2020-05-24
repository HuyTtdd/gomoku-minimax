from copy import deepcopy

SIZE = 20  # 20x20


class State():
    def __init__(self):
        self.table = self.create_table()
        self.signs = []

    def set_cell(self, position, player):
        self.table[position[0]][position[1]] = self.get_sign(player)

    def reset_cell(self, position):
        self.table[position[0]][position[1]] = "_"

    def get_sign(self, player):
        return self.signs[player % 2]

    def set_signs(self, player_sign):
        if player_sign == 0:
            self.signs = ["x", "o"]
        else:
            self.signs = ["o", "x"]

    def create_table(self):
        return [["_"] * SIZE for _ in range(SIZE)]

    def print_table(self):
        for row in self.table:
            print(*row, sep=" ")


class Gomoku():
    def __init__(self, player):
        self.state = State()
        self.state.set_signs(player)
        self.sign = self.state.get_sign(player)
        self.player = player

    def move(self, position):
        if validate_move(self.state.table, position):
            self.state.set_cell(position, self.player)

            if check_state(self.state.table, position):
                return 5, self.sign

            if self.player == 399:
                return 6, self.sign

            self.player += 1
            self.sign = self.state.get_sign(self.player)

            return 1, self.state.get_sign(self.player - 1)
        else:
            return -1, self.state.get_sign(self.player - 1)

    def bot(self):
        position = bot(self.state.table, self.player,
                       self.state.signs, depth=2)

        code, sign = self.move(position)

        return code, sign, position


def bot(table, player, signs, depth, root=True, alpha=-999999, beta=999999):
    # Minimax with alpha-beta pruning
    state = State()
    state.table = deepcopy(table)
    state.signs = signs
    move = ()

    if player == 399 or depth == 0:
        return calc_score(state.table)

    if state.get_sign(player) == "x":
        best_score = -999999
        for i in range(SIZE):
            for j in range(SIZE):
                if validate_move(state.table, (i, j)) and has_neighbor(state.table, (i, j)):
                    state.set_cell((i, j), player)

                    score = bot(state.table, player+1, signs,
                                depth-1, False, alpha, beta)

                    if score >= best_score:
                        best_score = score
                        move = (i, j)

                    if best_score > alpha:
                        alpha = best_score

                    if alpha > beta:
                        if root:
                            return (i, j)
                        return best_score

                    state.reset_cell((i, j))
    else:
        best_score = 999999
        for i in range(SIZE):
            for j in range(SIZE):
                if validate_move(state.table, (i, j)) and has_neighbor(state.table, (i, j)):
                    state.set_cell((i, j), player)

                    score = bot(state.table, player+1, signs,
                                depth-1, False, alpha, beta)

                    if score <= best_score:
                        best_score = score
                        move = (i, j)

                    if best_score < beta:
                        beta = best_score

                    if alpha > beta:
                        if root:
                            return (i, j)
                        return best_score

                    state.reset_cell((i, j))

    if root:
        return move
    return best_score


def calc_score(table):
    score = 0

    for i in range(SIZE):
        for j in range(SIZE):
            if table[i][j] != "_" or has_neighbor(table, [i, j]):
                row = "".join(get_row(table, (i, j)))
                column = "".join(get_column(table, (i, j)))
                lslash = "".join(get_lslash(table, (i, j)))
                rslash = "".join(get_rslash(table, (i, j)))

                score += _calc_score(row)
                score += _calc_score(column)
                score += _calc_score(lslash)
                score += _calc_score(rslash)

    return score


def _calc_score(list_):
    scores = {0: 99999, 1: 900, 2: 90, 3: 90, 4: 90, 5: 90,
              6: 90, 7: 50, 8: 5, 9: 5, 10: 2, 11: 2, 12: 2, 13: 2}
    pattern_x = ["xxxxx", "_xxxx_", "xxxx_", "_xxxx", "xxx_x", "xx_xx",
                 "x_xxx", "_xxx_", "xxx_", "_xxx", "_x_x_", "_xx_", "_xx", "xx_"]
    pattern_o = ["ooooo", "_oooo_", "oooo_", "_oooo", "ooo_o", "oo_oo",
                 "o_ooo", "_ooo_", "ooo_", "_ooo", "_o_o_", "_oo_", "_oo", "oo_"]

    score = 0

    for index, pattern in enumerate(pattern_x):
        z = list_.find(pattern)
        if z != -1:
            score += scores[index]
            break

    for index, pattern in enumerate(pattern_o):
        z = list_.find(pattern)
        if z != -1:
            score -= scores[index]
            break

    return score


def check_state(table, p):
    sign = table[p[0]][p[1]]

    row = get_row(table, p)
    column = get_column(table, p)
    lslash = get_lslash(table, p)
    rslash = get_rslash(table, p)

    return check_win(row, sign) or check_win(column, sign) or check_win(lslash, sign) or check_win(rslash, sign)


def check_win(list_, sign):
    if len(list_) < 5:
        return False

    for i in range(len(list_) - 4):
        if all(map(lambda x: x == sign, list_[i:i+5])):
            return True

    return False


def has_neighbor(table, p):
    pos = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
           (1, 1), (1, 0), (1, -1), (0, -1)]

    for i in pos:
        try:
            if table[p[0]+i[0]][p[1]+i[1]] != "_":
                return True
        except IndexError:
            continue
    return False


def get_row(table, p):
    return table[p[0]][max(p[1]-4, 0): min(p[1]+5, SIZE)]


def get_column(table, p):
    return [table[i][p[1]] for i in range(max(p[0]-4, 0), min(p[0]+5, SIZE))]


def get_lslash(table, p):
    lslash_1 = [table[p[0]+i][p[1]+i]
                for i in range(min(5, SIZE - max(p[0], p[1])))]
    lslash = [table[p[0]-i][p[1]-i]
              for i in range(1, min(5, p[0]+1, p[1]+1))][::-1]

    lslash.extend(lslash_1)

    return lslash


def get_rslash(table, p):
    rslash_1 = [table[p[0]-i][p[1]+i]
                for i in range(min(p[0] - max(p[0]-5, -1), min(p[1]+5, SIZE) - p[1]))]

    rslash = [table[p[0]+i][p[1]-i]
              for i in range(1, min(min(p[0]+5, SIZE) - p[0], p[1] - max(p[1]-5, -1)))][::-1]

    rslash.extend(rslash_1)

    return rslash


def validate_move(table, position):
    return table[position[0]][position[1]] == "_"
