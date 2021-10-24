from inflection import underscore


def snakify(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for key, val in obj.items():
            new_obj[underscore(key)] = snakify(val)
        return new_obj
    elif isinstance(obj, list):
        new_obj = []
        for elem in obj:
            new_obj.append(snakify(elem))
        return new_obj
    else:
        return obj


def test_level1():
    hsh = {"keyOne": 1, "KeyTwo": 2.2, "key_three": "hello"}
    exp = {"key_one": 1, "key_two": 2.2, "key_three": "hello"}
    act = snakify(hsh)
    assert act == exp


def test_seq_val():
    hsh = {"keyOne": [1, 2, 3], "KeyTwo": 2.2, "key_three": "hello"}
    exp = {"key_one": [1, 2, 3], "key_two": 2.2, "key_three": "hello"}
    act = snakify(hsh)
    assert act == exp


def test_nested():
    hsh = {
        "KeyOne": 1,
        "KeyTwo": {"KeyTwoA": 1, "KeyTwoB": [1, 2, 3]},
        "key_Three": "hello",
    }
    exp = {
        "key_one": 1,
        "key_two": {"key_two_a": 1, "key_two_b": [1, 2, 3]},
        "key_three": "hello",
    }
    act = snakify(hsh)
    assert act == exp


def test_nested_deep():
    hsh = {
        "KeyOne": 1,
        "KeyTwo": {
            "KeyTwoA": 1,
            "KeyTwoB": [1, 2, 3],
            "KeyTwoC": {"KeyTwoCOne": 1, "KeyTwoCTwo": 2},
        },
        "key_Three": "hello",
    }
    exp = {
        "key_one": 1,
        "key_two": {
            "key_two_a": 1,
            "key_two_b": [1, 2, 3],
            "key_two_c": {"key_two_c_one": 1, "key_two_c_two": 2},
        },
        "key_three": "hello",
    }
    act = snakify(hsh)
    assert act == exp


def test_seq_map():
    hsh = {
        "KeyOne": [1, 2, 3],
        "keyTwo": "hello",
        "key_three": {
            "keyThreeOne": 1,
            "keyThreeTwo": 1.1,
            "key_three_three": {"KeyThreeThreeFour": 12},
        },
        "keyFour": [1, {"KeyFourOne": 1, "keyFourTwo": 2}, [1, 2, 3]],
    }
    exp = {
        "key_one": [1, 2, 3],
        "key_two": "hello",
        "key_three": {
            "key_three_one": 1,
            "key_three_two": 1.1,
            "key_three_three": {"key_three_three_four": 12},
        },
        "key_four": [1, {"key_four_one": 1, "key_four_two": 2}, [1, 2, 3]],
    }
    act = snakify(hsh)
    assert exp == act


def test_seq():
    ary = [1, 2, 3]
    act = snakify(ary)
    exp = [1, 2, 3]
    assert exp == act


def test_seq_of_maps():
    ary = [1, {"KeyFourOne": 1, "keyFourTwo": 2}, [1, 2, 3]]
    exp = [1, {"key_four_one": 1, "key_four_two": 2}, [1, 2, 3]]
    act = snakify(ary)
    assert exp == act
