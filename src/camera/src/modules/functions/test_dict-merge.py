import pytest

from modules.functions.dict import merge


def test_merge_level_1():

    base = { "foo": "bar" }
    add  = { "foo": "baz" }

    assert merge(base, add) == add


def test_merge_level_2():

    base = { "foo": "bar", "bing": { "a": "1", "b": "2" } }
    add  = { "foo": "baz", "bing": { "a": "3", "b": "2" }  }

    assert merge(base, add) == add


def test_merge_level_3():

    base = { "foo": "bar", "bing": { "a": "1", "b": { "zing": "zang" } } }

    # overwrite with same structure:
    add1  = { "foo": "baz", "bing": { "a": "3", "b": { "zing": "zong" } } }
    assert merge(base, add1) == add1
    
    # overwrite with primitive type:
    add2  = { "foo": "baz", "bing": { "a": "3", "b": "2" } }
    assert merge(base, add2) == add2
    
    # overwrite with dict:
    add3 = { "foo": "bar", "bing": { "a": { "foo": "bar", "1": "2" }, "b": { "zing": "zang" } } }
    assert merge(base, add3) == add3


def test_merge_do_not_delete_values():

    base = { "foo": "bar", "bing": { "a": "1", "b": { "zing": "zang" } } }

    # change only one value (level 1):
    add1  = { "foo": "baz" }
    assert merge(base, add1) == { "foo": "baz", "bing": { "a": "1", "b": { "zing": "zang" } } }

    # change only one value (level 2):
    add1  = { "bing": { "a": "5" } }
    assert merge(base, add1) == { "foo": "bar", "bing": { "a": "5", "b": { "zing": "zang" } } }

    # change only one value (level 3):
    add1  = { "bing": { "b": { "zing": "zonk" } } }
    assert merge(base, add1) == { "foo": "bar", "bing": { "a": "1", "b": { "zing": "zonk" } } }

    # overwrite with primitive type:
    add1  = { "bing": { "b": "a" } }
    assert merge(base, add1) == { "foo": "bar", "bing": { "a": "1", "b": "a" } }


def test_merge_explicitly_delete_value():
    """
    Note: Python doesn't really allow to delete variables. You can set them to None,
    so this is not different from setting any other value.
    """

    base = { "foo": "bar", "bing": { "a": "1", "b": { "zing": "zang" } } }

    # change only one value (level 1):
    add1  = { "foo": None }
    assert merge(base, add1) == { "foo": None, "bing": { "a": "1", "b": { "zing": "zang" } } }

    # change only one value (level 1):
    add2  = { "bing": None }
    assert merge(base, add2) == { "foo": "bar", "bing": None }


def test_merge_do_not_touch_input_dicts():

    base = { "foo": "bar", "bing": { "a": "1", "b": { "zing": "zang" } } }
    
    add1  = { "foo": "baz" }
    merge(base, add1)
    assert add1 == { "foo": "baz" }
    assert base == { "foo": "bar", "bing": { "a": "1", "b": { "zing": "zang" } } }
