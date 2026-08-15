def test_init_db_creates_expected_tables(test_db):
    conn = test_db._connect()
    tables = {
        row[0]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    }
    conn.close()
    assert {"games", "quiz_questions"}.issubset(tables)


def test_init_db_is_idempotent(test_db):
    test_db.init_db()
    test_db.init_db()

    conn = test_db._connect()
    columns = [row[1] for row in conn.execute("PRAGMA table_info(games)").fetchall()]
    conn.close()

    assert columns.count("advanced_rule") == 1
    assert columns.count("card_effects") == 1


def test_get_game_missing_returns_none(test_db):
    assert test_db.get_game("does_not_exist") is None


def test_upsert_and_get_game_roundtrip(test_db, make_game):
    game = make_game()
    test_db.upsert_game(game)

    fetched = test_db.get_game("test_game")

    assert fetched["id"] == "test_game"
    assert fetched["title"] == "Test Game"
    assert fetched["mechanics"] == ["Set Collection", "Hand Management"]
    assert fetched["setup"] == ["Shuffle the deck.", "Deal 5 cards to each player."]
    assert fetched["advanced_rule"] == {"title": "Advanced Variant", "text": "Use the advanced deck."}
    assert fetched["quiz"] == [
        {
            "question": "What is the goal?",
            "options": ["Score points", "Lose points", "Draw cards", "Discard cards"],
            "answer_index": 0,
        },
    ]


def test_upsert_game_update_replaces_fields_and_quiz(test_db, make_game):
    test_db.upsert_game(make_game())

    updated = make_game(
        title="Updated Title",
        weight="heavy",
        quiz=[
            {
                "question": "New question?",
                "options": ["A", "B", "C", "D"],
                "answer_index": 2,
            },
        ],
    )
    test_db.upsert_game(updated)

    fetched = test_db.get_game("test_game")
    assert fetched["title"] == "Updated Title"
    assert fetched["weight"] == "heavy"
    assert len(fetched["quiz"]) == 1
    assert fetched["quiz"][0]["question"] == "New question?"

    all_games = test_db.get_all_games()
    assert len(all_games) == 1


def test_advanced_rule_none_roundtrip(test_db, make_game):
    game = make_game(advanced_rule=None)
    test_db.upsert_game(game)

    fetched = test_db.get_game("test_game")
    assert fetched["advanced_rule"] is None


def test_list_fields_default_to_empty_when_omitted(test_db, make_game):
    game = make_game()
    del game["mechanics"]
    del game["teaching_tips"]
    test_db.upsert_game(game)

    fetched = test_db.get_game("test_game")
    assert fetched["mechanics"] == []
    assert fetched["teaching_tips"] == []


def test_get_all_games_orders_by_weight_then_title(test_db, make_game):
    test_db.upsert_game(make_game(id="zebra", title="Zebra Game", weight="heavy"))
    test_db.upsert_game(make_game(id="apple", title="Apple Game", weight="light"))
    test_db.upsert_game(make_game(id="banana", title="Banana Game", weight="medium"))
    test_db.upsert_game(make_game(id="cherry", title="Cherry Game", weight="light"))

    titles = [g["title"] for g in test_db.get_all_games()]

    assert titles == ["Apple Game", "Cherry Game", "Banana Game", "Zebra Game"]


def test_delete_game_removes_game_and_cascades_quiz(test_db, make_game):
    test_db.upsert_game(make_game())
    assert test_db.get_game("test_game") is not None

    test_db.delete_game("test_game")

    assert test_db.get_game("test_game") is None

    conn = test_db._connect()
    remaining_quiz = conn.execute(
        "SELECT COUNT(*) FROM quiz_questions WHERE game_id = ?", ("test_game",)
    ).fetchone()[0]
    conn.close()
    assert remaining_quiz == 0
