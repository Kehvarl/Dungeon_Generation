"""
Crafting.py
Inspired by: Craft3.pdf by John Arras
http://web.archive.org/web/20080211222642/http://www.cs.umd.edu/~jra/craft3.pdf

Intention: Implement a crafting system which can act as a suitable base for a procedurally-generated
 society.
"""


# Crafting is the act of producing an object from resources by use of a recipe
# A Crafting Recipe must define Location, Participants, Resources, Tools, Time, and Results
# Example Craft structure from article
# Craft
# {
#   int time;
#   string resource_names;
#   Craft_need *resource_list; // List of resources and quantities
#   int num_resources;
#   string skill_name;
#   int skill_level;
#   int percent_failure;
#   string item_created_amount; // Allow for random number of items made.
#   string item_created_name;
#   int item_created_id;
# };
# Craft_need
# {
#   int type;
#   int in_object;
#   int amount_needed;
#   int *acceptable_objects;
#   int num_acceptable_objects;
#   int damage_amount;
# }
#
# Sample Recipe: Wood (1 to 10 logs)
# Tree Here
# Axe Wield
# Wood_Log Produce [1,10]


# TODO: Define Crafting Primitives
class Craft:
    def __init__(self):
        self.time = 1
        self.needs = {}
        self.failure_percent = 10
        self.create_amount = 10
        self.create_id = 0
        raise NotImplementedError


class CraftNeeded:
    def __init__(self):
        self.type = 0
        self.in_object = 0
        self.amount = 0
        raise NotImplementedError
