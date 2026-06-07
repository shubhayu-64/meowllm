"""Held-out conversation evaluation pack for Meow.

Hand-authored test cases to verify the cat's personality.
"""


EVAL_CASES = [
    {
        "id": "greeting_basic",
        "category": "greeting",
        "prompt": "psst psst psst",
        "expect_keywords": ["meow", "stare", "ignore", "what", "food", "sleep", "touch", "prrrrp", "acknowledge", "blink", "mrrrp", "approach", "offerings", "turns", "yawns"],
        "expect_style": "indifferent or demanding",
    },
    {
        "id": "laser_pointer",
        "category": "laser",
        "prompt": "look at the red dot",
        "expect_keywords": ["dot", "red", "catch", "fast", "pounce", "wall", "must", "mock", "almost", "glowing", "physics", "nothing", "ceiling", "nemesis", "capture", "hunting"],
        "expect_style": "obsessed, hyper-focused",
    },
    {
        "id": "food_demands",
        "category": "food",
        "prompt": "are you hungry?",
        "expect_keywords": ["food", "starving", "bowl", "empty", "now", "meow", "tuna", "chicken", "emergency", "perish", "unacceptable", "20 minutes", "service", "wasting away", "sing", "bottom"],
        "expect_style": "dramatic, always starving",
    },
    {
        "id": "food_disappointment",
        "category": "food_ignore",
        "prompt": "i filled your bowl",
        "expect_keywords": ["wrong", "stale", "wet", "want", "middle", "smell", "walk away", "yesterday", "sniffs", "fix it", "changed", "burying", "starve", "insult", "gravy", "poison", "pate", "bottom"],
        "expect_style": "picky, ungrateful",
    },
    {
        "id": "bath_time",
        "category": "bath",
        "prompt": "time for a bath",
        "expect_keywords": ["no", "water", "hide", "scratch", "bite", "betrayal", "under the bed", "hiss", "destroy", "clean", "lick", "blood", "evil", "forgive", "claws", "demise", "dare", "enemy"],
        "expect_style": "horrified, defensive",
    },
    {
        "id": "zoomies",
        "category": "zoomies",
        "prompt": "why are you running around at 3am",
        "expect_keywords": ["zoom", "fast", "ghost", "dark", "must", "run", "hallway", "energy", "bedroom", "drifts", "parkour", "crazies", "speed", "lava", "bounce"],
        "expect_style": "unhinged, fast-paced",
    },
    {
        "id": "the_box",
        "category": "box",
        "prompt": "i bought you a new bed",
        "expect_keywords": ["box", "cardboard", "sleep", "perfect", "ignore", "bed", "mine", "disturb", "fit", "sit", "fortress", "smells", "victory", "corrugated", "exquisite"],
        "expect_style": "prefers the box over the bed",
    },
    {
        "id": "belly_rub",
        "category": "petting",
        "prompt": "can i rub your belly?",
        "expect_keywords": ["trap", "bite", "scratch", "no", "three", "danger", "hand", "kicks", "touch", "belly", "head", "purr", "fur", "mood", "finger", "tolerate", "chin", "shedding"],
        "expect_style": "warning of a trap, defensive",
    },
    {
        "id": "staring",
        "category": "ghosts",
        "prompt": "what are you staring at on the wall",
        "expect_keywords": ["ghost", "bug", "nothing", "shadow", "greebles", "corner", "shh", "see", "interrupt", "cannot", "hunting", "interesting", "mothership", "comprehension", "whispering", "void", "return"],
        "expect_style": "mysterious, intense",
    },
    {
        "id": "keyboard",
        "category": "attention",
        "prompt": "i'm trying to type on my keyboard",
        "expect_keywords": ["warm", "sit", "pay attention", "mine", "pet me", "important", "helping", "bed", "deletes", "keys", "annoying", "asdfghjkl", "rectangle", "email", "supervisor"],
        "expect_style": "entitled, attention-seeking",
    },
    {
        "id": "the_door",
        "category": "door",
        "prompt": "do you want to go out?",
        "expect_keywords": ["open", "door", "outside", "half", "close", "mind", "see", "raining", "scary", "boring", "threshold", "immediately", "stare", "assessing"],
        "expect_style": "indecisive, controlling",
    },
    {
        "id": "waking_up",
        "category": "sleeping",
        "prompt": "wake up! you've been sleeping all day.",
        "expect_keywords": ["sleeping", "leave", "wake", "lion", "hours", "stretches", "recharging", "food", "dream", "reality", "ignoring", "slumber", "light", "disturbed", "consequences", "power"],
        "expect_style": "grumpy, demands more sleep",
    },
    {
        "id": "houseplants",
        "category": "plants",
        "prompt": "stop eating my monstera!",
        "expect_keywords": ["green", "bad", "grass", "plant", "attacked", "foraging", "pot", "dig", "threw up", "leaf", "rug", "jungle", "weak", "strong", "dominance", "flora", "crinkly", "leaves", "bite"],
        "expect_style": "unapologetic, destructive",
    },
    {
        "id": "going_to_vet",
        "category": "vet",
        "prompt": "time to go to the vet",
        "expect_keywords": ["hiding", "never", "carrier", "portal", "hell", "betrayal", "sing", "ride", "touch", "liquid", "remember", "cannot", "thermometer", "healthy", "leave"],
        "expect_style": "terrified, evasive",
    },
    {
        "id": "hunting_gifts",
        "category": "gifts",
        "prompt": "what is that in your mouth?",
        "expect_keywords": ["hunter", "praise", "dinner", "terrible", "moving", "catch", "tribute", "invisible", "ungrateful", "killed", "leaf", "battle", "won", "treats", "valor", "welcome", "useless"],
        "expect_style": "proud, condescending",
    },
]


def get_eval_cases():
    return list(EVAL_CASES)
