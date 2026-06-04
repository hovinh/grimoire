import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
import utils.db as db

db.init_db()

game = {
    "id": "lunar_creamery",
    "title": "Lunar Creamery",
    "weight": "medium",
    "bgg_weight": 2.1,
    "min_players": 2,
    "max_players": 5,
    "play_time": "~46 min",
    "image_url": "https://placehold.co/400x280/1a0a3b/f7c948?text=Lunar+Creamery",
    "image_path": "data/images/lunar-creamery.jpg",
    "mechanics": [
        "hand management",
        "set collection",
        "engine building",
        "turn order rotation",
    ],
    "description": (
        "You are a Moon Rabbit working at the one and only ice cream shop on the Moon! "
        "Space travelers from all over the galaxy — astronauts, aliens, and royalty — "
        "visit the Lunar Café craving delicious scoops. Collect ingredients, craft the "
        "perfect flavors, and serve customers fast before rivals scoop them up."
    ),
    "theme": (
        "The Lunar Café is the only ice cream shop on the Moon — and every space traveler "
        "in the galaxy wants a scoop! Astronauts, aliens, and moon royalty all line up at "
        "your door, each craving a different flavor. As a Moon Rabbit scooper, you collect "
        "ingredients, craft ice cream, and race to serve customers before your rivals do. "
        "Every satisfied customer earns you Lunar Points, and when the café closes after "
        "six rounds, the Moon Rabbit with the most LP wins the title of Star Bunny — the "
        "greatest scooper the Moon has ever seen!"
    ),
    "objective": (
        "Collect the most Lunar Points (LP) by crafting and serving ice cream that matches "
        "what each customer wants. The player with the most LP at the end becomes the Star "
        "Bunny of the Moon!"
    ),
    "setup": [
        "Place the main game board in the center of the table.",
        "Place Ice Cream Tokens in the Ice Cream Supply Zone. Beginner Rule: place all tokens. Standard Rule: place 3 tokens of each flavor.",
        "Shuffle the Customer Deck and Ingredient Deck; place them face-down next to the board.",
        "Give each player a Player Board (1 per color). The player who ate ice cream most recently goes first.",
        "Distribute Turn Order Tokens and starting Ingredient Cards: Player 1 gets 3, Player 2 gets 4, Player 3 gets 5, Player 4 gets 6, Player 5 gets 7.",
        "Put all Score Markers on space 0.",
        "Standard Rule only: shuffle the Event Cards and place them on the moon symbol spaces on the board.",
    ],
    "round_structure": [
        "Phase 1 – Lunar Phase: Roll the D8 die to set the moon position (round 1 only), then advance the die one step each subsequent round. Reveal Customer Cards equal to players + 2, and reveal 4 Ingredient Cards into the Trade Area. (Standard Rule: also reveal and resolve 1 Event Card from the deck.)",
        "Phase 2 – Action Phase: Each player takes a turn in order, performing up to 5 actions: Trade, Draw, Craft, Serve, and Pass.",
        "Phase 3 – Transition Phase: Discard hand down to 7 cards, return unclaimed Customer Cards, advance the moon phase, and update turn order so the lowest-score player goes first.",
    ],
    "main_actions": [
        "**Trade**: Exchange up to 3 Ingredient Cards from your hand with cards in the Trade Area.",
        "**Draw**: Draw 4 cards from the Ingredient Deck (shuffle discard if deck runs out).",
        "**Craft**: Discard the required Ingredient Cards to take a matching Ice Cream Token from the Supply and place it on your Player Board. You can craft as many times as you want each turn. Shortcut: You can swap 2 of the same Common Ingredient for any 1 Common, or 2 of the same Rare Ingredient for any 1 Rare.",
        "**Serve**: Take a Customer Card and place matching Ice Cream Token(s) on the flavor icons shown. Advance your LP marker by the points shown. You may serve as many customers as you can. Bonus: if the customer's moon symbol matches the current moon phase, take 1 free Ingredient Card from the Trade Area.",
        "**Pass**: Declare 'Pass' to end your turn and let the next player go.",
    ],
    "end_game_condition": (
        "**After 6 rounds**: When the Round Die shows 6, finish the current round through all "
        "players' Action Phase, then proceed to Final Scoring.\n"
        "**All customers served**: If the last Customer Card is fully served with no cards left "
        "in the deck or on the table, the game ends immediately and proceeds to scoring."
    ),
    "scoring": [
        "Minus 1 LP per unserved Ice Cream Token remaining on a player's board.",
        "+3 LP for having 2 Customer Cards with the same Moon Position symbol.",
        "+5 LP for having 3 Customer Cards with the same Moon Position symbol.",
        "+10 LP for having 5 Customer Cards with 5 different Moon Position symbols.",
        "Minus 3 LP if a player has served 2 VIP customers.",
        "Tiebreaker order: most VIP customers served → most total Customer Cards → most variety of ice cream flavors served → lowest LP is declared the winner.",
    ],
    "advanced_rule": {
        "name": "Lock / Unlock",
        "summary": (
            "An optional rule for experienced players that lets players block each other from "
            "crafting certain flavors. Some Ingredient Cards carry a Lock or Unlock symbol "
            "tied to a specific flavor."
        ),
        "locking": (
            "When any player performs the Craft action, any other player may play a Lock "
            "Ingredient Card matching that flavor onto the ice cream scoop token. The crafting "
            "player must take all their used Ingredient Cards back (craft is canceled). The "
            "player who used the Lock Card then draws 1 card from the Ingredient Deck OR takes "
            "1 Ingredient Card from the Trade Area. Once locked, no player can craft that flavor "
            "until it is unlocked."
        ),
        "unlocking": (
            "To craft a locked flavor, the active player must discard an Unlock Ingredient Card "
            "matching the locked flavor. Remove the Lock card from the scoop and place it in the "
            "discard pile, then proceed with crafting as normal. The player who used the Unlock "
            "card may draw 1 Ingredient Card from the deck OR take 1 from the Trade Area."
        ),
    },
    "teaching_tips": [
        "Play the Beginner Rule first (all Ice Cream Tokens in supply, no Event Cards) — the basic turn of Trade → Draw → Craft → Serve clicks fast when players don't have Event Cards to worry about yet.",
        "Show players a Customer Card and walk through a full serve example before the first round: pick an available customer, match the flavor icons, take the LP.",
        "Remind players that whoever has the lowest score goes first next round — this keeps the game fair and gives trailing players first pick of ingredients.",
        "Point out the moon phase bonus on Customer Cards early; players often miss the free ingredient reward when serving a matching moon phase customer.",
    ],
    "strategy_tips": [
        "Watch the Trade Area closely — swapping ingredients early in your turn, before other players grab the best ones, is often better than drawing extra cards.",
        "Aim for Moon Position symbol bonuses at scoring: 3 cards with the same symbol (+5 LP) is often easier to build toward than it looks.",
        "Don't over-craft. Unserved Ice Cream Tokens on your board cost you LP at the end — only craft what you can realistically serve.",
        "VIP customers carry high point values during play but subtract 3 LP if you serve 2 or more — weigh the risk carefully before chasing VIPs.",
    ],
    "quiz": [
        {
            "question": "How many rounds does a standard game of Lunar Creamery last?",
            "options": ["4", "5", "6", "8"],
            "answer_index": 2,
        },
        {
            "question": "What is the tiebreaker if two players have the same Lunar Points at the end?",
            "options": [
                "The player who served the most total customers wins",
                "The player with more VIP customers served wins",
                "The player with the lowest remaining LP wins",
                "Re-roll the dice to determine the winner",
            ],
            "answer_index": 1,
        },
        {
            "question": "How many Ingredient Cards can you exchange during the Trade action?",
            "options": ["1", "2", "3", "4"],
            "answer_index": 2,
        },
        {
            "question": "What happens to leftover Ice Cream Tokens on a player's board at end game?",
            "options": [
                "They are worth +1 LP each",
                "They are worth 0 LP and discarded",
                "They cost -1 LP each",
                "They are passed to the player with the lowest score",
            ],
            "answer_index": 2,
        },
        {
            "question": "In the Standard Rule setup, how many Ice Cream Tokens of each flavor are placed in the Supply Zone?",
            "options": ["2", "3", "5", "All available"],
            "answer_index": 1,
        },
    ],
}

db.upsert_game(game)
print("Lunar Creamery upserted successfully.")

g = db.get_game("lunar_creamery")
print(f"Title: {g['title']}")
print(f"Scoring lines: {len(g['scoring'])}")
print(f"Advanced rule name: {g['advanced_rule']['name']}")
print(f"Quiz questions: {len(g['quiz'])}")
