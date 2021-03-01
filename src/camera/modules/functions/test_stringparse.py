import pytest

from modules.functions.stringparser import parseDuration


def test_parseDuration():

    # singular:
    assert parseDuration('1d') == 86400
    assert parseDuration('1h') == 3600
    assert parseDuration('1m') == 60
    assert parseDuration('10s') == 10

    # consecutive:
    assert parseDuration('3m5s') == 185
    assert parseDuration('2d1h3m5s') == 176585

    # with gap:
    assert parseDuration('1h5s') == 3605
    assert parseDuration('1d20s') == 86420

    # empty string:
    assert parseDuration('') == 0

    # shouldn't accept wrong order:
    # Would `ArithmeticError` fit better in this case?
    with pytest.raises(ValueError):
        parseDuration('1s2d')

    # shouldn't accept additional text or characters:
    with pytest.raises(ValueError):
        parseDuration('1d2m3foo')
    with pytest.raises(ValueError):
        parseDuration('foo')

    # shouldn't accept spaces:
    with pytest.raises(ValueError):
        parseDuration(' 1d2m')
    with pytest.raises(ValueError):
        parseDuration('1d2m ')
    with pytest.raises(ValueError):
        parseDuration('1d 2m')

    # shouldn't accept upper case:
    with pytest.raises(ValueError):
        parseDuration('1D')
    with pytest.raises(ValueError):
        parseDuration('1H')
    with pytest.raises(ValueError):
        parseDuration('1M')
    with pytest.raises(ValueError):
        parseDuration('1S')