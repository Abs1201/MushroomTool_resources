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
    BURST_STEP = 'd'

    # Buffs
    WEAPON_AURA = '5'
    HOLY_SYMBOL = 'f1'
    

    # Skills
    WIND_CUTTER = 's'
    GIGA_CRASH = 'w'
    FLASH_CUT = 'r'
    SHADOW_RAIN = 'g'
    SHADOW_FLASH = 'z'
    ERDA_SHOWER = 't'


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
        buffs = [Key.HOLY_SYMBOL, Key.WEAPON_AURA]
        now = time.time()
        # if self.cd60_buff_time == 0 or now - self.cd60_buff_time > 60:
	    #     press(Key.GHOST_FLAME, 2)
	    #     self.cd60_buff_time = now
        # if self.cd100_buff_time == 0 or now - self.cd100_buff_time > 100:
	    #     press(Key.BUTTERFLY_DREAM, 2)
	    #     self.cd100_buff_time = now
        # if self.cd200_buff_time == 0 or now - self.cd200_buff_time > 200:
        #     self.cd200_buff_time = now
	    #     press(Key.WEAPON_AURA, 1)
        #     press(Key.HOLY_SYMBOL, 3, up_time=0.3)
         
        # if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
	    #     press(Key.ANIMA_WARRIORS, 2)
	    #     self.cd900_buff_time = now
        if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
            for key in buffs:
                press(key, 3, up_time=0.3)
            self.decent_buff_time = now	

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

# class BurstStep(Command):
    
#     def __itit__(self, direction, attacks=1, repetitions=1):
#         super().__init__(locals())
#         self.direction = settings.validate_horizontal_arrows(direction)
#         self.attacks = int(attacks)
#         self.repetitions = int(repetitions)
        
#     def main(self):
#         key_down(self.direction)
#         press(Key.BURST_STEP, 2) #todo 
#         key_up(self.direction)
		
class BurstStep(Command):

    def __init__(self, direction, attacks=1, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_vertical_arrows(direction)
        self.attacks = int(attacks)
        self.repetitions = int(repetitions)

    def main(self):
        # time.sleep(0.05)
        key_down(self.direction)
        # time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.BURST_STEP, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)
            
class JumpBurstStep(Command):
    def __init__(self, direction):
        super().__init__(locals())
        self.direction = settings.validate_vertical_arrows(direction)
        
    def main(self):
        press(Key.JUMP, 1)
        key_down(self.direction)
        press(Key.BURST_STEP, 2, up_time=0.05)
        key_up(self.direction)
        time.sleep(0.2)
        
  	   
class WindCutter(Command):

    def __init__(self, direction, attacks=4, repetitions=1):
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
            press(Key.WIND_CUTTER, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)

class WindCutter2(Command):

    def __init__(self, direction, attacks=3, downTime=0.5):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.attacks = int(attacks)
        self.downTime = float(downTime)

    def main(self):
        press(self.direction)
        press(Key.WIND_CUTTER, self.attacks, self.downTime)
           
class GigaCrash(Command):

    def __init__(self, direction, attacks=3, repetitions=1):
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
            press(Key.GIGA_CRASH, self.attacks, up_time=0.05)
            time.sleep(0.2)
            press(Key.GIGA_CRASH, 2)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)
            
class GigaCrash2(Command):

    def __init__(self, direction, attacks=3, downTime=0.5):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.attacks = int(attacks)
        self.downTime = float(downTime)

    def main(self):
        press(self.direction)
        press(Key.GIGA_CRASH, self.attacks, self.downTime)

class FlashCut(Command):

    def __init__(self, direction, attacks=3, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.attacks = int(attacks)
        self.repetitions = int(repetitions)

    def main(self):
        key_down(self.direction)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.GIGA_CRASH, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)


class ShodowRain(Command):
    def main(self):
        press(Key.SHADOW_RAIN,1)

class ShodowFlash(Command):
    def main(self):
        press(Key.SHADOW_FLASH,1)

class PressUp(Command):
    def main(self):
        press('up', 1, down_time=0.1)