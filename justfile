_default:
  just --choose

webhost:
  source .venv/bin/activate
  python WebHost.py

launcher:
  source .venv/bin/activate
  python Launcher.py
