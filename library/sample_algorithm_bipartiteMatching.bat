@echo off
set local
set pythonpath=%pythonpath%;.
python -m algorithm.bipartiteMatching
endlocal
pause
