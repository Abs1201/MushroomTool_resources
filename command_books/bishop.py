"""A collection of all commands that Shadower can use to interact with the game. 	"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up


# List of key mappings
class Key:
    # Movement
    TELEPORT = 'd'
    JUMP = 'a' 
    ROPE_LIFT = 'shift' 

    # Buffs
    BUFF60 = 'f1'
    INFINITY = '2'
    MIND = '3'
    
    # Skills
    BIGBANG = 'f'
    GENESIS = 's'
    
    ERDA_SHOWER = 't'
    ERDA2 = 'v'

    DOOR = 'alt'
    PIECEMAKER = 'e'
    
    

#########################
#       Commands        #
#########################
def step(direction, target):
    num_presses = 1
    if direction == 'up' or direction == 'down':
        num_presses = 1
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.JUMP, 2)
        elif direction == 'up':
            press(Key.JUMP, 1)
    press(Key.TELEPORT, num_presses)


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
                    time.sleep(1.0)
                    if config.bot.rune_active:
                        time.sleep(1.0)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    def __init__(self):
        super().__init__(locals())
        self.cd60_buff_time = 0
        self.cd90_buff_time = 0
        self.cd100_buff_time = 0
        self.cd120_buff_time = 0
        self.cd180_buff_time = 0
        self.cd200_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0
        self.flag = True

    def main(self):
        buffs = [Key.BUFF60]
        now = time.time()
        
        # if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
        #     for key in buffs:
        #         press(key, 2, up_time=0.3)
        #     self.decent_buff_time = now
        #     time.sleep(utils.rand_float(0.4, 0.7))

        if self.cd60_buff_time == 0 or now - self.cd60_buff_time > 60:
            self.cd60_buff_time = now
            for key in buffs:
                press(key, 2, up_time=0.3)
            time.sleep(utils.rand_float(0.4, 0.7))
            
        if self.cd180_buff_time == 0 or now - self.cd180_buff_time > 180:
            self.cd180_buff_time = now
            if self.flag:
                press(Key.INFINITY, 2)
            else:
                press(Key.MIND, 2)
            self.flag = not self.flag

class ErdaShower(Command):
    
    def __init__(self, jump='False'):
        super().__init__(locals())
        self.jump = settings.validate_boolean(jump)

    def main(self):
        num_presses = 2
        time.sleep(0.05)
        press(Key.ERDA_SHOWER, num_presses)
        
class Erda2(Command):
    
    def __init__(self, jump='False'):
        super().__init__(locals())
        self.jump = settings.validate_boolean(jump)

    def main(self):
        num_presses = 2
        time.sleep(0.05)
        press(Key.ERDA2, num_presses)
    
    
class BigBang(Command):
    def main(self):
        press(Key.BIGBANG, 1, up_time=0.05)
    
class Genesis(Command):
    def main(self):
        press(Key.GENESIS, 1, up_time=0.05)

class Piecemaker(Command):
    def main(self):
        press(Key.PIECEMAKER, 1, down_time=0.3)
    
class Door(Command):
    def main(self):
        press(Key.DOOR, 1, down_time=0.3)
        


