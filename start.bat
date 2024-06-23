@echo off
del out.json
del pos.json
python scraper.py
python convert.py
pause