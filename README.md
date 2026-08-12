# B3313-Multiplayer
B3313 (SM64 ROM hack), but Multiplayer!
This project is Windows/WINE only!

## Features
- Health Link
- Lives Link
- Death Link

## Initial Setup Guide
1. Put Client.lua in the "scripts" folder of Project64-EM
2. That's kind of it!

## Running Guide
1. Configure the server parameters, such as what types of syncing you would want(several variables), the port number(25565 by default), and the number of players(NUM_CONNECTIONS).
2. Run the server
3. For every player:
4.   Run Project64
5.   After choosing your save file, navigate to File->Lua Scripts
6.   Choose Client.lua and press Run
7. Enjoy!

## To do
- Properly sync the count of stars/red stars/green stars in RAM (Currently only updates when stars are collected on the receiving end, aka only EEPROM is modified)
- Draw other players as particles
