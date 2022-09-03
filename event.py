"""
Domoticz passes information to python scripts through global variables and the
domoticz python module

The global variables in the script are:
 * changed_device: the current device that changed (object of Device)
 * changed_device_name: name of current device (same as changed_device.name)
 * is_daytime: boolean, true when it is is daytime
 * is_nighttime: same for the night
 * sunrise_in_minutes: integer
 * sunset_in_minutes: integer
 * user_variables: dictionary from string to value

A Device has a number of attributes and methods
The attributes are:
 * id
 * name
 * type
 * sub_type
 * switch_type
 * n_value
 * n_value_string
 * s_value
 * last_update_string
 * last_update: datetime object

The methods are:
 * def last_update_was_ago(self, **kwargs):
    Arguments can be: days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]
 * def is_on(self):
    returns True when device is on
 * def is_off(self):
    returns True when device is off

 * def on(self, after=None, reflect=False):
 	  turns device on, after is optional and are the number of seconds after which
    to turn the device on.
    If reflect is True, a next call to is_on will return True, while normally
    domoticz will first have to go through possible script before turning it on
 	def off(self, after=None, reflect=False):
 		simular to on()

uservariables and uservariables_lastupdate are arrays for all user variables:
 uservariables['yourvariablename'] = 'Test Value'
 uservariables_lastupdate['yourvariablename'] = '2015-12-27 11:19:22'

other useful details are contained in the following global variables:
 * is_daytime
 * is_nighttime
 * sunrise_in_minutes
 * sunset_in_minutes
 * (TODO) security

Compare to Lua, instead of filling a commandArray, you change the status of a
device by calling device.on() or device.off()

TODO: setting variables

Calling Python's print function will not print to the domoticz console, see below
"""
import datetime
import DomoticzEvents as DE

# > Weekday = (' Sun ', ' Mon ', ' Tue ', ' Wed ', ' Thu ', ' Fri ', ' Sat ')
WEEK_SLEEP  = ('23:00', '23:00', '23:00', '23:00', '23:00', '23:30', '23:30')
WEEK_WAKEUP = ('08:00', '06:45', '06:45', '06:45', '06:45', '06:45', '08:00')
RATE_LIMIT = 100 # in Ko
SWITCH_FREEBOX = "Freebox"

now = datetime.datetime.now()
day = int(float(now.strftime("%w"))) # Weekday (as integer) -> 0=Sun, 1=Mon, 2=Tue...

sleep_time = WEEK_SLEEP[day]
wakeup_time = WEEK_WAKEUP[day]

def diff_time (begin=sleep_time, end=wakeup_time):
    """
    number of sec between two clock : end - begin

    Args:
        begin (str, optional): '%H:%M'. Defaults to sleep_time.
        end (str, optional): '%H:%M'. Defaults to wakeup_time.

    Returns:
        int: seconds from begin to end
    """
    start, stop = begin.split(':'), end.split(':')
    start_h, start_m = int(float(start[0])), int(float(start[1]))
    stop_h, stop_m = int(float(stop[0])), int(float(stop[1]))
    delta = (stop_h * 60 + stop_m) - (start_h * 60 + start_m)
    if delta < 0:
        delta = delta + 1440
    return delta * 60

def is_ready_shut(DE, rate_limit, wake_after):
    """
    Can I shutdown the Freebox?

    Args:
        rate_limit (int): dl / ul limit (in ko/s). If limit is reach Freebox isn't ready to shutdown
        wake_after (int): how long (in second)

    Returns:
        bool: False if Freebox is used else True
    """
    res = DE.Devices["Freebox - API - Freebox Player 1"].n_value_string == "Off" \
    and DE.Devices["Freebox - API - Débit download"].n_value < rate_limit \
    and DE.Devices["Freebox - API - Débit upload"].n_value < rate_limit \
    and (
        DE.Devices["Freebox - API - Next Record In"].n_value == -1
        or
        DE.Devices["Freebox - API - Next Record In"].n_value > wake_after
        )
    return res

def shutdown(DE, device=SWITCH_FREEBOX):
    """
    shutdown device

    Args:
        device (str, optional): device to shutdown. Defaults to "Freebox".
    """
    if DE.Devices[device].n_value_string == "On":
        DE.Log("Bonne nuit Free!")
        DE.Command(device, "Off")

def wakeup(DE, device=SWITCH_FREEBOX):
    """
    wake up device

    Args:
        device (str, optional): device to wake up. Defaults to "Freebox".
    """
    if DE.Devices[device].n_value_string == "Off":
        DE.Command(device, "On")

if now.strftime('%H:%M') == sleep_time:
    DE.Log("It's time to sleep")
    if is_ready_shut(DE, RATE_LIMIT, diff_time()):
        shutdown(DE)
elif now.strftime('%H:%M') == wakeup_time:
    DE.Log("It's time to wakeup")
    wakeup(DE)
