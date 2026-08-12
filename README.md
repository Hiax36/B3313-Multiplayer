# B3313-Multiplayer
B3313 (SM64 ROM hack), but Multiplayer!
This project is Windows/WINE only!

## Features
- Health Link
- Lives Link
- Death Link

## Initial Setup Guide
1. Put Client.lua in the "scripts" folder of Project64-EM
2. Configure Port forwarding if necessary
3. That's kind of it!

## Running Guide
1. Configure the server parameters, such as what types of syncing you would want(several variables), the port number(25565 by default), and the number of players(NUM_CONNECTIONS).
2. Configure client parameters, such as the server's IP and port number.
3. Run the server
4. For every player, do the following:
5.    Run Project64-EM
6.    Open B3313
7.    Select save file 1
8.    Navigate to File -> Lua Scripts
9.    Select Client.lua and select Run
10.    Enjoy!

## To do
- Properly sync the count of stars/red stars/green stars in RAM (Currently only updates when stars are collected on the receiving end, aka only EEPROM is modified)
- Draw other players as particles
