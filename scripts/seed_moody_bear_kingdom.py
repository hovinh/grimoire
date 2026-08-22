import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
import utils.db as db

db.init_db()

game = {
    "id": "moody_bear_kingdom",
    "title": "Moody Bear Kingdom",
    "weight": "light",
    "bgg_weight": 1.5,
    "min_players": 3,
    "max_players": 5,
    "play_time": "20–35 min",
    "image_url": "https://placehold.co/400x280/2a0a0a/f7c948?text=Moody+Bear+Kingdom",
    "image_path": "data/images/moody-bear-kingdom.jpg",
    "mechanics": [
        "hidden roles",
        "hand management",
        "set collection",
        "bluffing",
        "take-that",
    ],
    "description": (
        "The throne of Moody Bear Kingdom has sat empty for thousands of years. "
        "Legendary items scattered across the land hold the power to crown a new ruler "
        "— but a monstrous Dark Swallow threatens to consume everything. Bears form "
        "secret teams to collect the sacred gems before it's too late."
    ),
    "theme": (
        "The ancient throne of Moody Bear Kingdom has been empty for a thousand years, "
        "and three secret teams are racing to claim it. Red Bears hunt for Lava Gems, "
        "Blue Bears seek Snow Diamonds, and a hidden Solo Bear hopes to let the dreaded "
        "Dark Swallow destroy everything before anyone wins. No one knows who's on whose "
        "side — so every trade could be a gift to an ally or a gift to your enemy. "
        "Collect your team's gems first, keep your identity secret, and be the first "
        "to stand up and proclaim victory for your kingdom!"
    ),
    "objective": (
        "Be the first team to collect all 3 of your team's legendary gems — Lava Gems "
        "for Red, Snow Diamonds for Blue — and proclaim victory. The Solo player wins if "
        "the Dark Swallow event triggers before any team claims victory."
    ),
    "setup": [
        "Sort cards by the symbols on their backs into separate piles (Team Cards, Item Cards).",
        "Pick Team Cards based on player count: 3 players = 1 Red, 1 Blue, 1 Solo; 4 players = 2 Red, 2 Blue; 5 players = 2 Red, 2 Blue, 1 Solo.",
        "Shuffle and deal one Team Card face-down to each player. Everyone keeps their team a secret. Put leftover Team Cards back in the box without looking at them.",
        "Set the Dark Swallow card face-down off to the side. Shuffle the rest of the Item Cards and deal 5 to each player.",
        "Once everyone has their 5 cards, shuffle the Dark Swallow back into the remaining Item Cards at a random position. This becomes the drawing deck.",
    ],
    "round_structure": [
        "Players take turns clockwise. The player who last physically touched the game box goes first.",
        "On your turn, you may do any of these actions in any order: Trade an Item Card (once per turn), Play Item Cards (as many as you want), or Pass.",
    ],
    "main_actions": [
        "**Trade an Item Card** (once per turn): Offer one of your Item Cards face-down to another player. They secretly look at it and decide to accept or reject. If they accept, they keep your card and must give you one of their cards in return — you cannot refuse. If they reject, you take your card back and draw 1 card from the deck.",
        "**Play Item Cards**: Announce the card name out loud before playing it. Other players may respond with a Cancel card to stop the effect. If no one cancels, the effect happens. You can play as many cards as you want per turn, including combos.",
        "**Pass**: Choose not to act. Draw 1 card from the drawing deck instead.",
    ],
    "card_effects": [
        "**Lava Gem** (x3): The Red team's victory gem. Red team must hold all 3 together to win.",
        "**Snow Diamond** (x3): The Blue team's victory gem. Blue team must hold all 3 together to win.",
        "**Duo Jewel** (promo): A wild gem — counts as either a Lava Gem or a Snow Diamond.",
        "**Reveal Identity**: Secretly peek at one player's Team Card. You can say anything afterward, but you cannot show the card to anyone.",
        "**Swap Hand**: Swap your entire hand of cards with another player's hand.",
        "**Shuffle the Deck**: Shuffle the drawing deck in a random order.",
        "**Cancel the Curse** (x4): Cancel any Item Card's effect at any time, even during combos.",
        "**Dark Swallow**: When drawn, the player must show it to everyone. If nobody plays a Mace of Light right away, the game ends and the Solo player wins. If someone plays a Mace of Light, the Dark Swallow is shuffled back into the deck at a random position.",
        "**Mace of Light** (x4): Play immediately in response to the Dark Swallow to send it back into the deck.",
        "**Forest Knight** (x7): Combo card — no effect on its own.",
        "**Ambassador of Earth** (x7): Combo card — no effect on its own.",
        "**Thunder Assassin** (x7): Combo card — no effect on its own.",
    ],
    "combo_cards": [
        "**Forest Knight + Thunder Assassin**: Pick a direction (left or right). Everyone must pass one Item Card of their choice to their neighbor in that direction.",
        "**Thunder Assassin + Ambassador of Earth**: Look at any one player's full hand of cards.",
        "**Forest Knight + Ambassador of Earth**: Look at the top 3 cards of the drawing deck, then put them back in any order you like.",
        "**Forest Knight + Thunder Assassin + Ambassador of Earth**: Ask any player for one specific card by name. If they have it, they must give it to you. If they don't, nothing happens.",
        "**A matching pair** (2× Forest Knight, 2× Ambassador of Earth, or 2× Thunder Assassin): Steal any one card you choose from any player.",
    ],
    "end_game_condition": (
        "**Red team wins**: The Red team together holds all 3 Lava Gems and proclaims victory.\n"
        "**Blue team wins**: The Blue team together holds all 3 Snow Diamonds and proclaims victory.\n"
        "**Solo player wins**: The Dark Swallow card appears and no one plays a Mace of Light in time.\n"
        "**Wrong proclamation**: If a team proclaims victory but doesn't actually meet the conditions, the other team wins immediately."
    ),
    "advanced_rule": {
        "name": "4-Player with Unknown Team Structure",
        "summary": (
            "When playing with exactly 4 players, you can optionally use the 5-player team "
            "setup to add extra uncertainty about whether a Solo player is even in the game."
        ),
        "details": (
            "Use 2 Red, 2 Blue, and 1 Solo Team Cards (5 total). Remove one card at random "
            "without looking at it, then deal one to each of the 4 players. Because one card "
            "was secretly set aside, nobody knows for sure whether both teams have 2 members "
            "or whether a Solo player is hiding among them — making every trade feel uncertain "
            "since nobody knows who is really on whose side."
        ),
    },
    "teaching_tips": [
        "Explain the three team goals before dealing any cards — Red collects Lava Gems, Blue collects Snow Diamonds, Solo wants the Dark Swallow to trigger. Players need this picture in their heads before the sneakiness begins.",
        "Before dealing, sort the Item Card deck into two piles — single-effect cards and combo cards — and walk through each pile's effects out loud. Explaining singles first, then combos, keeps players from confusing what a combo card does alone versus paired.",
        "Make clear that Team Cards stay face-down the whole game. Players are allowed to lie about their team, so bluffing is a core skill, not cheating.",
        "Walk through the Dark Swallow moment before the first game: when it appears, everyone has a split second to play a Mace of Light. Make sure everyone knows what those cards look like and what they do.",
        "Remind players that a wrong victory proclamation hands the win to the other team instantly — encourage everyone to double-check before standing up.",
    ],
    "strategy_tips": [
        "Use Reveal Identity early to confirm or deny allies before you share gems — trading a Lava Gem to an unknown player might be handing victory to the enemy.",
        "If you're on Red or Blue team, hold onto Cancel cards specifically for the Dark Swallow moment. Letting it go through gives the game to the Solo player.",
        "As the Solo player, act like a helpful teammate. Try to make sure the Mace of Light cards get traded away or played on other things before the Dark Swallow appears.",
        "As the Solo player, keep the pace brisk — every extra card drawn from the deck raises your odds of hitting the Dark Swallow. Encourage quick Passes and discourage stalling trades rather than sitting back.",
        "If the game feels like it's speeding up for no clear reason, be suspicious — that pace often means the Solo player is trying to draw into the Dark Swallow faster.",
        "In the 4-player Advanced Rule, play carefully in the early rounds — nobody knows if a Solo player is even in the game, so a quick victory proclamation based on a wrong read of your ally loses instantly.",
    ],
    "quiz": [
        {
            "question": "What happens when a player draws the Dark Swallow card?",
            "options": [
                "The player keeps it secret and adds it to their hand",
                "The player must show it to everyone; if no Mace of Light is played, the Solo player wins",
                "The card is immediately discarded and the game continues",
                "The player who drew it is out of the game",
            ],
            "answer_index": 1,
        },
        {
            "question": "When can a player proclaim victory?",
            "options": [
                "At any point during their turn",
                "Only after playing all their Item Cards",
                "Only at the start of their turn, before taking any actions",
                "At the end of their turn after passing",
            ],
            "answer_index": 2,
        },
        {
            "question": "If a Trade is rejected, what does the player who offered the card do?",
            "options": [
                "Discard the offered card",
                "Offer the card to a different player",
                "Take the card back and draw 1 card from the deck",
                "Place the card face-up in the center of the table",
            ],
            "answer_index": 2,
        },
        {
            "question": "What does the Forest Knight + Ambassador of Earth combo do?",
            "options": [
                "Look at another player's full hand",
                "Steal one card from any player",
                "Look at the top 3 cards of the drawing deck and rearrange them",
                "Force all players to pass a card to their neighbor",
            ],
            "answer_index": 2,
        },
        {
            "question": "How does the Solo player win the game?",
            "options": [
                "By collecting 3 Lava Gems before the Red team",
                "By holding the Duo Jewel at the end of the game",
                "By causing the Dark Swallow event to end the game before Red or Blue proclaims victory",
                "By having the most cards in hand when the deck runs out",
            ],
            "answer_index": 2,
        },
    ],
    "scoring": [],
}

db.upsert_game(game)
print("Moody Bear Kingdom upserted successfully.")

# Remove old hyphen-ID entry if it exists
import sqlite3
conn = sqlite3.connect(ROOT / "data" / "grimoire.db")
old = conn.execute("SELECT id FROM games WHERE id = 'moody-bear-kingdom'").fetchone()
if old:
    db.delete_game("moody-bear-kingdom")
    print("Deleted old moody-bear-kingdom entry.")
conn.close()

g = db.get_game("moody_bear_kingdom")
print(f"Title: {g['title']}")
print(f"Card effects: {len(g['card_effects'])}")
print(f"Combo cards: {len(g['combo_cards'])}")
print(f"Advanced rule: {g['advanced_rule']['name']}")
print(f"Quiz questions: {len(g['quiz'])}")
