import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import slippi
from slippi import Game
import os
import sys
import matplotlib.image as mpimg
import matplotlib
import gc

def damage_taken(pre_frame, post_frame):
    return post_frame.damage - pre_frame.damage

def character_names(char):
    global all_characters
    for character in all_characters:
        if character[0] == char:
            return character[1]

    return

def stage_filenames(stage):
    global all_stages
    for map in all_stages:
        if map[0] == stage: return map[2]
    return None

def stage_name(stage):
    global all_stages
    for map in all_stages:
        if map[0] == stage: return map[1]
    return None

def is_damaged(state):
    damage_bool = (75 <= state <= 91)
    return damage_bool

def is_grabbed(state):
    grabbed_bool = (223 <= state <=236)
    return grabbed_bool

def is_teching(state):
    tech_bool = (199 <= state <= 204)
    return tech_bool

def is_in_control(state):

    ground = 14 <= state <= 24
    squat = 39 <= state <= 41
    ground_attack = 44 <= state <= 64
    grabbing = state == 212

    return ground or squat or ground_attack or grabbing

def is_dead(state):
    return 0 <= state <= 10

def is_attacking(state):
    return 44 <= state <= 69

def is_grabbing(state):
    return state == 212 or state == 214

def is_holding(state):
    return state == 213 or 215 <= state <= 218

def is_respawn(state):
    return state == 12 or state == 13

def add_game(game, characters, fname):
    global all_games
    puff_port = characters[0][0]
    peach_port = characters[1][0]
    game_data = {'puff_port' : puff_port,
                 'peach_port': peach_port,
                 'stage' : stage_name(game.start.stage),
                 'duration': game.metadata.duration,
                 'filename': fname}
    all_games = all_games.append(game_data, ignore_index = True)
    return

def getPositionPoints(stage, stage_name, fname, char):
    input_char = char
    print(char)
    stage_to_positions = {
        fod[1]: list(),
        stadium[1]: list(),
        dreamland[1]: list(),
        yoshis[1]: list(),
        bf[1]: list(),
        fd[1]: list()}
    stage_games = all_games[all_games.stage == stage_name]

    for index, row in stage_games.iterrows():

        game = Game('games/' + str(row.filename))

            # Every half second (30 frames), record character's position
        for frame in game.frames[0::30]:
            if input_char == 'puff':
                stage_to_positions[stage_name].append(frame.ports[row.puff_port].leader.post.position)

            elif input_char == 'peach':
                stage_to_positions[stage_name].append(frame.ports[row.peach_port].leader.post.position)


    x_pos = [p.x for p in stage_to_positions[stage_name]]
    y_pos = [p.y for p in stage_to_positions[stage_name]]
    return x_pos, y_pos

def graphPositionPoints(char):
    input_char = char
    for stage, stage_name, fname in all_stages:
        x_pos, y_pos = getPositionPoints(stage, stage_name, fname, input_char)
        char_pos = sns.kdeplot(x_pos, y_pos, cmap="Reds", shade=False, thresh = 0.05, n_levels = 20)

        fig = plt.gcf()
        fig.set_size_inches(15, 15)
        x_left, x_right = stage_boundaries[stage_name][0]
        y_bottom, y_top = stage_boundaries[stage_name][1]

        plt.xlim(x_left, x_right)
        plt.ylim(y_bottom, y_top)
        plt.axis('off')

        map_img = mpimg.imread('stages/' + fname)

    #put the map under the heatmap
        char_pos_plot = char_pos.imshow(map_img, aspect = char_pos.get_aspect(), extent = char_pos.get_xlim() + char_pos.get_ylim(), zorder = 0)


        plt.show()
    return char_pos_plot

def getNeutralWins(game, char_port, opp_port):
    # The time a character must be in control for neutral to be re-established
    # Currently set to one-and-a-half seconds
    DISENGAGE = 90

    # Time since the opponent was last hit with an attack
    opp_time_since_hit = 9999

    conversions = list()
    current_combo = list()

    # Whether we can count a kill as 'new'
    kill_registerable = True

    prev_frame = game.frames[0]
    prev_j_state = prev_frame.ports[char_port].leader.post.state
    prev_opp_state = prev_frame.ports[opp_port].leader.post.state

    # Whether the game is in neutral (as oppposed to punish)
    neutral = True

    for frame in game.frames[1:]:

        f_index = str(frame.index)

        j_data = frame.ports[char_port].leader.post
        opp_data = frame.ports[opp_port].leader.post

        j_state = j_data.state
        opp_state = opp_data.state

        j_damaged = is_damaged(j_state)
        j_grabbed = is_grabbed(j_state)
        j_damage_taken = damage_taken(prev_frame.ports[char_port].leader.post, j_data)
        j_dead = is_dead(j_state)
        j_attacking = is_attacking(j_state)
        j_grabbing = is_grabbing(j_state)
        j_holding = is_holding(j_state)
        j_in_control = is_in_control(j_state)
        j_respawn = is_respawn(j_state)
        j_state_changed = j_state != prev_j_state

        opp_damaged = is_damaged(opp_state)
        opp_grabbed = is_grabbed(opp_state)
        opp_damage_taken = damage_taken(prev_frame.ports[opp_port].leader.post, opp_data)
        opp_dead = is_dead(opp_state)
        opp_attacking = is_attacking(opp_state)
        opp_grabbing = is_grabbing(opp_state)
        opp_holding = is_holding(opp_state)
        opp_in_control = is_in_control(opp_state)
        opp_respawn = is_respawn(opp_state)
        opp_state_changed = opp_state != prev_opp_state

        if opp_respawn:
            kill_registerable = True

        # Opponent got hit or grabbed
        if opp_damaged or opp_grabbed:

            opp_time_since_hit = 0
            j_attack = j_data.last_attack_landed
            #print(j_attack)
            if (str(j_attack) == "Attack.OTHER" or str(j_attack) == "87"):
                j_pos = opp_data.position
            else:
                j_pos = j_data.position

            # If we're in neutral, jiggs landed the first hit
            if neutral:
                neutral = False

            # Add the attack to the current combo if it's fresh
            if opp_damage_taken:
                current_combo.append((j_attack, j_pos))

        # If opponent didn't get hit, increment time since the last hit landed
        else:
            opp_time_since_hit = opp_time_since_hit + 1

        # If it's been long enough without a hit, return to neutral
        if opp_time_since_hit > DISENGAGE:

            neutral = True

            # Reset the combo
            if current_combo:
                conversions.append(current_combo)
                current_combo = list()

        # If the opponent died, credit the death to jiggs' last combo
        if opp_dead and kill_registerable:

            # Reset the combo
            if current_combo:
                conversions.append(current_combo)
                current_combo = list()

            conversions.append("KILL")
            kill_registerable = False


        prev_frame = frame
        prev_j_state = j_state
        prev_opp_state = opp_state

    return conversions

def graphNeutralWins(character):
    neutral_wins = {
    fod[1]: list(),
    stadium[1]: list(),
    yoshis[1]:list(),
    dreamland[1]: list(),
    bf[1]: list(),
    fd[1]: list()}

    kills = {
    stadium[1]: list(),
    yoshis[1]: list(),
    dreamland[1]: list(),
    bf[1]: list(),
    fd[1]: list()}

    for index, row in all_games.iterrows():
        game = Game('games/' + row.filename)
        if character == 'puff':
            conversions = getNeutralWins(game, row.puff_port, row.peach_port)
        elif character == 'peach':
            conversions = getNeutralWins(game, row.peach_port, row.puff_port)
        for i in range(len(conversions)):

            combo = conversions[i]
            if isinstance(combo, str):

            # If the very first opponent death was a self-destruct without taking any hits, do nothing
                if i == 0:
                    continue

            # Otherwise, credit the last move hit with the kill
                kills[row.stage].append(conversions[i - 1][-1])

            else:
                neutral_wins[row.stage].append(combo[0])

    for stage, stage_name, fname in all_stages:

        neutral_x_pos = [w[1].x for w in neutral_wins[stage_name]]
        neutral_y_pos = [w[1].y for w in neutral_wins[stage_name]]
        neutral_win_move = [str(w[0]) for w in neutral_wins[stage_name]]
        count = 0
        for w in neutral_win_move:
            w = str(w)
            if ((w == '87') or (w == 'OTHER') or (w=='Attack.OTHER') or (w == 'Attack.87')):
                neutral_win_move[count] = "Turnip"
            else:
                id, move = neutral_win_move[count].split('.')
                neutral_win_move[count] = move
            count += 1

    # Plot neutral wins
        ax = sns.scatterplot(neutral_x_pos, neutral_y_pos, hue = neutral_win_move, palette = "deep", legend = "full")

        fig = plt.gcf()
        fig.set_size_inches(15, 15)

        x_left, x_right = stage_boundaries[stage_name][0]
        y_bottom, y_top = stage_boundaries[stage_name][1]

        plt.xlim(x_left, x_right)
        plt.ylim(y_bottom, y_top)
        plt.axis('off')

        map_img = mpimg.imread('stages/' + fname)

        im2 = ax.imshow(map_img, aspect = ax.get_aspect(), extent = ax.get_xlim() + ax.get_ylim(), zorder = 0)
        plt.show()
    return

def validGame(game):
    try:
        game = Game('games/' + fname)
        return game
    except KeyboardInterrupt:
        sys.exit()
    except:
        print('Game ' + fname + ' contains corrupt data.')
        return None

#variable definitions

puff = (slippi.id.InGameCharacter.JIGGLYPUFF, 'jigglypuff')
peach = (slippi.id.InGameCharacter.PEACH, 'peach')
fod = (slippi.id.Stage.FOUNTAIN_OF_DREAMS, 'fountain of dreams', 'fod.png')
stadium = (slippi.id.Stage.POKEMON_STADIUM, 'pokemon stadium', 'stadium.png')
yoshis = (slippi.id.Stage.YOSHIS_STORY, 'yoshi\'s story', 'yoshis.png')
dreamland = (slippi.id.Stage.DREAM_LAND_N64, 'dreamland', 'dreamland.png')
bf = (slippi.id.Stage.BATTLEFIELD, 'battlefield', 'bf.png')
fd = (slippi.id.Stage.FINAL_DESTINATION, 'final destination', 'fd.png')

all_stages = [fod, stadium, yoshis, dreamland, bf, fd]

stage_boundaries = {
    fod[1]: ((-198.75, 198.75), (-146.25, 202.5)),  # FOD
    stadium[1]: ((-230, 230), (-111, 180)),         # Stadium
    yoshis[1]: ((-175.7, 173.6), (-91, 168)),       # Yoshi's story
    dreamland[1]: ((-255.00, 255.00), (-123, 250)), # Dreamland
    bf[1]: ((-224, 224), (-108.8, 200)),            # BF
    fd[1]: ((-246.00, 246), (-140, 188))}                # FD

all_games = pd.DataFrame(columns = ['puff_port',
                                    'peach_port',
                                    'stage',
                                    'duration',
                                    'filename'])

# define filepath to games and images
print('This program will read Peach vs. Puff .slp Files.')
print('type "-h" for help')
zip_folder = input('Enter folder path to the .slp files: ')
if zip_folder == '-h':

    print('This is a script for converting .slp replay files',
          'into several visualizations. Read more about',
          'the .slp format at:')

    print('www.slippi.gg')
    zip_folder = input('Enter folder path to the'
                       '.slp files you wish to analyze: ')

#load games into dataframe from files
for fname in os.listdir(zip_folder):
    game = validGame(fname)
    frame1 = game.frames[1]
    ports = frame1.ports
    characters = list()
    for port_num in range(4):
        if ports[port_num]:
            char = ports[port_num].leader.post.character
            characters.append((port_num, char))

        if characters[0][1] != puff[0]:
            characters.reverse()

    add_game(game,characters,fname)

print(all_games.head())

char1 = 'puff'
char2 = 'peach'

puff_position = graphPositionPoints(char1)

peach_position = graphPositionPoints(char2)

puff_neutral = graphNeutralWins(char1)

peach_neutral = graphNeutralWins(char2)
