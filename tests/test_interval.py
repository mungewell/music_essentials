import pytest

from music_essentials import Interval

# Manual interval creation - correct values
def test_manual_interval_creation_correct_interval_major():
    i = Interval('M', 5)
    assert i.interval_type == 'M'

def test_manual_interval_creation_correct_interval_minor():
    i = Interval('m', 5)
    assert i.interval_type == 'm'

def test_manual_interval_creation_correct_interval_diminished():
    i = Interval('dim', 5)
    assert i.interval_type == 'dim'

def test_manual_interval_creation_correct_interval_augmented():
    i = Interval('aug', 5)
    assert i.interval_type == 'aug'

def test_manual_interval_creation_correct_distance_whole_number():
    i = Interval('aug', 5)
    assert i.distance == 5

def test_manual_interval_creation_correct_distance_as_string():
    i = Interval('aug', '7')
    assert i.distance == 7

# Interval creation from string - correct values
def test_interval_creation_correct_interval_major():
    i = Interval.from_interval_string('M5')
    assert i.interval_type == 'M'

def test_interval_creation_correct_interval_minor():
    i = Interval.from_interval_string('m5')
    assert i.interval_type == 'm'

def test_interval_creation_correct_interval_diminished():
    i = Interval.from_interval_string('dim5')
    assert i.interval_type == 'dim'

def test_interval_creation_correct_interval_augmented():
    i = Interval.from_interval_string('aug5')
    assert i.interval_type == 'aug'

def test_interval_creation_correct_distance():
    i = Interval.from_interval_string('aug5')
    assert i.distance == 5

# Manual interval creation - incorrect values
def test_manual_interval_creation_incorrect_interval_type():
    with pytest.raises(ValueError):
        i = Interval('asd', 5)

def test_manual_interval_creation_incorrect_distance_negative():
    with pytest.raises(ValueError):
        i = Interval('M', -5)

def test_manual_interval_creation_incorrect_distance_float_value():
    with pytest.raises(ValueError):
        i = Interval('M', 5.5)

def test_manual_interval_creation_incorrect_distance_string():
    with pytest.raises(ValueError):
        i = Interval('M', 'butts')

# Interval creation from string - incorrect values
def test_interval_creation_incorrect_interval_type():
    with pytest.raises(ValueError):
        i = Interval.from_interval_string('asd5')

def test_interval_creation_incorrect_distance_negative():
    with pytest.raises(ValueError):
        i = Interval.from_interval_string('M-5')

def test_interval_creation_incorrect_distance_float_value():
    with pytest.raises(ValueError):
        i = Interval.from_interval_string('M5.5')

def test_interval_creation_incorrect_distance_string():
    with pytest.raises(ValueError):
        i = Interval.from_interval_string('Mbutts')