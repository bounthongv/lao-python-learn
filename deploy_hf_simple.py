#!/usr/bin/env python3
"""
Deploy Lao Python Learning Platform to Hugging Face Spaces

Usage:
    export HF_TOKEN="your-token-here"
    python deploy_hf.py
"""

import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_file

SPACE_NAME = "lao-python-learn"
REPO_TYPE = "space"
SDK = "docker"

def check_hf_login(token):
    """Check if we're logged in to Hugging Face"""
    api = HfApi(token=token)
    try:
        user = api.whoami()
        return user['name']
    except Exception as e:
        print(f"Error checking login: {e}")
        return None

def main():
    # Get token from environment
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN environment variable not set")
        print("Get a token from: https://huggingface.co/settings/tokens")
        print("Then run: export HF_TOKEN='your-token-here'")
        sys.exit(1)

    # Check login
    print("Checking Hugging Face login...")
    username = check_hf_login(token)
    if not username:
        print("ERROR: Could not authenticate with Hugging Face")
        sys.exit(1)

    print(f"Logged in as: {username}")

    # Create space repo name
    repo_id = f"{username}/{SPACE_NAME}"
    print(f"Space ID: {repo_id}")

    # Create the repo
    print("\nCreating Hugging Face Space...")
    try:
        create_repo(
            repo_id=repo_id,
            repo_type=REPO_TYPE,
            token=token,
            space_sdk=SDK,
            exist_ok=True,
        )
        print(f"✓ Space created: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print(f"Error creating repo: {e}")
        sys.exit(1)

    # Upload files
    project_dir = Path(__file__).parent
    print("\nUploading files...")

    files_to_upload = [
        "app.py",
        "requirements.txt",
        "README.md",
        "Dockerfile",
        ".gitignore",
    ]

    for filepath in files_to_upload:
        full_path = project_dir / filepath
        if full_path.exists():
            try:
                upload_file(
                    path_or_fileobj=str(full_path),
                    path_in_repo=filepath,
                    repo_id=repo_id,
                    repo_type=REPO_TYPE,
                    token=token,
                )
                print(f"  ✓ {filepath}")
            except Exception as e:
                print(f"  ✗ {filepath}: {e}")
        else:
            print(f"  ⚠ {filepath}: not found")

    print("\n" + "="*50)
    print("✅ Deployment complete!")
    print("="*50)
    print(f"\nYour learning platform is live at:")
    print(f"  https://huggingface.co/spaces/{repo_id}")
    print(f"\nTo update later, just run this script again.")

if __name__ == "__main__":
    main()
