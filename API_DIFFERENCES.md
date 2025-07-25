# National Rail API Differences

This document outlines the key differences between the old National Rail API and the new API used in this component.

## Base URL Changes

### Old API
```
http://www.nationalrail.co.uk/ldbws/api/20220120/GetDepartureBoard/{station_code}
```

### New API
```
https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepartureBoard/{station_code}
```

## Authentication Changes

### Old API
- Used username/password authentication
- Required SOAP envelope format
- More complex authentication process

### New API
- Uses API key authentication
- API key passed in `x-apikey` header
- Simplified authentication process

## Required Headers

### New API Requirements
```http
x-apikey: YOUR_API_KEY
User-Agent: ParkRail/1.1
```

## API Parameters

The API parameters remain largely the same:

- `crs` (path parameter): Station CRS code
- `numRows` (query): Number of services to return (1-50)
- `filterCrs` (query): Filter by destination/origin station
- `filterType` (query): "to" or "from"
- `timeOffset` (query): Time offset in minutes (-60 to 60)
- `timeWindow` (query): Time window in minutes (1-300)

## Response Format

The response format is identical to the old API, maintaining compatibility with existing code.

## Rate Limits

### Old API
- Limited by account type
- Various rate limiting schemes

### New API
- 5 million requests per 4-week railway period
- More generous limits for most use cases

## Error Handling

### New API Error Responses
```json
{
  "error": "Error message",
  "status": 400
}
```

## Migration Guide

### For Existing Users

1. **Get New API Key**: Register at the new Rail Data Portal (https://raildata.org.uk/)
2. **Update Configuration**: Use the new API key in the `x-apikey` header
3. **Update Base URL**: The component automatically uses the new base URL
4. **Test Connection**: Use the provided test script to verify connectivity

### Configuration Changes

| Old Setting | New Setting |
|-------------|-------------|
| Username/Password | API Key |
| SOAP Authentication | Header Authentication |
| Complex setup | Simple API key |

## Testing the API

Use the provided test script:

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
echo "NATIONAL_RAIL_API_KEY=your_key_here" > .env

# Test the API
python test_api.py
```

## Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Check your API key is correct
   - Ensure the API key is in the `x-apikey` header

2. **403 Forbidden**
   - Verify your API subscription is active
   - Check rate limits

3. **404 Not Found**
   - Verify the station code is correct
   - Check the API endpoint URL

4. **User-Agent Issues**
   - Ensure the User-Agent is set to `ParkRail/1.1`
   - Some endpoints require this specific User-Agent

## API Documentation

For detailed API documentation, refer to:
- [Rail Data Portal](https://raildata.org.uk/)
- [API Swagger Documentation](assets/ldbws.json)

## Station Codes

Station codes (CRS) can be found in:
- `stations.json` file in this repository
- [National Rail Station Search](https://www.nationalrail.co.uk/stations/)
- [National Rail Data Portal](https://www.nationalrail.co.uk/developers/)

## Support

For API-related issues:
- Check the [Rail Data Portal](https://raildata.org.uk/)
- Review the API documentation
- Test with the provided test script

For component-related issues:
- Check the [Home Assistant Community Forum](https://community.home-assistant.io/)
- Review the component logs
- Verify your configuration 