# B3313-Multiplayer
B3313 (SM64 ROM hack), but Multiplayer!
This project is Windows/WINE only!

## Features
- Health Link
- Lives Link
- Death Link
- Live Star Syncing

## Initial Setup Guide
1. For every player, put Client.lua in the "scripts" folder of Project64-EM
3. For the server host, configure port forwarding if necessary
4. That's kind of it!

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

## Disclaimers
I will not provide a ROM for B3313; you have to find that yourself. On top of that, this project could be very easily adapted to work with multiple ROM hacks, so look out for that in the future.
Your progress is not stored in any way on the server. If you quit the client without saving, you still lose all of your progress.
Following from that, players who are not on the server will not have the progress they missed stored unless they connect to the server last, so the server sees other people's progress as an update.
## To do
- Draw other players as particles
- Model other players?
