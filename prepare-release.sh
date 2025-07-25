#!/bin/bash

# Prepare Release Script for National Rail UK Component

if [ $# -eq 0 ]; then
    echo "Usage: ./prepare-release.sh <version>"
    echo "Example: ./prepare-release.sh 1.0.0"
    exit 1
fi

VERSION=$1

echo "🚂 Preparing release v$VERSION for National Rail UK Component"

# Update version in manifest files
echo "📝 Updating version numbers..."

# Update main component manifest
sed -i '' "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" custom_components/nationalrailuk/manifest.json

# Update card version in the JS file
sed -i '' "s/@version \".*\"/@version \"$VERSION\"/" lovelace/nationalrailuk-card.js

# Commit changes
echo "💾 Committing changes..."
git add .
git commit -m "Prepare release v$VERSION"

# Create tag
echo "🏷️  Creating git tag v$VERSION..."
git tag -a "v$VERSION" -m "Release v$VERSION"

# Push everything
echo "📤 Pushing to GitHub..."
git push origin main
git push origin "v$VERSION"

echo "✅ Release v$VERSION prepared successfully!"
echo ""
echo "📦 Manual Release Steps:"
echo "1. Go to https://github.com/darrenparkinson/homeassistant_nationalrail"
echo "2. Click 'Releases' in the right sidebar"
echo "3. Click 'Create a new release'"
echo "4. Select tag 'v$VERSION'"
echo "5. Add title: 'Release v$VERSION'"
echo "6. Add description:"
echo "   National Rail UK Home Assistant Component"
echo "   - Integration for Rail Data API"
echo "   - Lovelace card for train departures"
echo "   - HACS compatible"
echo "7. Click 'Publish release'"
echo "8. Wait 5-10 minutes for HACS to recognize the release"
echo "9. Try the HACS installation buttons again" 