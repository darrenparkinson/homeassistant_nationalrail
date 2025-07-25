# National Rail UK Card

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=darrenparkinson&repository=homeassistant_nationalrail&category=plugin)

A simple Lovelace card for displaying train departures from the National Rail UK Home Assistant integration.

## Features

- **Simple Table Display**: Clean, compact table showing departure times, destinations, and status
- **Status Indicators**: Color-coded status for on-time, delayed, and cancelled trains
- **Configurable**: Customize title, number of rows, and filtering options
- **Responsive Design**: Adapts to different screen sizes
- **Real-time Updates**: Automatically updates when sensor data changes

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Add this repository as a custom repository in HACS
3. Search for "National Rail UK Card" in the Frontend section
4. Click "Download"
5. Restart Home Assistant

### Manual Installation

1. Download the `nationalrailuk-card.js` file
2. Place it in your `config/www/` directory
3. Add the following to your `configuration.yaml`:

```yaml
lovelace:
  mode: yaml
  resources:
    - url: /local/nationalrailuk-card.js
      type: module
```

## Configuration

### Basic Configuration

```yaml
type: custom:nationalrailuk-card
entity: sensor.train_schedule_wat_all
title: "Waterloo Departures"
```

### Advanced Configuration

```yaml
type: custom:nationalrailuk-card
entity: sensor.train_schedule_wyb_wat
title: "Weybridge to Waterloo"
max_rows: 8
show_delayed: true
show_cancelled: true
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entity` | string | **required** | The National Rail sensor entity ID |
| `title` | string | "Train Departures" | Card title |
| `max_rows` | number | 10 | Maximum number of trains to display |
| `show_delayed` | boolean | true | Whether to show delayed trains |
| `show_cancelled` | boolean | true | Whether to show cancelled trains |

## Usage Examples

### Basic Departure Board

```yaml
type: custom:nationalrailuk-card
entity: sensor.train_schedule_wat_all
title: "London Waterloo"
```

### Filtered Route Display

```yaml
type: custom:nationalrailuk-card
entity: sensor.train_schedule_wyb_wat
title: "Weybridge → Waterloo"
max_rows: 5
```

### Compact Display

```yaml
type: custom:nationalrailuk-card
entity: sensor.train_schedule_wat_wyb
title: "Waterloo → Weybridge"
max_rows: 3
show_cancelled: false
```

## Status Indicators

The card displays different status indicators:

- **🟢 On time**: Green text for trains running on schedule
- **🟡 Delayed**: Orange text with delay time (e.g., "+5min")
- **🔴 Cancelled**: Red text for cancelled trains

## Styling

The card uses Home Assistant's CSS custom properties for consistent theming:

- `--ha-card-background`: Card background color
- `--primary-text-color`: Main text color
- `--secondary-text-color`: Secondary text color
- `--divider-color`: Border and divider colors
- `--primary-color`: Primary accent color

## Troubleshooting

### Card Not Loading

1. Check that the JavaScript file is properly loaded in your resources
2. Verify the entity ID exists and is a National Rail sensor
3. Check the browser console for JavaScript errors

### No Trains Displayed

1. Verify the sensor has data (check the sensor state in Developer Tools)
2. Check if the sensor's `trains` attribute contains data
3. Try adjusting the `show_delayed` and `show_cancelled` options

### Styling Issues

1. The card uses Home Assistant's theme variables
2. If colors don't match your theme, check your theme configuration
3. You can override styles using the `style` property in your configuration

## Development

### Building from Source

1. Clone the repository
2. Make your changes to `nationalrailuk-card.js`
3. Test in your Home Assistant instance
4. Submit a pull request

### Local Development

For local development, you can:

1. Place the card file in `config/www/`
2. Add it as a resource in your Lovelace configuration
3. Use browser developer tools to debug

## Support

- **Issues**: Report issues on the GitHub repository
- **Questions**: Ask in the Home Assistant Community Forum
- **Feature Requests**: Submit via GitHub issues

## Credits

- Inspired by the original National Rail integration by [jfparis](https://github.com/jfparis/homeassistant_nationalrail/)
- Code structure inspired by [ChevronTango's National Rail Status Card](https://github.com/ChevronTango/nationalrail-status-card)
- Built for the new Rail Data API
- Designed for Home Assistant Lovelace UI 