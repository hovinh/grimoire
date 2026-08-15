import copy

import pytest

from utils import db


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "grimoire_test.db")
    db.init_db()
    return db


@pytest.fixture
def make_game():
    def _make_game(**overrides):
        game = {
            "id": "test_game",
            "title": "Test Game",
            "weight": "light",
            "bgg_weight": 1.5,
            "min_players": 2,
            "max_players": 4,
            "play_time": "30-45 min",
            "image_url": "https://example.com/img.jpg",
            "image_path": "data/images/test_game.jpg",
            "mechanics": ["Set Collection", "Hand Management"],
            "description": "A short description.",
            "theme": "A cozy narrative theme that makes the win condition clear.",
            "objective": "Score the most points.",
            "setup": ["Shuffle the deck.", "Deal 5 cards to each player."],
            "round_structure": ["Draw a card.", "Play a card.", "Discard down to hand limit."],
            "main_actions": ["**Draw**: take a card.", "**Play**: play a card."],
            "end_game_condition": "The deck runs out.",
            "card_effects": ["**Bonus**: gain 2 points."],
            "combo_cards": ["**Bonus** + **Draw**: gain 4 points."],
            "scoring": ["1 point per card.", "2 points per set."],
            "teaching_tips": ["Start with fewer cards for new players."],
            "strategy_tips": ["Collect sets early."],
            "advanced_rule": {"title": "Advanced Variant", "text": "Use the advanced deck."},
            "quiz": [
                {
                    "question": "What is the goal?",
                    "options": ["Score points", "Lose points", "Draw cards", "Discard cards"],
                    "answer_index": 0,
                },
            ],
        }
        game.update(overrides)
        return copy.deepcopy(game)

    return _make_game
