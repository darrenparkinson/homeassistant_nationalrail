#!/bin/bash

# Manual Release Script for National Rail UK Component

if [ $# -eq 0 ]; then
    echo "Usage: ./manual-release.sh <version>"
    echo "Example: ./manual-release.sh 1.0.0"
    exit 1
fi

VERSION=$1

echo "🚂 Creating manual release v$VERSION for National Rail UK Component"

# Update version in manifest files
echo "📝 Updating version numbers..."

# Update main component manifest
sed -i '' "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" custom_components/nationalrailuk/manifest.json

# Update card version in the JS file
sed -i '' "s/@version \".*\"/@version \"$VERSION\"/" lovelace/nationalrailuk-card.js

# Commit changes
echo "💾 Committing changes..."
git add .
git commit -m "Release v$VERSION"

# Create and push tag
echo "🏷️  Creating git tag v$VERSION..."
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin main
git push origin "v$VERSION"

echo "✅ Manual release v$VERSION created successfully!"
echo ""
echo "📦 Next steps:"
echo "1. Go to GitHub repository"
echo "2. Click on 'Releases' in the right sidebar"
echo "3. Click 'Create a new release'"
echo "4. Select the tag 'v$VERSION'"
echo "5. Add release notes and publish"
echo "6. Wait a few minutes for HACS to recognize the release"
echo "7. Try installing via HACS again" 