#!/bin/bash

# National Rail UK Home Assistant Component Installation Script

echo "🚂 National Rail UK Home Assistant Component Installer"
echo "=================================================="

# Check if we're in the right directory
if [ ! -d "custom_components/nationalrailuk" ]; then
    echo "❌ Error: custom_components/nationalrailuk directory not found!"
    echo "Please run this script from the root of the component directory."
    exit 1
fi

# Get Home Assistant config directory
echo "Please enter your Home Assistant configuration directory:"
echo "Default: /config (for Docker installations)"
read -p "Config directory: " config_dir

if [ -z "$config_dir" ]; then
    config_dir="/config"
fi

# Check if config directory exists
if [ ! -d "$config_dir" ]; then
    echo "❌ Error: Config directory '$config_dir' does not exist!"
    echo "Please check your Home Assistant installation path."
    exit 1
fi

# Create custom_components directory if it doesn't exist
if [ ! -d "$config_dir/custom_components" ]; then
    echo "📁 Creating custom_components directory..."
    mkdir -p "$config_dir/custom_components"
fi

# Copy the component
echo "📋 Copying National Rail UK component..."
cp -r custom_components/nationalrailuk "$config_dir/custom_components/"

if [ $? -eq 0 ]; then
    echo "✅ Component copied successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Restart Home Assistant"
    echo "2. Go to Settings > Devices & Services > Add Integration"
    echo "3. Search for 'National Rail UK' and add it"
    echo "4. Enter your API key and station configuration"
    echo ""
    echo "📖 For detailed instructions, see README.md"
else
    echo "❌ Error copying component!"
    exit 1
fi 