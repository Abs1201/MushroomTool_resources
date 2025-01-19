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

    # Buffs
    DECENT_HOLY_SYMBOL = 'f3'
    RITUAL_FAN_ACCELERATION = 'f4'
    DECENT_SHARP_EYE = 'f5'
    DECENT_SPEED_INFUSION = 'f6'

    

    # Skills
    FAN = 'f'
    GOLD_BANDED_CUDGEL = 'g' 
    STAR_VOLTEX = 'v' 
    STONE_TREMOR = 'r'
    TALIESMAN_CLONE = 'q'
    WARP_GATE = 'z'
    CONSUMING_FLAMES = 's'
    GHOST_FLAME = 'w'
    THOUSANDTON_STONE = 'd'
    IRONFAN = 'c'
    ERDA_SHOWER = 't'
    TIGER = '2'
    CLONE_RAMPAGE = '3'
    
    BUTTERFLY_DREAM = '1'
    WRATH_OF_GODS = 'page down'
    SAGE_TAIYU_MIRACLE_TONIC = 'h'
    TIGER = '2'
    
    REFLECTION = 'f1'
    SOLAR_CREST = 'f2'


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
        self.cd60_buff_time = 0 #ghostflame
        self.cd90_buff_time = 0
        self.cd100_buff_time = 0
        self.cd120_buff_time = 0
        self.cd180_buff_time = 0
        self.cd250_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0
        self.flag250 = True

    def main(self):
        buffs = [Key.DECENT_HOLY_SYMBOL]
        now = time.time()
        if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
            for key in buffs:
                press(key, 3, up_time=0.3)
            self.decent_buff_time = now
            
        if self.cd250_buff_time == 0 or now - self.cd250_buff_time > 250/2+4:
            if self.flag250:
                press(Key.SOLAR_CREST,2)
            else:
                press(Key.REFLECTION,2)
            self.cd250_buff_time = now
            self.flag250 = not self.flag250
        # if self.cd60_buff_time == 0 or now - self.cd60_buff_time > 60:
	    #     press(Key.GHOST_FLAME, 2)
	    #     self.cd60_buff_time = now
        # if self.cd100_buff_time == 0 or now - self.cd100_buff_time > 100:
	    #     press(Key.BUTTERFLY_DREAM, 2)
	    #     self.cd100_buff_time = now
        # if self.cd200_buff_time == 0 or now - self.cd200_buff_time > 200:
	    #     press(Key.RITUAL_FAN_ACCELERATION, 2)
	    #     self.cd200_buff_time = now
        # if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
	    #     press(Key.ANIMA_WARRIORS, 2)
	    #     self.cd900_buff_time = now
        # if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
	    #     for key in buffs:
		#         press(key, 3, up_time=0.3)
	    #     self.decent_buff_time = now		

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
			   
class Fan(Command):
    """Attacks using 'fan' in a given direction."""

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
            press(Key.FAN, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)
            
class GoldBandedCudgel(Command):
    """Attacks using 'GoldBandedCudgel' in a given direction."""

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
            press(Key.GOLD_BANDED_CUDGEL, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)
			
class StarVortex(Command):
    """
    Uses 'StarVortex' in a given direction, or towards the center of the map if
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
        press(Key.STAR_VOLTEX, 1)

class StoneTremor(Command):
    """Attacks using 'StoneTremor' in a given direction."""

    def __init__(self, direction='up'):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)

    def main(self):
        key_down(self.direction)
        time.sleep(0.05)
        press(Key.STONE_TREMOR, 2, up_time=0.05)
        time.sleep(0.05)
        key_up(self.direction)


class newWarpGate(Command):      
    def main(self):
        key_down('up')
        time.sleep(0.1)
        press(Key.WARP_GATE, 2)
        time.sleep(0.1)
        key_up('up')
        
class useWarpGate(Command):    
    def main(self):
        press(Key.WARP_GATE, 2)


class GhostFlame(Command):
    """Uses 'SuddenRaid' once."""

    def main(self):
        press(Key.GHOST_FLAME, 2)

class TalismanClone(Command):
    """Uses 'SuddenRaid' once."""

    def main(self):
        press(Key.TALIESMAN_CLONE, 2)
        
class ButterflyDream(Command):
    def main(self):
        press(Key.BUTTERFLY_DREAM, 2)
        
class WrathofGods(Command):
    def main(self):
        press(Key.WRATH_OF_GODS, 1)
        
class ConsumingFlames(Command):
    def main(self):
        press(Key.CONSUMING_FLAMES, 1)

class MiracleTonic(Command):
    def main(self):
        press(Key.SAGE_TAIYU_MIRACLE_TONIC,2)
        
class ThousandTonStone(Command):
    def main(self):
        press(Key.THOUSANDTON_STONE,1)

class IronFan(Command):
    def main(self):
        press(Key.IRONFAN,1)

