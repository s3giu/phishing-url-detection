@echo off
setlocal
cd /d "%~dp0"

echo ======================================================
echo SPRINT 4: Generate features CSV + PNG plots + push to GitHub
echo Repo: %cd%
echo ======================================================

if not exist "data\processed" mkdir "data\processed"

echo.
echo [1/3] Building feature matrix CSV...
python "src\features\build_features_sprint4.py"
if errorlevel 1 goto :error

echo.
echo [2/3] Generating plots (from 100k sample)...
python "src\features\plot_features_sprint4.py"
if errorlevel 1 goto :error

echo.
echo [3/3] Git add + commit + push (scripts + PNGs)...
git status

REM Stage Sprint 4 code + plots (CSV excluded by default)
git add git add "src\features\lexical_features.py" ^
        "src\features\build_features_sprint4.py" ^
        "src\features\plot_features_sprint4.py" ^
        "run_sprint4.bat" ^
        "data\processed\features_sprint4.csv" ^
        "data\processed\04_feature_distributions.png" ^
        "data\processed\05_feature_correlation.png"

REM Optional: also stage __init__.py if you created them
if exist "src\__init__.py" git add "src\__init__.py"
if exist "src\features\__init__.py" git add "src\features\__init__.py"

git commit -m "Sprint 4: lexical features + plots"
REM If there is nothing new to commit, commit will fail; that's OK.
git push origin main
if errorlevel 1 goto :error

echo.
echo ======================================================
echo DONE.
echo Outputs:
echo - data\processed\features_sprint4.csv
echo - data\processed\04_feature_distributions.png
echo - data\processed\05_feature_correlation.png
echo Repo pushed to origin/main.
echo ======================================================
echo.
pause
exit /b 0

:error
echo.
echo ======================================================
echo ERROR: Sprint 4 batch run failed.
echo Check the error message above.
echo ======================================================
echo.
pause
exit /b 1
