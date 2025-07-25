"""Constants for the National Rail UK integration."""

DOMAIN = "nationalrailuk"

CONF_API_KEY = "api_key"
CONF_STATION_CODE = "station_code"
CONF_FILTER_CRS = "filter_crs"
CONF_FILTER_TYPE = "filter_type"
CONF_NUM_ROWS = "num_rows"
CONF_TIME_WINDOW = "time_window"
CONF_TIME_OFFSET = "time_offset"

DEFAULT_NUM_ROWS = 10
DEFAULT_TIME_WINDOW = 120
DEFAULT_TIME_OFFSET = 0
DEFAULT_FILTER_TYPE = "to"

FILTER_TYPES = ["to", "from"]

BASE_URL = "https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepartureBoard"
USER_AGENT = "ParkRail/1.1" 