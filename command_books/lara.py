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
    LEAP_UP = 'shift'
    ROPE_RIFT = '\''

    # Buffs
    ANIMA_WARRIOR = 'd'
    DECENT_SPEED_INFUSION = 'f'
    YAKISOBA = '-'
    PEERLESS_MOUNTAIN = '0'
    DRAGON_VEIN_READING = '9'
    MANA_OVERLOAD = '8'
    DECENT_HYPER_BODY = ';'
    DECENT_ADVANCED_BLESSING = 'g'

    # Skills
    ESSENCE_SPRINKLE = 'ctrl'
    DRAGON_VEIN_ERUPTION = 's'
    WINDING_MOUNTAIN_RIDGE = 'h'
    ERDA_SHOWER = 't'
    BIG_STRETCH = '4'
    TRUE_ARACHNID_REFLECTION = 'q'
    WAKEUP_CALL = 'w'
    UNCONSTRAINED_DRAGON_VEIN = 'insert'
    MENIFESTATION_WHERE_THE_RIVER_COURSES = 'delete'
    SURGING_ESSENCE = 'g'
    LARAS_CONNECTION = '5'
    


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
                        press(Key.ROPE_RIFT, 1, down_time=0.01)
                        time.sleep(0.5)
                        # press(Key.LEAP_UP, 1)
                    else:
                        key_down('down')
                        time.sleep(0.05)
                        press(Key.JUMP, 1, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    time.sleep(0.5)
                    if config.bot.rune_active:
                        time.sleep(1.5)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    """Uses each of Kanna's buffs once. Uses 'Haku Reborn' whenever it is available."""

    def __init__(self):
        super().__init__(locals())
        self.cd120_buff_time = 0
        self.cd180_buff_time = 0
        self.cd200_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0

    def main(self):
        buffs = [Key.DECENT_SPEED_INFUSION, Key.DECENT_ADVANCED_BLESSING]
        now = time.time()
        
        if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
	        press(Key.ANIMA_WARRIOR, 2)
	        self.cd900_buff_time = now
        if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
	        for key in buffs:
		        press(key, 3, up_time=0.3)
	        self.decent_buff_time = now		


class DragonVeinEruption(Command):
    """uses eruption once"""
    def main(self):
        press(Key.DRAGON_VEIN_ERUPTION, 3)

# class DragonVeinEruptionDirectional(Command):
#     """uses eruption with direction"""
#     def __init__(self, direction='up'):
#         super().__init__(locals())
#         self.direction = settings.validate_arrows(direction)
    
#     def main(self):
#         press(Key.DRAGON_VEIN_ERUPTION, 3)
        
class EssenceSprinkle(Command):
    """uses eruption once"""
    def main(self):
        press(Key.ESSENCE_SPRINKLE, 1, up_time=0.05)

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
        # if self.direction in ['up', 'down']:
        #     num_presses = 2
        # if self.direction != 'up':
        #     key_down(self.direction)
        #     time.sleep(0.05)
        # if self.jump:
        #     if self.direction == 'down':
        #         press(Key.JUMP, 3, down_time=0.1)
        #     else:
        #         press(Key.JUMP, 1)
        # if self.direction == 'up':
        #     key_down(self.direction)
        #     time.sleep(0.05)
        press(Key.ERDA_SHOWER, num_presses)
        # key_up(self.direction)
        if settings.record_layout:
	        config.layout.add(*config.player_pos)
         

class WindingMountainRidge(Command):
    """uses mountainRidge once"""
    def main(self):
        press(Key.WINDING_MOUNTAIN_RIDGE, 3)

class BigStretch(Command):
    """uses Big stretch once"""
    def main(self):
        press(Key.BIG_STRETCH, 3)
        
class TrueArachnidReflection(Command):
    """uses will skill once"""
    def main(self):
        press(Key.TRUE_ARACHNID_REFLECTION, 1, down_time=0.05)
        
class WakeUpCall(Command):
    """uses wakeUpCall once"""
    def main(self):
        press(Key.WAKEUP_CALL, 3)
        
    #     UNCONSTRAINED_DRAGON_VEIN = 'insert'
    # MENIFESTATION_WHERE_THE_RIVER_COURSES = 'delete'
    
class UnconstrainedDragonVein(Command):
    """Uses UnconstrainedDragonVein once"""
    def main(self):
        press(Key.UNCONSTRAINED_DRAGON_VEIN, 1)

class MenifestationWhereTheRiverCourses(Command):
    """set river course"""
    def main(self):
        press(Key.MENIFESTATION_WHERE_THE_RIVER_COURSES, 1)
        
class UpAndEruption(Command):
    def main(self):
        press('up',1)
        press(Key.DRAGON_VEIN_ERUPTION, randint(1,2))
        
class PressUp(Command):
    def main(self):
        press('up',1)
        time.sleep(random.uniform(0.2, 0.5))
        

class SurgingEssence(Command):
    def main(self):
        press(Key.SURGING_ESSENCE, 1)
        
class LeapUp(Command):
    def main(self):
        press(Key.LEAP_UP, 1)
       
class LarasConnection(Command):
    def main(self):
        press(Key.LARAS_CONNECTION, 1)

         
# class EruptionAndUp(Command):
#     def __init__(self, direction='up', jump='False', sleepTime=90.0):
#         super().__init__(locals())
#         self.direction = settings.validate_arrows(direction)
#         self.jump = settings.validate_boolean(jump)
#         self.sleepTime = float(sleepTime) + random.uniform(0, 0.5)
#         self.instream = False
        
#     def main(self):
#         num_presses = 2
#         if not self.instream:
#             self.instream=True
#             key_down(self.direction)
#             key_down(Key.DRAGON_VEIN_ERUPTION)
#             time.sleep(self.sleepTime)
#             key_up(self.direction)
#             key_up(Key.DRAGON_VEIN_ERUPTION)
        
