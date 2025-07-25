# National Rail UK Home Assistant Component - Summary

## What Has Been Built

I've created a complete Home Assistant component for the UK National Rail API inspired by and based on the original [jfparis/homeassistant_nationalrail](https://github.com/jfparis/homeassistant_nationalrail/) repository, but updated to use the new Rail Data API with the following key changes:

**Repository**: [darrenparkinson/homeassistant_nationalrail](https://github.com/darrenparkinson/homeassistant_nationalrail)

The project includes both a backend integration and a frontend Lovelace card component.

### Key Updates from Original Component

1. **New API Base URL**: Updated to use `https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepartureBoard/{station_code}`

2. **Authentication Method**: Changed from username/password to API key authentication using the `x-apikey` header

3. **User-Agent Header**: Added required `User-Agent: ParkRail/1.1` header

4. **Modern Home Assistant Integration**: Updated to use the latest Home Assistant integration patterns with config flow

## Component Structure

```
custom_components/nationalrailuk/
├── __init__.py          # Main component initialization
├── const.py             # Constants and configuration keys
├── config_flow.py       # Configuration flow for UI setup
├── sensor.py            # Sensor implementation
├── manifest.json        # Component metadata
└── translations/
    └── en.json         # English translations

lovelace/
├── nationalrailuk-card.js    # Lovelace card component
├── hacs.json                 # HACS configuration
├── README.md                 # Card documentation
└── example-dashboard.yaml    # Example dashboard
```

## Features

### Backend Integration
- ✅ **Config Flow Integration**: Easy setup through Home Assistant UI
- ✅ **Real-time Data**: Fetches live departure board information
- ✅ **Filtering Support**: Filter by destination/origin station
- ✅ **Configurable Parameters**: Time windows, number of rows, etc.
- ✅ **Rich Sensor Attributes**: Detailed train information
- ✅ **Error Handling**: Proper error handling and logging
- ✅ **Rate Limiting**: Respects API rate limits
- ✅ **Station Database**: Includes comprehensive station codes

### Frontend Card
- ✅ **Simple Table Display**: Clean, compact table showing departures
- ✅ **Status Indicators**: Color-coded status for on-time, delayed, cancelled
- ✅ **Configurable**: Customize title, rows, filtering options
- ✅ **Responsive Design**: Adapts to different screen sizes
- ✅ **Real-time Updates**: Automatically updates when sensor data changes
- ✅ **HACS Compatible**: Easy installation via HACS

## Installation

### Quick Start

1. **Copy the component**:
   ```bash
   cp -r custom_components/nationalrailuk /path/to/homeassistant/config/custom_components/
   ```

2. **Restart Home Assistant**

3. **Add Integration**:
   - Go to Settings > Devices & Services > Add Integration
   - Search for "National Rail UK"
   - Enter your API key and station configuration

### Using the Install Script

```bash
./install.sh
```

## Configuration Example

### Basic Setup (All Departures)
```yaml
# Configuration via UI
name: "Waterloo Departures"
api_key: "your_api_key_here"
station_code: "WAT"
```

### Filtered Setup (Specific Route)
```yaml
# Configuration via UI
name: "Weybridge to Waterloo"
api_key: "your_api_key_here"
station_code: "WYB"
filter_crs: "WAT"
filter_type: "to"
num_rows: 10
time_window: 120
```

## API Testing

Test your API connection:

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
echo "NATIONAL_RAIL_API_KEY=your_key_here" > .env

# Test the API
python test_api.py
```

## Sensor Data

The component creates sensors with rich attributes:

```yaml
# Example sensor state
sensor.train_schedule_wyb_wat:
  state: "5 trains"
  attributes:
    station_name: "Weybridge"
    crs: "WYB"
    generated_at: "2024-01-15T10:30:00Z"
    trains:
      - std: "10:35"
        etd: "10:38"
        platform: "1"
        operator: "South Western Railway"
        destination: "London Waterloo"
        isCancelled: false
```

## Automation Examples

### Notify on Delays
```yaml
automation:
  - alias: "Train Delay Alert"
    trigger:
      platform: state
      entity_id: sensor.train_schedule_wyb_wat
    condition:
      - condition: template
        value_template: >
          {% for train in state_attr('sensor.train_schedule_wyb_wat', 'trains') %}
            {% if train.isCancelled or (train.etd != train.std) %}
              true
            {% endif %}
          {% endfor %}
    action:
      - service: notify.mobile_app
        data:
          title: "🚂 Train Delay"
          message: "Your train may be delayed or cancelled"
```

## Files Created

### Backend Integration
1. **`custom_components/nationalrailuk/`** - Complete Home Assistant component
2. **`README.md`** - Comprehensive documentation
3. **`API_DIFFERENCES.md`** - API migration guide
4. **`test_api.py`** - API testing script
5. **`requirements.txt`** - Python dependencies
6. **`install.sh`** - Installation script
7. **`env.example`** - Environment template

### Frontend Card
8. **`lovelace/nationalrailuk-card.js`** - Lovelace card component
9. **`lovelace/hacs.json`** - HACS configuration
10. **`lovelace/README.md`** - Card documentation
11. **`lovelace/example-dashboard.yaml`** - Example dashboard configuration

## Next Steps

1. **Get API Key**: Register at [Rail Data Portal](https://raildata.org.uk/)
2. **Test API**: Use the provided test script to verify connectivity
3. **Install Component**: Copy to your Home Assistant config directory
4. **Configure**: Add through Home Assistant UI
5. **Create Automations**: Set up notifications and alerts

## Support

- **API Issues**: Check [Rail Data Portal](https://raildata.org.uk/)
- **Component Issues**: Check [Home Assistant Community Forum](https://community.home-assistant.io/)
- **Testing**: Use the provided test script
- **Documentation**: See README.md and API_DIFFERENCES.md

## Credits

- Original component by [jfparis](https://github.com/jfparis/homeassistant_nationalrail/) - this component is inspired by their work
- Updated for new Rail Data API
- Station data from National Rail
- **Repository**: [darrenparkinson/homeassistant_nationalrail](https://github.com/darrenparkinson/homeassistant_nationalrail) 