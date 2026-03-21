#!/bin/bash

# Fetch Shopware Upgrade Documents Script
# This script downloads the latest Shopware upgrade guides for versions 6.5, 6.6, and 6.7

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCES_DIR="$SCRIPT_DIR/resources"

# URLs to fetch
declare -A URLs=(
    ["6.5"]="https://raw.githubusercontent.com/shopware/shopware/trunk/UPGRADE-6.5.md"
    ["6.6"]="https://raw.githubusercontent.com/shopware/shopware/trunk/UPGRADE-6.6.md"
    ["6.7"]="https://raw.githubusercontent.com/shopware/shopware/trunk/UPGRADE-6.7.md"
)

echo -e "${YELLOW}Fetching Shopware upgrade documents...${NC}"

# Create resources directory if it doesn't exist
mkdir -p "$RESOURCES_DIR"

# Fetch each document
for version in "${!URLs[@]}"; do
    url="${URLs[$version]}"
    output_file="$RESOURCES_DIR/UPGRADE-$version.md"
    
    echo -e "${YELLOW}Fetching UPGRADE-$version.md...${NC}"
    
    if curl -s -f -L "$url" -o "$output_file"; then
        echo -e "${GREEN}✓ Successfully fetched UPGRADE-$version.md${NC}"
        
        # Add a header with fetch timestamp
        temp_file=$(mktemp)
        echo "---" > "$temp_file"
        echo "fetched: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$temp_file"
        echo "source: $url" >> "$temp_file"
        echo "---" >> "$temp_file"
        echo "" >> "$temp_file"
        cat "$output_file" >> "$temp_file"
        mv "$temp_file" "$output_file"
        
    else
        echo -e "${RED}✗ Failed to fetch UPGRADE-$version.md${NC}"
        echo "URL: $url"
    fi
done

echo -e "${GREEN}Fetch complete!${NC}"
echo "Documents saved in: $RESOURCES_DIR"
ls -la "$RESOURCES_DIR"
