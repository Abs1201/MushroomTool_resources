"""A collection of all commands that a Kanna can use to interact with the game."""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up
import random
from random import randint


# List of key mappings
class Key:
    # Movement
    JUMP = 'a'
    ROPE_LIFT = 'shift'

    # Buffs
    SYMBOL = 'f2'
    ROLL_OF_THE_DICE = 'f1'
    TERMS_CONDITIONS='1'
    MASCOT='5'
    EXALTATION='4'

    # Skills
    CELESTIAL_ROAR = 'f'
    FINALE_RIBBON = 'r'
    ERDA_SHOWER = 't'
    ROPE_LIFT = 'z'
    SUPERNOVA = 'w'
    PINK_PUMMEL='d'
    SOUL_SEEKER='s'
    SPOTLIGHT='c'
    SPARKLE_BURST='q'
    REFLECTION = 'v'
    
    
    


#########################
#       Commands        #
#########################
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by MushroomTool.
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
                        time.sleep(0.5)
                        # press(Key.LEAP_UP, 1)
                    else:
                        key_down('down')
                        time.sleep(0.05)
                        press(Key.JUMP, 1, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    time.sleep(0.75)
                    if config.bot.rune_active:
                        time.sleep(1.5)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    """Uses each of Kanna's buffs once. Uses 'Haku Reborn' whenever it is available."""

    def __init__(self):
        super().__init__(locals())
        self.cd60_buff_time=0
        self.cd120_buff_time = 0
        self.cd180_buff_time = 0
        self.cd200_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0

    def main(self):
        buffs = [Key.ROLL_OF_THE_DICE, Key.SYMBOL]
        now = time.time()
        if self.cd60_buff_time==0 or now-self.cd60_buff_time>60:
            press(Key.TERMS_CONDITIONS, 2)
            press(Key.EXALTATION, 2)
            press(Key.MASCOT,2)
            self.cd60_buff_time=now
        if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
            for key in buffs:
                press(key, 3, up_time=0.3)
            self.decent_buff_time = now


class CelestialRoar(Command):
    def main(self):
        press(Key.CELESTIAL_ROAR, 2)
        
class SoulSeeker(Command):
    def __init__(self, use_random='false', min=1, max=3):
        super().__init__(locals())
        self.use_random = settings.validate_boolean(use_random)
        self.min = int(min)
        self.max = int(max)
    
    def main(self):
        if self.use_random:
            tmp = randint(self.min, self.max)
            for _ in range(tmp):
                press(Key.SOUL_SEEKER, 1, up_time=0.05)
                time.sleep(utils.rand_float(0.02, 0.05))
        else:
            press(Key.SOUL_SEEKER, 1)
class PinkPummel(Command):
    def main(self):
        press(Key.PINK_PUMMEL, 1)
        
class FinaleRibbon(Command):
    def main(self):
        press(Key.FINALE_RIBBON, 2)
        
class Supernova(Command):
    def main(self):
        press(Key.SUPERNOVA, 2)    

class ErdaShower(Command):
    """
    Use ErdaShower in a given direction, Placing ErdaFountain if specified. Adds the player's position
    to the current Layout if necessary.
    """

    def __init__(self, jump='False'):
        super().__init__(locals())
        #self.direction = settings.validate_arrows(direction)
        self.jump = settings.validate_boolean(jump)

    def main(self):
        num_presses = 3
        time.sleep(0.05)
        press(Key.ERDA_SHOWER, num_presses)
        if settings.record_layout:
	        config.layout.add(*config.player_pos)
         
class Spotlight(Command):
    def main(self):
        press(Key.SPOTLIGHT, 2)
        
class SparkleBurst(Command):
    def main(self):
        press(Key.SPARKLE_BURST, 2)
        
class Reflection(Command):
    def main(self):
        press(Key.REFLECTION, 2)