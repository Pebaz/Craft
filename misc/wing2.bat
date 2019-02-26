@echo off
title Wing
SET file=%~dpnx1
pushd .
cd ../src
python wing.py %file%
popd
@echo on