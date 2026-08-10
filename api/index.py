"""Vercel serverless entrypoint for the Flask application."""

import os
import sys

# Repository root is one directory above /api.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("VERCEL", "1")

from app import app  # noqa: E402

# Vercel's Python runtime looks for a WSGI application named `app`.
