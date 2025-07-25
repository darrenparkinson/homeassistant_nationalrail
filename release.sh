#!/bin/bash

# National Rail UK Home Assistant Component Release Script

if [ $# -eq 0 ]; then
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 1.0.0"
    exit 1
fi

VERSION=$1

echo "🚂 Creating release v$VERSION for National Rail UK Component"

# Update version in manifest files
echo "📝 Updating version numbers..."

# Update main component manifest
sed -i '' "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" custom_components/nationalrailuk/manifest.json

# Update card version in the JS file
sed -i '' "s/@version \".*\"/@version \"$VERSION\"/" lovelace/nationalrailuk-card.js

# Create git tag
echo "🏷️  Creating git tag v$VERSION..."
git add .
git commit -m "Release v$VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin main
git push origin "v$VERSION"

echo "✅ Release v$VERSION created successfully!"
echo "📦 HACS should now be able to install the component and card"
echo ""
echo "Next steps:"
echo "1. Wait a few minutes for GitHub to process the release"
echo "2. Try installing via HACS again"
echo "3. The installation buttons should now work properly" 