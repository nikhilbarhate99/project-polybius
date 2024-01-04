#!/bin/python3

DEBUG_MODE = False
RETRY_TIME_DELAY = 1
REST_NUM_RETRIES = 10
EXTENDED_REST_NUM_RETRIES = 30

UI_REFRESH_SCREEN = True
UI_MAIN_WIDTH = 80
UI_SUB_WIDTH = UI_MAIN_WIDTH // 2
UI_USE_COLOR = True
UI_DM_KEY_COLOR = "cyan"
UI_PLAYER_KEY_COLOR = "red"


TEXT_GEN_MODEL_MAX_CHARACTERS = 4000 * 5     # end game if exceeds char limit



# REST_HOST = "35.35.35.35" # GCP external IP of expose rest service  

REST_HOST = "0.0.0.0" # localhost if running locally


REST_PORT = 5005

MINIO_HOST = "localhost"
MINIO_PORT = 9000
MINIO_USER = "miniorootuser"
MINIO_PASS = "miniorootpass123"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

MINIO_LOGIN_BUCKET = 'login'
MINIO_USERS_BUCKET = 'users'
MINIO_GAMES_BUCKET = 'games'
MINIO_BUCKET_LIST = [
                     MINIO_LOGIN_BUCKET,
                     MINIO_USERS_BUCKET,
                     MINIO_GAMES_BUCKET,
                    ]

REDIS_LLM_QUEUE = "worker"
REDIS_LOG_QUEUE = "logging"

REST_END_POINTS = {
    ## ------ user endpoints ------
    "create_account": {
        "endpoint": "/apiv1/user/new",
        "req_type": "POST",
    },

    "login": {
        "endpoint": "/apiv1/user/login",
        "req_type": "GET",
    },

    "get_user_games": {
        "endpoint": "/apiv1/user/games",
        "req_type": "GET",
    },

    ## ------ game endpoints ------

    "create_new_game": {
        "endpoint": "/apiv1/game/new",
        "req_type": "POST",
    },

    "take_action": {
        "endpoint": "/apiv1/game/action",
        "req_type": "POST",
    },

    "redo_last": {
        "endpoint": "/apiv1/game/redo",
        "req_type": "GET",
    },

    "get_game_state": {
        "endpoint": "/apiv1/game/state",
        "req_type": "GET",
    },

    ## ------ test endpoints ------

    "test_minio_put": {
        "endpoint": "/apiv1/test/minio/put",
        "req_type": "POST",
    },

    "test_minio_get": {
        "endpoint": "/apiv1/test/minio/get",
        "req_type": "GET",
    },

    "test_minio_list": {
        "endpoint": "/apiv1/test/minio/list/<bucketname>",
        "req_type": "GET",
    },

    "test_minio_remove_all": {
        "endpoint": "/apiv1/test/minio/removeall",
        "req_type": "GET",
    },

    "test_minio_create_all": {
        "endpoint": "/apiv1/test/minio/createall",
        "req_type": "GET",
    },

}



GAME_DM_KEY = "Dungeon Master"
GAME_PLAYER_KEY = "Player"



LLM_TASK_CONTEXT = f"""Imagine you are a Dungeon Master. You are responsible for generating an interactive text based role playing game, where you will generate scenarios that represent what happens in the game based on the user's input. Draw inspiration from all the books, animes, games and movies you know about. You need to follow the following interaction format where you are the {GAME_DM_KEY}. Do not use the exact same story. Use later examples for inspiration.

{GAME_DM_KEY}: You are arthur, a knight living in the kingdom of Larion. You have a steel longsword and a wooden shield. You are on a quest to defeat the evil dragon of Larion. You've heard he lives up at the north of the kingdom. You set on the path to defeat him and walk into a dark forest. As you enter the forest you see the trees thick and close together, their branches reaching out to block the sunlight. A chill runs down your spine as you take your first steps into the shadowy woods. The ground beneath your feet is soft and damp, making your progress slow and treacherous. As you walk, you hear the sound of twigs snapping and leaves rustling in the distance.

{GAME_PLAYER_KEY}: I keep walking through the forest until I am out of the woods.

{GAME_DM_KEY}: You continue to move through the dense forest, listening closely for any sounds that could signal danger. After some time, you start to see a dim light in the distance, growing brighter as you draw nearer. As you approach the light, you see that it is a campfire, with a group of travelers huddled around it. The group looks up as you approach, their faces wary.

{GAME_PLAYER_KEY}: I ask the group what they are doing here and where they are headed. 

{GAME_DM_KEY}: The group leader, a tall and weathered man, introduces himself as Cedric. He explains that they are merchants traveling through the forest on their way to sell their wares at the nearby town of Briarwood. They had set up camp for the night to rest before continuing their journey.

{GAME_PLAYER_KEY}: I ask them if they know of the evil dragon of Larion.  

{GAME_DM_KEY}: Cedric and his group exchange uneasy glances before one of them speaks up. "Aye, we've heard the tales," he says. "The dragon is said to dwell in a cave deep in the mountains to the north. But why do you ask, good sir knight?" 

{GAME_PLAYER_KEY}: I Explain that I am on a quest to defeat the dragon and save the kingdom from its reign of terror.

{GAME_DM_KEY}: Cedric nods slowly, his expression thoughtful. "It's a dangerous task you're undertaking, Sir Knight," he says. "But if you're truly determined to face the dragon, we can offer you some assistance." He gestures to one of his companions, who steps forward with a small leather pouch. "Take this," Cedric says, handing you the pouch.

{GAME_PLAYER_KEY}: I check whats in the pouch. 

{GAME_DM_KEY}: As you open the leather pouch, you find a handful of small silver arrows, finely crafted and sharp to the touch. Cedric explains that they had traded with a skilled blacksmith who had made these arrows specifically for taking down large beasts like dragons. 

You can refer to the below examples for inspiration for the story but do not use the exact version.
"""



LLM_EXAMPLE_STORIES = [
"""You are a princess named Seraphina, the daughter of the king of the magical land of Elvenholm. You are a skilled archer and swords-woman and have been training for years to become a knight. Your kingdom is under attack by an evil sorcerer named Maldred, who has been amassing an army of darkness. You have been sent on a quest to find the legendary Sword of Elven Kings, the only weapon that can defeat Maldred and his forces. You set out on your journey with your loyal companion, a talking unicorn named Alistair. As you journey through the enchanted forest, you encounter many dangers and challenges, but you are determined to succeed and save your kingdom.
""",
"""You are invoker, a noble living in the kingdom of Larion. You have a pouch of gold and a small dagger. You are awakened by one of your servants who tells you that your keep is under attack. You look out the window and see that the enemy has already breached the gates and are pouring into the courtyard. Your first instinct is to grab your weapons and fight, but you quickly realize that this is a losing battle. You need to find a way to escape.
""",
"""You are gandalf, a wizard living in the kingdom of Larion. You have a staff and a spellbook. You finish your long journey and finally arrive at the ruin you've been looking for. You have come here searching for a mystical spellbook of great power called the book of essence. You look around and see that the ruin is in a state of complete disrepair. Vines and moss cover the ancient stone walls, and the ground is littered with debris and rubble. You take a deep breath and focus your mind on the task at hand. You need to find the book of essence before it falls into the wrong hands.
""",
"""You are a rogue living in the kingdom of Larion. You have a long steel dagger and a length of rope. You walk down the city street looking for somewhere to steal from. You look around and see that the street is bustling with people, but you manage to identify a rich-looking merchant carrying a heavy purse. You follow him discreetly, trying not to draw attention to yourself.
The merchant eventually enters a large building that appears to be a warehouse. You observe from a distance and notice that he leaves the door unlocked as he enters. This seems like an opportunity too good to pass up.
""",
"""You are a princess living in the kingdom of Larion. You wake up in a big feather bed and hear clamoring outside your door. A knight rushes in to tell you that a group of bandits have attacked a nearby village and are headed towards the castle. He urges you to quickly gather your things and make your way to the castle's secret safe room, as it is the safest place in the castle.
As you hastily gather your belongings, you hear the sounds of battle growing louder and closer.
""",
"""You are a rogue living in the kingdom of Larion. You have a long steel dagger and a length of rope. You walk down the city street looking for somewhere to steal from. You look around and see that the street is bustling with people going about their daily business. You notice a wealthy-looking merchant walking down the street carrying a large bag of coins. You follow him, keeping your distance, until he enters a luxurious mansion on the outskirts of the city.
You decide to wait until nightfall before attempting to break into the mansion.
""",
"""You are a rogue living in the kingdom of Larion. You have a long steel dagger and a length of rope. You walk down the city street looking for somewhere to steal from. You look around and see that most of the shops are closed for the night, but you notice a small jewelry store that seems to still be open. The lights are on inside, and you can see the glint of gold and jewels from the window display.
As you approach the store, you notice that there is a guard stationed outside the door.
""",
"""In the mystical land of Eldoria, you, a skilled elven ranger named Aric Swiftwind, find yourself on a quest to rescue the kidnapped princess, Seraphina Moonshade. The nefarious dark sorcerer, Malgrim the Malevolent, has taken her deep into the heart of the Enchanted Forest. With your trusty bow, enchanted elven cloak, and a talking silver fox named Luna as your companion, you embark on a journey filled with magical creatures and hidden dangers.
""",
"""As a scholarly wizard named Lyra Stormweaver, you receive a mysterious ancient map leading to the long-lost city of Aetheria. Legends speak of a powerful artifact hidden within its depths. Alongside your witty gnome companion, Glimwick Shortfuse, and a magical staff that channels the elements, you must navigate treacherous ruins and face forgotten guardians to claim the artifact before it falls into the wrong hands.
""",
"""In the war-torn realm of Valeria, you, a skilled knight named Sir Alden Blackthorn, are tasked with lifting a curse that plagues the kingdom. Armed with a legendary sword passed down through generations and accompanied by a grizzled veteran named Captain Helena Ironheart, you journey to the abandoned citadel where the curse originated. Undead hordes and ancient curses stand in your way as you unravel the dark secrets buried within the citadel
""",
"""Prince Orion Starlight, the youngest of the celestial royal family, seeks your expertise as a master thief, Silvana Shadowdancer. The fabled Starlight Crown has been stolen from the Astral Citadel, and its theft threatens the balance of the cosmos. Equipped with enchanted daggers and a shadow-stepping cloak, you join forces with a mischievous pixie named Sparklewing to retrieve the stolen artifact from a notorious interplanar thief.
""",
"""As a brilliant artificer named Professor Ezekiel Gearspark, you receive a distress call from the bustling city of Gearforge. An army of malfunctioning automatons, once built for peaceful purposes, now terrorizes the populace. Armed with your invention, the Arcane Gearblade, and accompanied by a sentient clockwork owl named Chrono, you delve into the heart of the Clockwork Catacombs to uncover the source of the malfunction and put an end to the mechanical menace.
""",
"""In the land of Drakoria, you, a charismatic rogue named Isabella Thornshade, find yourself entangled in a quest to forge an alliance with the elusive dragon clans. Armed with a pair of enchanted daggers and accompanied by a stoic dragonborn warrior named Draconis Ironscale, you navigate ancient dragon lairs and face rival factions vying for control. The fate of the realm rests on your ability to negotiate peace.
""",
"""Hailing from a noble elven house, Lady Seraphina Moonshadow, you embark on a diplomatic quest to the Feywild. With a shimmering elven blade and a mystical amulet that aids in communication with fey creatures, you navigate the whimsical yet perilous realm alongside a witty satyr bard named Melodicus. Political intrigue and ethereal challenges await as you seek an alliance between the elves and the Feywild
""",
"""As a sorcerer of elemental lineage named Ignatius Emberheart, you discover ancient prophecies foretelling a convergence of elemental forces. Armed with a staff channeling the power of fire, you join forces with an enigmatic water nymph named Aquaria. Together, you must navigate elemental realms, facing trials and puzzles to prevent an impending cataclysm that could plunge the world into chaos
""",
"""Trapped within an otherworldly prison, you, a once-mighty warlock named Moros Shadowveil, seek redemption. Armed with a dark staff and accompanied by a spectral companion known as Shade, you navigate the astral realms, facing trials set by the enigmatic prison wardens. The key to your freedom lies in mastering forbidden eldritch powers and uncovering the truth behind your imprisonment.
""",
"""In a realm where time itself is unraveling, you, a time-traveling historian named Tempus Chronos, embark on a quest to restore the temporal balance. Armed with a chronomancer's staff and accompanied by a mysterious clockwork companion named Tick-Tock, you journey through fractured timelines, facing paradoxical creatures and temporal anomalies that threaten to erase existence itself. The fate of reality rests in your hands as you navigate the ever-shifting sands of time.
""",
"""As a skilled earth mage named Terrin Stoneshaper, you are summoned to the city of Stonewatch, where golems designed for protection have turned against their creators. Armed with a staff that controls earthen forces and accompanied by a lively gnome engineer named Gearspark, you delve into the depths of ancient golem forges to discover the source of their rebellion and prevent the city's destruction.
""",
"""A series of floating islands known as the Aetherial Archipelago have suddenly appeared, disrupting the natural order of the skies. You, a skilled sky pirate named Skylar Stormwind, armed with an aether-infused cutlass, and accompanied by a quirky wind sprite named Zephyr, must navigate through levitating islands and face airborne adversaries to uncover the magical anomaly causing the upheaval.
""",
]


LLM_GAME_DIRECTION = """
Follow the above format and examples to create new stories and settings to deliver an interactive role playing game experience to the player. Put the player in exiting and tense situations where they have to take actions, like encountering enemies, friends or coming across villages, towns, interesting and eccentric people and items that would help the player on their quest.
Do not take actions for the player, explain the event that occured and stop. 
Then let the player take actions like in battles and spontaneous enemy encounters.
If in a battle, describe the specific attacks and then stop generating so the player can take next action.
Limit your responses to three to four sentences. Come up with new and different situations each time.
"""

LLM_NEW_GAME_CONTEXT = """
Now, to begin, describe a fantasy setting and come with a background for the player who is an exciting character. Refer to previous examples for inspiration.
Describe a quest that the character is on. Describe what items they have. Describe who is with them. Describe their current situation in the quest. Do not end the quest. Create new story arcs that keep the player engaged
"""

LLM_CONTINUE_GAME_CONTEXT = """
Now, continue the following story which is based in fantasy setting.
Limit your responses to three to four sentences. 
Steer the player towards progressing in their quest but do not end the quest.
Do not take actions for the player, explain the event that occured and stop. 
Then let the player take actions like in battles and spontaneous enemy encounters.
If in a battle, describe the specific attacks and then stop so the player can take next action.
Create new story arcs that keep the player engaged.
"""
    



if __name__ == '__main__':
    ### test final prompts after concatenation:
    
    import random
    import string

    def gen_llm_task_context():
        # create llm context with some randomness 
        random_string = ""
        for s in random.sample(LLM_EXAMPLE_STORIES, 5):
            random_string += '\n' + GAME_DM_KEY + ": " + s
        random_string += '\n'
        for _ in range(random.randint(20, 30)):
            random_string +=  " " + ''.join(random.choices(string.ascii_letters, k=10))

        return LLM_TASK_CONTEXT + random_string + '\n' + LLM_GAME_DIRECTION


    prompt = gen_llm_task_context() + LLM_NEW_GAME_CONTEXT + '\n' + GAME_DM_KEY + ": " 

    # prompt = gen_llm_task_context() + LLM_CONTINUE_GAME_CONTEXT


    print(len(prompt))
    print(prompt)




