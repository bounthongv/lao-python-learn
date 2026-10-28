#!/bin/bash
# Deploy Lao Python Learning Platform to Hugging Face Spaces

set -e

cd "$(dirname "$0")"

echo "=== Deploy to Hugging Face Spaces ==="
echo ""

# Check for HF token
if [ -z "$HF_TOKEN" ]; then
    echo "ERROR: HF_TOKEN environment variable not set"
    echo ""
    echo "Get a token from: https://huggingface.co/settings/tokens"
    echo "Then run: export HF_TOKEN='your-token-here'"
    exit 1
fi

# Check requirements
echo "Checking requirements..."
source venv/bin/activate
python -c "import gradio; print(f'Gradio {gradio.__version__} OK')"

# Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << 'EOF'
HUGGINGFACE_TOKEN=placeholder
EOF
fi

# Update .env with real token
sed -i "s/HUGGINGFACE_TOKEN=placeholder/HUGGINGFACE_TOKEN=$HF_TOKEN/" .env

echo ""
echo "Starting deployment..."
echo ""
echo "This will:"
echo "  1. Create a Hugging Face Space called 'lao-python-learn'"
echo "  2. Upload your code"
echo "  3. Set up the space with Docker support"
echo ""
echo "Your space will be at: https://huggingface.co/spaces/YOUR_USERNAME/lao-python-learn"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Get username
USERNAME=$(hf auth whoami --token "$HF_TOKEN" 2>/dev/null | grep "^name:" | awk '{print $2}')
if [ -z "$USERNAME" ]; then
    echo "ERROR: Could not get username from token"
    exit 1
fi

echo "Detected username: $USERNAME"
SPACE_ID="$USERNAME/lao-python-learn"
echo "Space ID: $SPACE_ID"
echo ""

# Create space
echo "Creating Hugging Face Space..."
huggingface-cli upload \
    --repo-type space \
    --repo-id "$SPACE_ID" \
    --token "$HF_TOKEN" \
    .

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your learning platform is live at:"
echo "  https://huggingface.co/spaces/$USERNAME/lao-python-learn"
echo ""
echo "To update later, just run this script again."
