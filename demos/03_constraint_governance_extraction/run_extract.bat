@echo off
REM Usage:
REM   run_extract.bat input_file
REM   run_extract.bat input_file cleaned_output_name.json
REM Always saves BOTH raw and cleaned outputs into .\outputs\ with a timestamp.

set "BASE=%~dp0"
set "INPUT=%~1"
set "OUTNAME=%~2"

if "%INPUT%"=="" set "INPUT=input_trophy.txt"

REM Ensure outputs folder exists
if not exist "%BASE%outputs" mkdir "%BASE%outputs"

REM Timestamp (locale-dependent, but good enough for filenames)
set "TS=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TS=%TS: =0%"

REM Default cleaned output name if not provided
if "%OUTNAME%"=="" set "OUTNAME=cleaned_%~n1_%TS%.json"

REM Raw output name always unique
set "RAWNAME=raw_%~n1_%TS%.txt"

REM Build prompt temp file
type "%BASE%extractor_prompt.txt" > "%BASE%_prompt_tmp.txt"
type "%BASE%%INPUT%" >> "%BASE%_prompt_tmp.txt"

REM Run model -> save raw
type "%BASE%_prompt_tmp.txt" | ollama run mistral > "%BASE%outputs\%RAWNAME%"

REM Clean -> save cleaned
type "%BASE%outputs\%RAWNAME%" | python "%BASE%clean_extract.py" "%INPUT%" > "%BASE%outputs\%OUTNAME%"

del "%BASE%_prompt_tmp.txt"

echo ---
echo Input : %INPUT%
echo Raw   : outputs\%RAWNAME%
echo Clean : outputs\%OUTNAME%
echo ---
echo To open RAW output:
echo notepad "%BASE%outputs\%RAWNAME%"
echo.
echo To open CLEANED output:
echo notepad "%BASE%outputs\%OUTNAME%"
echo ---
