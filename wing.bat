@echo off
title Wing
SET file=%~dpnx1
pushd %~dp0
python src/wing.py %file%
popd
@echo on