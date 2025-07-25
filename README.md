# National Rail UK Home Assistant Component

This is a Home Assistant integration for the UK National Rail API that allows you to monitor train departures and arrivals at UK railway stations.

## Features

- Real-time train departure and arrival information
- Support for filtering by destination/origin station
- Configurable time windows and number of results
- Automatic updates every 5 minutes
- Rich sensor attributes with detailed train information
- **Lovelace Card**: Simple table display for dashboards

## Installation

### Prerequisites

1. **Get an API Key**: Register with Rail Data to get an API token at [Rail Data Portal](https://raildata.org.uk/)
2. **Find Station Codes**: Use the CRS (Computer Reservation System) codes for stations. You can find these in the `stations.json` file or on the [National Rail website](https://www.nationalrail.co.uk/stations/)

### Manual Installation

1. Copy the `custom_components/nationalrailuk` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings** > **Devices & Services** > **Add Integration**
4. Search for "National Rail UK" and add it
5. Enter your API key and station configuration

## Configuration

### Required Parameters

- **Name**: A friendly name for this integration instance
- **API Key**: Your National Rail API key
- **Station Code**: The CRS code of the station you want to monitor (e.g., "WAT" for London Waterloo)

### Optional Parameters

- **Filter CRS**: Filter results to show only trains going to/from a specific station
- **Filter Type**: Choose "to" (default) or "from" for the filter direction
- **Number of Rows**: How many services to return (1-50, default: 10)
- **Time Window**: How far into the future to look for services in minutes (1-300, default: 120)
- **Time Offset**: Offset from current time in minutes (-60 to 60, default: 0)

## Usage Examples

### Basic Setup (All Departures)
- Station Code: `WAT` (London Waterloo)
- Leave Filter CRS empty to see all departures

### Filtered Setup (Specific Route)
- Station Code: `WYB` (Weybridge)
- Filter CRS: `WAT` (London Waterloo)
- Filter Type: `to`
- This will show only trains from Weybridge to Waterloo

### Evening Return Journey
- Station Code: `WAT` (London Waterloo)
- Filter CRS: `WYB` (Weybridge)
- Filter Type: `to`
- This will show only trains from Waterloo to Weybridge

## Lovelace Card

This integration includes a custom Lovelace card for displaying train departures in a simple table format.

### Card Installation

The card can be installed via HACS or manually:

**HACS (Recommended):**
1. Add this repository as a custom repository in HACS
2. Search for "National Rail UK Card" in the Frontend section
3. Click "Download"

**Manual Installation:**
1. Copy `lovelace/nationalrailuk-card.js` to your `config/www/` directory
2. Add to your Lovelace resources:
```yaml
lovelace:
  resources:
    - url: /local/nationalrailuk-card.js
      type: module
```

### Card Usage

```yaml
type: custom:nationalrailuk-card
entity: sensor.train_schedule_wat_all
title: "London Waterloo"
max_rows: 8
```

See `lovelace/README.md` for detailed card documentation and examples.

## Sensor Data

The integration creates a sensor with the following attributes:

- **station_name**: Name of the station
- **crs**: Station CRS code
- **generated_at**: When the data was last updated
- **trains**: Array of train services with details including:
  - `std`: Scheduled departure time
  - `etd`: Expected departure time
  - `platform`: Platform number
  - `operator`: Train operator
  - `destination`: Final destination
  - `isCancelled`: Whether the service is cancelled
  - `delayReason`: Reason for delay (if applicable)
- **bus_services**: Bus replacement services
- **ferry_services**: Ferry services
- **nrcc_messages**: National Rail Customer Communications messages
- **platform_available**: Whether platform information is available
- **are_services_available**: Whether services are available

## Automation Examples

### Notify on Delays
```yaml
automation:
  - alias: "Notify on train delays"
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
          title: "Train Delay"
          message: "Your train may be delayed or cancelled"
```

### Binary Sensor for Disruptions
```yaml
template:
  - binary_sensor:
      - unique_id: train_disruption_wyb_wat
        name: "Train Disruption WYB to WAT"
        state: >
          {% set trains = state_attr('sensor.train_schedule_wyb_wat', 'trains') %}
          {% if trains %}
            {% for train in trains %}
              {% if train.isCancelled or (train.etd != train.std) %}
                true
              {% endif %}
            {% endfor %}
          {% else %}
            false
          {% endif %}
```

## API Information

This integration uses the Rail Data Live Departure Board API with the following specifications:

- **Base URL**: `https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepartureBoard/{station_code}`
- **Authentication**: API key in `x-apikey` header
- **User Agent**: `ParkRail/1.1`
- **Rate Limits**: 5 million requests per 4-week railway period

## Troubleshooting

### Common Issues

1. **"Failed to connect to National Rail API"**
   - Check your API key is correct
   - Ensure you have an active National Rail API subscription
   - Verify the station code is valid

2. **No train data showing**
   - Check the station code is correct
   - Verify the station has regular services
   - Try increasing the time window

3. **API rate limiting**
   - The integration updates every 5 minutes by default
   - You can reduce update frequency if needed

### Debugging

Enable debug logging by adding to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.nationalrailuk: debug
```

## Contributing

This component is inspired by and based on the original work by [jfparis](https://github.com/jfparis/homeassistant_nationalrail/) but updated to use the new Rail Data API.

**Repository**: [darrenparkinson/homeassistant_nationalrail](https://github.com/darrenparkinson/homeassistant_nationalrail)

## License

This project is licensed under the MIT License.

## Credits

- Original component by [jfparis](https://github.com/jfparis/homeassistant_nationalrail/) - this component is inspired by their work
- Updated for new Rail Data API
- Station data from National Rail
- **Repository**: [darrenparkinson/homeassistant_nationalrail](https://github.com/darrenparkinson/homeassistant_nationalrail) 