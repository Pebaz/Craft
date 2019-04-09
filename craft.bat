@echo off
title Craft
SET file=%~dpnx1
pushd %~dp0
python src/craft.py %file%
popd
@echo on