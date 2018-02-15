import leviathans_planets as lp
import leviathans_world as game

import logging
import random

if __name__ != "__main__":
    logging.debug("leviathans_anomaly imported")

GENERATION_CHANCE = 0.5

lp.blueprints["Assorted Data"] = "Unprocessed Data"

def generate_blueprint(world):
    logging.info('Generating a blueprint')
    
    item_adj = random.choice(lp.blueprint_adj)
    item = ('' if not item_adj else item_adj + ' ') + random.choice(world.mat.keys()) + ' ' + random.choice(lp.blueprint_types)
    item_blueprint = item + ' ' + random.choice(('Blueprint', 'Schematic', 'Template'))
    lp.blueprints[item] = item_blueprint
    logging.info('Player discovered %s', item_blueprint)
    return item

class Anomaly(object):
    def __init__(self):
        self.blu = None
        self.name = "black hole"

    def __repr__(self):
        if self.blu is None:
            return "<Undiscovered Anomaly>"
        else:
            return "<Anomaly: " + self.blu + ">"

    def __str__(self):
        return self.name

    def discover(self, world):
        if self.blu is None:
            self.blu = generate_blueprint(world)
            return world.blu[self.blu]
        else:
            return "Assorted Data"

@game.world_hook
def generate_anomalies(new, world):
    if new:
        logging.info('Generating anomalies')
    elif not hasattr(world, "ANOMALIES"):
        logging.info('Retroactively generating anomalies')
    else:
        logging.debug('Anomalies already generated in this world')

    world.ANOMALIES = True

    for system in world.systems.values():
        if random.random() <= GENERATION_CHANCE:
            system.anomaly = Anomaly()
        else:
            system.anomaly = None
            
def research(world, cmd, playerid):
    logging.info('Discovering anomaly')

    system = world.system_list[world.players[playerid].systemID]

    if system.anomaly is None:
        print "There is no anomaly to research here, Captain"
    else:
        print "Scanning anomaly, Captain."

        time.sleep(2)

        print
        print 'The following has been added to your cargo bay:'

        item = system.anomaly.discover()
        logging.info('Adding %s to player cargo bay', item)
        world.players[playerid].cargo.append(item)
        print item

game.new_cmd['research'] = game.new_cmd['discover'] = research