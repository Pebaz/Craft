@echo off
title Wing
SET file=%~dpnx1
python src/wing.py %file%
@echo on