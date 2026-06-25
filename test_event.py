import event


def test_diff_time_one_hour():
    assert event.diff_time("22:00", "23:00") == 3600


def test_diff_time_wraparound_past_midnight():
    assert event.diff_time("23:00", "08:00") == 9 * 3600


def test_diff_time_zero():
    assert event.diff_time("08:00", "08:00") == 0
