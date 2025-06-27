_default:
  just --choose

webhost:
  .venv/bin/python WebHost.py

launcher:
  .venv/bin/python Launcher.py

generate:
  .venv/bin/python Generate.py
