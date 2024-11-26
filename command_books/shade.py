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
    ROPE_LIFT = 'shift' 
    FOX_TROT = 'd'
    BACK_STEP = 's'

    # Buffs
    DICE = 'f1'
    HOLY_SYMBOL = 'f2'
    HEROIC_MEMORIES = '1'
    

    # Skills
    BOMB_PUNCH = 'f'
    SPIRIT_CLAW = 'g'
    
    ERDA_SHOWER = 't'
    SPIRIT_FRENZY = 'r'

    FOX_GOD_FLASH = '2'
    FOX_MARBLE_FUSION = '3'
    SPIRIT_GATE = 'v'
    
    

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
        # cloud = False
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
                        # cloud = True
                        # if cloud==False:
                        #     key_down('up')
                        #     press(Key.JUMP, 1, down_time=0.1)
                        #     key_down(Key.JUMP)
                        # else:
                        #     time.sleep(0.2)
                    else:
                        # if cloud==True:
                        #     cloud=False
                        #     key_up(Key.JUMP)
                        #     key_up('up')
                        key_down('down')
                        time.sleep(0.05)
                        press(Key.JUMP, 1, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    time.sleep(0.9)
                    if config.bot.rune_active:
                        time.sleep(1)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    """Uses each of Shadowers's buffs once."""

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

    def main(self):
        buffs = [Key.HOLY_SYMBOL, Key.DICE]
        now = time.time()

        if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
            for key in buffs:
                press(key, 2, up_time=0.3)
            self.decent_buff_time = now

        if self.decent_buff_time == 0 or now - self.decent_buff_time > 120:
            self.cd120_buff_time = now
            press(Key.HEROIC_MEMORIES, 2, up_time=0.3)

class ErdaShower(Command):
    
    def __init__(self, jump='False'):
        super().__init__(locals())
        self.jump = settings.validate_boolean(jump)

    def main(self):
        num_presses = 2
        time.sleep(0.05)
        press(Key.ERDA_SHOWER, num_presses)
        if settings.record_layout:
	        config.layout.add(*config.player_pos)
    
class SpirityFrenzy(Command):
    def main(self):
        press(Key.SPIRIT_FRENZY)
        
class FoxGodFlash(Command):
    def main(self):
        press(Key.FOX_GOD_FLASH, 1, down_time= 0.3)
        
class FoxMarbleFusion(Command):
    def main(self):
        press(Key.FOX_MARBLE_FUSION, 1, down_time=0.3)
        
    
class BombPunch_nodir(Command):
    def main(self):
        press(Key.BOMB_PUNCH)
        
class BombPunch(Command):
    def __init__(self, direction, attacks=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.attacks = int(attacks)

    def main(self):
        key_down(self.direction)
        key_up(self.direction)
        press(Key.BOMB_PUNCH, self.attacks)
        time.sleep(0.2)
  	   
class SpiritClaw(Command):
    def main(self):
        press(Key.SPIRIT_CLAW, 2)
           

class SpiritGate(Command):
    def main(self):
        press(Key.SPIRIT_GATE, 2) 
        


