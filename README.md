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
1. Set up Port Forwarding if necessary
2. Configure the server parameters, such as what types of syncing you would want(several variables), the port number(25565 by default), and the number of players(NUM_CONNECTIONS).
3. Configure client parameters, such as the server's IP and port number.
4. Run the server
5. For every player:
   -Run Project64
   -Launch B3313
   -After choosing your save file, navigate to File->Lua Scripts
   -Choose Client.lua and press Run
6. Enjoy!

## To do
- Properly sync the count of stars/red stars/green stars in RAM (Currently only updates when stars are collected on the receiving end, aka only EEPROM is modified)
- Draw other players as particles
