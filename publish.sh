#!/bin/bash

# Auto-Publish Script for Smart Retail App
echo "Starting publish process..."

# Navigate to the correct directory automatically
cd "$(dirname "$0")"

# Generate QR codes first to ensure they are updated
echo "Generating latest QR Codes..."
python3 -c "import generate_qrs; generate_qrs.generate_qrs('https://qrscannerq1.vercel.app')"

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo "No changes to publish."
    exit 0
fi

# Add, commit, and push
git add .
git commit -m "Auto-published updates from Admin UI 🚀"
git push

echo "Successfully published to live website!"
