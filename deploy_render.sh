#!/bin/bash
# Deploy to Render using their CLI

set -e

echo "📤 Uploading code to Render..."

# Use Render CLI to deploy
# The app will be deployed at: https://<service-name>-on-render.com

echo ""
echo "To deploy manually via dashboard:"
echo "  1. Push code to GitHub"
echo "  2. Go to https://dashboard.render.com"
echo "  3. Sign in with GitHub"
echo "  4. Click 'New' → 'Web Service'"
echo "  5. Connect your repository"
echo "  6. Leave defaults and deploy!"
echo ""
echo "Your app will be at: https://lao-python-learn.onrender.com"
