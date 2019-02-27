from flask import Flask, render_template, request, redirect
from random import randint

app = Flask(__name__)


class Field:
    def __init__(self, player=None, value=0):
        self.player = player
        self.value = value

    def place(self, placing_player):
        if self.player == placing_player:
            self.value += 1
        elif self.player is None:
            self.player = placing_player
            self.value = 1
        else:  # przeciwny gracz
            place_on_band(self.player)
            self.player = placing_player

    def remove(self):
        self.value -= 1
        if self.value == 0:
            self.player = None


board = [Field() for i in range(25)]
band = {'b': 0, 'w': 0}
player = 'b'
dice = [0, 0]
double_dice_value = 0
choice = 0
double = False
band_empty = {'b': True, 'w': True}
second_stage = {'b': False, 'w': False}
home_b = 0
home_w = 0
cant_move_b = False
cant_move_w = False


def place_on_band(player):
    band[player] += 1
    band_empty[player] = False


def prepare_board():
    global board, dice, band, player, choice, double, band_empty, second_stage, home_b, home_w, cant_move_b, cant_move_w, double_dice_value
    board = [Field() for i in range(25)]
    board[1] = Field('b', 2)
    board[6] = Field('w', 5)
    board[8] = Field('w', 3)
    board[12] = Field('b', 5)
    board[13] = Field('w', 5)
    board[17] = Field('b', 3)
    board[19] = Field('b', 5)
    board[24] = Field('w', 2)
    band = {'b': 0, 'w': 0}
    player = 'b'
    dice = [0, 0]
    double_dice_value = 0
    choice = 0
    double = False
    band_empty = {'b': True, 'w': True}
    second_stage = {'b': False, 'w': False}
    home_b = 0
    home_w = 0
    cant_move_b = False
    cant_move_w = False


def first_stage_move(chosen_field):
    global board, choice, dice, player
    if choice == 0:
        choice = chosen_field
    else:
        if chosen_field == choice:
            choice = 0
        else:
            diff = chosen_field - choice
            if i_can_move(diff, chosen_field):
                board[chosen_field].place(player)
                board[choice].remove()
                dice[dice.index(abs(diff))] = 0
                choice = 0
                if dice[0] == 0 and dice[1] == 0:
                    dices_are_0()


def i_can_move(diff, chosen_field):
    global board, dice, player
    if abs(diff) not in dice:
        return False
    if board[chosen_field].value > 1 and board[chosen_field].player is not player:
        return False
    if player == 'b' and diff < 0:
        return False
    if player == 'w' and diff > 0:
        return False
    return True


def dices_are_0():
    global double, dice, double_dice_value
    if not double:
        swap_player()
    else:
        double = False
        dice[0] = double_dice_value
        dice[1] = double_dice_value


def swap_player():
    global player
    if player is 'b':
        player = 'w'
    else:
        player = 'b'


def check_vals():
    global dice, choice
    if player == 'b':
        for i in range(18, choice):
            if board[i].player is 'b':
                return False
        if dice[0] >= dice[1]:
            if dice[0] > 25-choice:
                dice[0] = 0
                if dice[0] == 0 and dice[1] == 0:
                    dices_are_0()
                return True
            else:
                return False
        else:
            if dice[1] > 25 - choice:
                dice[1] = 0
                if dice[0] == 0 and dice[1] == 0:
                    dices_are_0()
                return True
            else:
                return False
    if player == 'w':
        for i in range(6, choice, -1):
            if board[i].player is 'w':
                return False
        if dice[0] >= dice[1]:
            if dice[0] > choice:
                dice[0] = 0
                if dice[0] == 0 and dice[1] == 0:
                    dices_are_0()
                return True
            else:
                return False
        else:
            if dice[1] > choice:
                dice[1] = 0
                if dice[0] == 0 and dice[1] == 0:
                    dices_are_0()
                return True
            else:
                return False


def second_stage_move(chosen_field):
    global player, board, dice, home_b, home_w, choice
    if choice == 0:
        choice = chosen_field
    else:
        if chosen_field == choice:
            choice = 0
        else:
            if player == 'b':
                if chosen_field == 25:
                    if 25 - choice in dice:
                        board[choice].remove()
                        home_b += 1
                        dice[dice.index(25 - choice)] = 0
                        choice = 0
                        if dice[0] == 0 and dice[1] == 0:
                            dices_are_0()
                        return
                    else:
                        if check_vals():
                            board[choice].remove()
                            home_b += 1
                            choice = 0
                            return
                        else:
                            return
                else:
                    diff = chosen_field - choice
                    if i_can_move(diff, chosen_field):
                        board[chosen_field].place(player)
                        board[choice].remove()
                        dice[dice.index(abs(diff))] = 0
                        choice = 0
                        if dice[0] == 0 and dice[1] == 0:
                            dices_are_0()
                    return
            if player == 'w':
                if chosen_field == -1:
                    if choice in dice:
                        board[choice].remove()
                        home_w += 1
                        dice[dice.index(choice)] = 0
                        choice = 0
                        if dice[0] == 0 and dice[1] == 0:
                            dices_are_0()
                        return
                    else:
                        if check_vals():
                            board[choice].remove()
                            home_w += 1
                            choice = 0
                            return
                        else:
                            return
                else:
                    diff = chosen_field - choice
                    if i_can_move(diff, chosen_field):
                        board[chosen_field].place(player)
                        board[choice].remove()
                        dice[dice.index(abs(diff))] = 0
                        choice = 0
                        if dice[0] == 0 and dice[1] == 0:
                            dices_are_0()
                    return


def band_move(chosen_field):
    global board, player, dice, cant_move_b, cant_move_w
    if player == 'b':
        if dice[0] > 0 and dice[1] > 0:
            if board[dice[0]].value > 1 and board[dice[0]].player is not player and board[dice[1]].value > 1 \
                    and board[dice[1]].player is not player:
                cant_move_b = True
                dice[0] = 0
                dice[1] = 0
                dices_are_0()
                return
        elif dice[0] > 0 and dice[1] == 0:
            if board[dice[0]].value > 1 and board[dice[0]].player is not player:
                dice[0] = 0
                cant_move_b = True
                dices_are_0()
                return
        elif dice[1] > 0 and dice[0] == 0:
            if board[dice[1]].value > 1 and board[dice[1]].player is not player:
                dice[1] = 0
                cant_move_b = True
                dices_are_0()
                return
        if chosen_field > 6 or chosen_field not in dice:
            return
        elif board[chosen_field].value > 1 and board[chosen_field].player is not player:
            return
        else:
            board[chosen_field].place(player)
            dice[dice.index(chosen_field)] = 0
            band[player] -= 1
            cant_move_b = False
            if band[player] == 0:
                band_empty[player] = True
            if dice[0] == 0 and dice[1] == 0:
                dices_are_0()
            return
    elif player == 'w':
        if dice[0] > 0 and dice[1] > 0:
            if board[25 - dice[0]].value > 1 and board[25 - dice[0]].player is not player and board[
                25 - dice[1]].value > 1 \
                    and board[25 - dice[1]].player is not player:
                cant_move_w = True
                dice[0] = 0
                dice[1] = 0
                dices_are_0()
                return
        elif dice[0] > 0 and dice[1] == 0:
            if board[25 - dice[0]].value > 1 and board[25 - dice[0]].player is not player:
                dice[0] = 0
                cant_move_w = True
                dices_are_0()
                return
        elif dice[1] > 0 and dice[0] == 0:
            if board[25 - dice[1]].value > 1 and board[25 - dice[1]].player is not player:
                dice[1] = 0
                cant_move_w = True
                dices_are_0()
                return
        if chosen_field < 19 or (25-chosen_field) not in dice:
            return
        if board[chosen_field].value > 1 and board[chosen_field].player is not player:
            return
        else:
            board[chosen_field].place(player)
            dice[dice.index(25-chosen_field)] = 0
            band[player] -= 1
            cant_move_w = False
            if band[player] == 0:
                band_empty[player] = True
            if dice[0] == 0 and dice[1] == 0:
                dices_are_0()
            return


def check_second_stages():
    global board, second_stage
    count_b = 0
    count_w = 0
    for i in range(7):
        if board[i].player == 'w':
            count_w += board[i].value
    for i in range(19, 25):
        if board[i].player == 'b':
            count_b += board[i].value
    if count_w + home_w == 15:
        second_stage['w'] = True
    else:
        second_stage['w'] = False
    if count_b + home_b == 15:
        second_stage['b'] = True
    else:
        second_stage['b'] = False


def remember_dices():
    global double_dice_value, dice
    double_dice_value = dice[0]


@app.route('/roll')
def roll_a_dice():
    global dice, double
    dice[0] = randint(1, 6)
    dice[1] = randint(1, 6)
    if dice[0] == dice[1]:
        double = True
        remember_dices()
    return redirect('game')


@app.route('/move', methods=['POST', 'GET'])
def move():
    global band, player, home_w, home_b
    chosen_field = int(request.args.get('choice', None))
    if band[player] > 0:
        band_move(chosen_field)
    else:
        if player == 'b' and second_stage['b']:
            second_stage_move(chosen_field)
            if home_b == 15:
                return redirect('won')
        elif player == 'w' and second_stage['w']:
            second_stage_move(chosen_field)
            if home_w == 15:
                return redirect('won')
        else:
            first_stage_move(chosen_field)
    check_second_stages()
    return redirect('game')


@app.route('/')
def index():
    prepare_board()
    return render_template('index.html')


@app.route('/reset')
def reset():
    prepare_board()
    return redirect('game')


@app.route('/game')
def game():
    return render_template('main.html', board=board, band=band, player=player, dice=dice, choice=choice,
                           band_empty=band_empty, home_w=home_w, home_b=home_b, second_stage=second_stage,
                           cant_move_w=cant_move_w, cant_move_b=cant_move_b)


@app.route('/won')
def won():
    return render_template('won.html', player=player)


if __name__ == '__main__':
    app.run()
