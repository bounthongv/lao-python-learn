#!/usr/bin/env python3
"""
Deploy Lao Python Learning Platform to Render.com (via CLI)

Prerequisites:
    - pip install render-cli
    - render login
"""

import os
import sys
import subprocess
from pathlib import Path

def check_render_cli():
    """Check if Render CLI is installed."""
    try:
        result = subprocess.run(["render", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return None

def deploy_to_render():
    """Deploy to Render using their CLI."""
    
    # Check CLI
    version = check_render_cli()
    if not version:
        print("❌ Render CLI not found")
        print("   Install: pip install render-cli")
        print("   Then login: render login")
        return False
    
    print(f"✓ Render CLI: {version}")
    
    # Check credentials
    token = os.environ.get("RENDER_API_KEY")
    if not token:
        print("⚠️  RENDER_API_KEY not set")
        print("   Get token from: https://dashboard.render.com/u/settings")
        print("   Or use 'render login' instead")
        return False
    
    print(f"✓ Token found: {token[:20]}...")
    
    # Deploy
    print("\n🚀 Deploying to Render...")
    
    deploy_script = Path(__file__).parent / "deploy_render.sh"
    if deploy_script.exists():
        result = subprocess.run(
            ["bash", str(deploy_script)],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    
    print("❌ deploy_render.sh not found")
    return False

if __name__ == "__main__":
    success = deploy_to_render()
    sys.exit(0 if success else 1)
