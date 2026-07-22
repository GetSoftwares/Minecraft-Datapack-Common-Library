@echo off
set "MINECRAFT_PROJECT_NAME=Minecraft Datapack Common Library"
title Minecraft Datapack Development Environment - %MINECRAFT_PROJECT_NAME%
cd /d "%~dp0"
chcp 65001>NUL
:: Environments
call set_environments.cmd
:: Start
start /B
