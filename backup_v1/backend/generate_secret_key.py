#!/usr/bin/env python3
"""
Generate a secure secret key for Flask application.
Usage: python generate_secret_key.py
"""

import secrets

# Generate a secure random key (32 bytes = 64 hex characters)
secret_key = secrets.token_hex(32)

print("=" * 60)
print("Flask Secret Key Generated")
print("=" * 60)
print(f"\nSECRET_KEY={secret_key}\n")
print("=" * 60)
print("\nCopy the SECRET_KEY value above to your .env file")
print("Example:")
print("  SECRET_KEY=" + secret_key)
print("=" * 60)

