from types import SimpleNamespace

import event


def make_de(devices):
    return SimpleNamespace(Devices=devices, Log=lambda msg: None)


def rate_devices(download=0, upload=0):
    return {
        "Freebox - API - Débit download": SimpleNamespace(n_value=download),
        "Freebox - API - Débit upload": SimpleNamespace(n_value=upload),
    }


def test_is_ready_shut_without_nosleep_switch():
    de = make_de(rate_devices())
    assert event.is_ready_shut(de, 100, 3600, None) is True


def test_is_ready_shut_blocked_by_nosleep_switch():
    devices = rate_devices()
    devices["Freebox - insomnie"] = SimpleNamespace(n_value_string="On")
    de = make_de(devices)
    assert event.is_ready_shut(de, 100, 3600, "Freebox - insomnie") is False


def test_is_ready_shut_blocked_by_high_download_rate():
    de = make_de(rate_devices(download=500))
    assert event.is_ready_shut(de, 100, 3600, None) is False


def test_is_ready_shut_without_rate_devices():
    de = make_de({})
    assert event.is_ready_shut(de, 100, 3600, None) is True


def test_diff_time_one_hour():
    assert event.diff_time("22:00", "23:00") == 3600


def test_diff_time_wraparound_past_midnight():
    assert event.diff_time("23:00", "08:00") == 9 * 3600


def test_diff_time_zero():
    assert event.diff_time("08:00", "08:00") == 0
