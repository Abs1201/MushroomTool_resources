"""A collection of all commands that Shadower can use to interact with the game. 	"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up


# List of key mappings
class Key:
    # Movement
    JUMP = 'a' 
    SHADOW_LEAP = 'd' 
    ROPE_LIFT = 'shift' 

    # Buffs
    MAPLE_WARRIOR = 'f1' 
    DECENT_HOLY_SYMBOL = 'f2'
    DECENT_SHARP_EYE = '.'
    SHADOW_PARTNER = 'f6' 
    # SPEED_INFUSION = '8'
    DECENT_COMBAT_ORDERS = 'f3'
    DECENT_ADVANCED_BLESSING = 'f4'

    EPIC_ADVENTURE = '1'

    # Skills
    SHOWDOWN = 'f' 
    QUAD_STAR = 'g' 
    DARKLORDS_OMEN = 'w' 
    DEATH_STAR = 'e' 
    SUDDEN_RAID = 'r'
    DARK_FLARE = 'v' 
   
    ERDA_SHOWER = 't'


#########################
#       Commands        #
#########################
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    """

    num_presses = 2
    if direction == 'up' or direction == 'down':
        num_presses = 1
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.JUMP, 1)
        elif direction == 'up':
            press(Key.JUMP, 1)
    press(Key.JUMP, num_presses)


class Adjust(Command):
    """Fine-tunes player position using small movements."""

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)

    def main(self):
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        while config.enabled and counter > 0 and error > settings.adjust_tolerance:
            if toggle:
                d_x = self.target[0] - config.player_pos[0]
                threshold = settings.adjust_tolerance / math.sqrt(2)
                if abs(d_x) > threshold:
                    walk_counter = 0
                    if d_x < 0:
                        key_down('left')
                        while config.enabled and d_x < -1 * threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('left')
                    else:
                        key_down('right')
                        while config.enabled and d_x > threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('right')
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        press(Key.ROPE_LIFT, 1, down_time=0.01)
                        time.sleep(1.5)
                        # press(Key.LEAP_UP, 1)
                    else:
                        key_down('down')
                        time.sleep(0.05)
                        press(Key.JUMP, 1, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    if config.bot.rune_active:
                        time.sleep(1)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle



class Buff(Command):
    """Uses each of Shadowers's buffs once."""

    def __init__(self):
        super().__init__(locals())
        self.cd120_buff_time = 0
        self.cd180_buff_time = 0
        self.cd200_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0

    def main(self):
        buffs = [Key.DECENT_ADVANCED_BLESSING, Key.DECENT_HOLY_SYMBOL, Key.DECENT_COMBAT_ORDERS]
        now = time.time()

        if self.cd120_buff_time == 0 or now - self.cd120_buff_time > 120:
	        press(Key.EPIC_ADVENTURE, 3)
	        self.cd120_buff_time = now
        if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
	        press(Key.MAPLE_WARRIOR, 3)
	        self.cd900_buff_time = now
        if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
	        for key in buffs:
		        press(key, 3, up_time=0.3)
	        self.decent_buff_time = now		

			   
class Showdown(Command):
    """Attacks using 'Showdown' in a given direction."""

    def __init__(self, direction, attacks=2, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.attacks = int(attacks)
        self.repetitions = int(repetitions)

    def main(self):
        # time.sleep(0.05)
        key_down(self.direction)
        # time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.SHOWDOWN, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)
			
class DarkFlare(Command):
    """
    Uses 'DarkFlare' in a given direction, or towards the center of the map if
    no direction is specified.
    """

    def __init__(self, direction=None):
        super().__init__(locals())
        if direction is None:
            self.direction = direction
        else:
            self.direction = settings.validate_horizontal_arrows(direction)

    def main(self):
        if self.direction:
            press(self.direction, 1, down_time=0.1, up_time=0.05)
        else:
            if config.player_pos[0] > 0.5:
                press('left', 1, down_time=0.1, up_time=0.05)
            else:
                press('right', 1, down_time=0.1, up_time=0.05)
        press(Key.DARK_FLARE, 3)

class DarklordsOmen(Command):
    """
    Uses 'ShadowVeil' in a given direction, or towards the center of the map if
    no direction is specified.
    """

    def __init__(self, direction=None):
        super().__init__(locals())
        if direction is None:
            self.direction = direction
        else:
            self.direction = settings.validate_horizontal_arrows(direction)

    def main(self):
        if self.direction:
            press(self.direction, 1, down_time=0.1, up_time=0.05)
        else:
            if config.player_pos[0] > 0.5:
                press('left', 1, down_time=0.1, up_time=0.05)
            else:
                press('right', 1, down_time=0.1, up_time=0.05)
        press(Key.DARKLORDS_OMEN, 3)        		

class ErdaShower(Command):
    """
    Use ErdaShower in a given direction, Placing ErdaFountain if specified. Adds the player's position
    to the current Layout if necessary.
    """

    def __init__(self, jump='False'):
        super().__init__(locals())
        self.jump = settings.validate_boolean(jump)

    def main(self):
        num_presses = 3
        time.sleep(0.05)
        press(Key.ERDA_SHOWER, num_presses)
        if settings.record_layout:
	        config.layout.add(*config.player_pos)

class SuddenRaid(Command):
    """Uses 'SuddenRaid' once."""

    def main(self):
        press(Key.SUDDEN_RAID, 3)

class DeathStar(Command):
    """Uses 'SuddenRaid' once."""

    def main(self):
        press(Key.DEATH_STAR, 3)


