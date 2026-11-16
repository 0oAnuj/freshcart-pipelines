from stream.routing import topic_matches


def test_topic_bindings_match_assignment_examples():
    assert topic_matches("bangalore.koramangala.*", "bangalore.koramangala.food")
    assert topic_matches("bangalore.#", "bangalore.koramangala.food")
    assert topic_matches("bangalore.#", "bangalore")
    assert not topic_matches("bangalore.*.ride", "bangalore.whitefield.food")
    assert not topic_matches("bangalore.#", "chennai.tnagar.food")
