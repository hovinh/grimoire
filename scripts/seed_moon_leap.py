import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
import utils.db as db

db.init_db()

game = {
    "id": "moon_leap",
    "title": "Moon Leap",
    "weight": "light",
    "bgg_weight": 1.2,
    "min_players": 2,
    "max_players": 4,
    "play_time": "~20 min",
    "image_url": "https://placehold.co/400x280/0d1b4b/e8e8e8?text=Moon+Leap",
    "image_path": "data/images/moon-leap.jpg",
    "mechanics": [
        "dice rolling",
        "positional movement",
        "score-and-reset",
        "push your luck",
    ],
    "description": (
        "Astronauts race across the moon's craters, leaping from space to space. "
        "Each token scores points by multiplying its number by the crater value "
        "it lands on — but the moon is crowded, tokens can leap over rivals, and "
        "well-timed chains earn extra rolls. Land wisely; the last three craters decide everything."
    ),
    "theme": (
        "The Moon is dotted with craters numbered from low to high, and your team of "
        "five astronauts is ready to leap across them! Each astronaut is numbered 1 to 5 "
        "— the bigger the number, the more they're worth when they land somewhere great. "
        "But watch out: minus craters at the edges can drag your score down, and any "
        "astronaut still waiting on the sideline when the race ends costs you points. "
        "Place all your astronauts wisely, build clever chains for extra rolls, and rack "
        "up the highest score before the last three craters are filled!"
    ),
    "objective": (
        "Score the most points when the game ends. Each token on the board scores "
        "token number × crater space value. The player with the highest total wins."
    ),
    "setup": [
        "Place the board in the center of the table.",
        "Each player picks a color and takes all 5 tokens of that color (numbered 1–5), placing them in front of themselves.",
        "Put tokens of unused colors back in the box.",
        "The youngest player takes the die and goes first. Play goes clockwise.",
    ],
    "round_structure": [
        "On your turn, roll the die.",
        "Place the token matching the rolled number onto the next free space on the board. Tokens automatically skip over any occupied spaces.",
        "If you roll an asterisk (*), you may move any one of your own tokens to the next free space.",
        "After the first time any token crosses the active Barrier (labeled to match your player count), you may split rolls of 3, 4, or 5 between two tokens.",
        "If your turn ends with 3 or more of your own tokens standing directly next to each other with no gaps, you earn an extra turn — roll again right away.",
        "If you cannot move at all, your turn is skipped.",
    ],
    "main_actions": [
        "**Roll and Place**: Roll the die and move the matching-numbered token to the next available space. Tokens jump over occupied spaces automatically.",
        "**Asterisk (*)**: Move any one of your own tokens to the next free space.",
        "**Split Roll** (after the barrier is crossed): Divide a roll of 3, 4, or 5 between two different tokens. Both tokens must be able to move — you can't split if one of them is stuck. Valid splits: 5 = 1+4 or 2+3; 4 = 1+3; 3 = 1+2. Rolls of 1, 2, or * cannot be split.",
        "**Chain Bonus**: If your turn creates a new chain of 3 or more of your tokens directly side by side with no gaps, roll again for a free extra turn. Chains that were already there before your turn don't count.",
    ],
    "end_game_condition": (
        "The game ends immediately when the last three spaces on the board are filled. "
        "All players then calculate their final scores."
    ),
    "scoring": [
        "For each token on the board: score = token number × crater space value.",
        "Tokens on red minus spaces score negative points (token number × negative value).",
        "Tokens on spaces with no point value score 0.",
        "Tokens never placed on the board score token number × -5 (a penalty for sitting out).",
        "Add all token scores together. The player with the highest total wins.",
        "Example: Token 2 on space 25 = 50 pts; Token 3 on space 9 = 27 pts; Token 5 on a -1 space = -5 pts; Token 4 never played = -20 pts; Token 1 on a 0-value space = 0 pts. Total = 52 pts.",
    ],
    "advanced_rule": {
        "name": "Split Roll (Barrier Rule)",
        "summary": (
            "Once any token crosses the active barrier for the first time, all players "
            "may split higher die rolls between two tokens for the rest of the game."
        ),
        "details": (
            "The board has three barriers labeled [2], [3], and [4] — use the one that "
            "matches your player count. Once the barrier is crossed, rolls of 3, 4, or 5 "
            "may be split: 5 into 1+4 or 2+3; 4 into 1+3; 3 into 1+2. Both moves from "
            "the split must be legal — you can't use a split if one of the two tokens "
            "can't move. You can move the two tokens in any order (e.g. move the 1 first, "
            "then the 4, or the other way around). The order matters: it can determine "
            "whether you create a chain of three and earn an extra turn."
        ),
    },
    "teaching_tips": [
        "Before the first turn, show the scoring formula with a quick example: 'If your 3-token lands on space 9, that's 27 points — but if it never enters play, that's -15 points.' The penalty for unplayed tokens surprises new players the most.",
        "Point out the minus spaces at the edges of the board early — players often rush forward without noticing tokens can land on negative craters.",
        "Explain the active barrier right away: show which barrier number matches the current player count, and remind everyone that splits only become available after the first token crosses it.",
        "Demo the chain bonus with a quick example before play — it's the most exciting moment in the game and gets players thinking about token placement from the very first roll.",
    ],
    "strategy_tips": [
        "Get all 5 tokens onto the board as early as you can — an unplayed token always costs 5× its number at the end, which can be a big penalty.",
        "Once the barrier unlocks, use splits to set up two tokens for a potential chain of three and fish for extra turns.",
        "Low-numbered tokens (1, 2) don't score much even on great spaces — use them to fill gaps and trigger chains rather than racing them to high-value craters.",
        "Watch where your opponents' tokens are sitting: since tokens skip over occupied spaces, a crowded board late in the game can push your token much further than you planned — sometimes right onto a minus space.",
    ],
    "quiz": [
        {
            "question": "How is a token's score calculated at the end of the game?",
            "options": [
                "The token number plus the space value",
                "The token number multiplied by the space value",
                "The space value divided by the token number",
                "A flat point value based on how far the token traveled",
            ],
            "answer_index": 1,
        },
        {
            "question": "What happens to tokens that were never placed on the board when the game ends?",
            "options": [
                "They score 0 points",
                "They score their token number in points",
                "They score token number × -5 (negative points)",
                "They are ignored in the final count",
            ],
            "answer_index": 2,
        },
        {
            "question": "What triggers an extra turn?",
            "options": [
                "Rolling an asterisk (*) on the die",
                "Moving a token past the active barrier",
                "Forming a new chain of 3 or more of your own tokens directly adjacent at the end of your turn",
                "Being the first player to place all 5 tokens on the board",
            ],
            "answer_index": 2,
        },
        {
            "question": "When rolling a 5 after the barrier is crossed, which split combinations are valid?",
            "options": [
                "1+4 or 2+3",
                "1+4 only",
                "2+3 only",
                "Any two numbers that add up to 5",
            ],
            "answer_index": 0,
        },
        {
            "question": "When does the game end?",
            "options": [
                "When one player has placed all 5 of their tokens",
                "After a fixed number of rounds equal to the player count",
                "As soon as the last three spaces on the board are occupied",
                "When the die has been rolled 20 times",
            ],
            "answer_index": 2,
        },
    ],
    "card_effects": [],
    "combo_cards": [],
}

db.upsert_game(game)
print("Moon Leap upserted successfully.")

import sqlite3
conn = sqlite3.connect(ROOT / "data" / "grimoire.db")
old = conn.execute("SELECT id FROM games WHERE id = 'moon-leap'").fetchone()
conn.close()
if old:
    db.delete_game("moon-leap")
    print("Deleted old moon-leap entry.")

g = db.get_game("moon_leap")
print(f"Title: {g['title']}")
print(f"Scoring lines: {len(g['scoring'])}")
print(f"Advanced rule: {g['advanced_rule']['name']}")
print(f"Quiz questions: {len(g['quiz'])}")
