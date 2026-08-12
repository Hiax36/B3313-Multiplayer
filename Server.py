import socket
import os
import time
import traceback
import sys

ENABLE_HEALTHLINK = False
ENABLE_DEATHLINK = False
ENABLE_LIVELINK = False


connections = list()
acceptorSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
acceptorSocket.bind(("0.0.0.0",25565))

def main():
    ### Memory Addresses ###
    livesAddress = 0x8033B21D #8 bit (signed for some reason)
    MarioXAddress = 0x8033B1AC # 32 bit float
    MarioYAddress = 0x8033B1B0 # 32 bit float
    MarioZAddress = 0x8033B1B4 # 32 bit float
    MarioHealthAddress = 0x8033B21E # 2 bytes ish
    starCountAddress = 0x8033B21A # 16 bit
    levelNumberAddress = 0x8032DDF8 # 16 bit
    areaNumberAddress = 0x8033B24A # 8 bit

    ### Acceptor Socket ###
    NUM_CONNECTIONS = 2
    

    print("Listening for Connections...")
    while len(connections) < NUM_CONNECTIONS:
        acceptorSocket.listen()
        connections.append(acceptorSocket.accept())
        print("Client " + str(len(connections)) + " Connected!")
    print("Done Listening For Connections.")



    ### Client Code ###
    
    # Note: All `[::-1]`s are to account for endianness

    ## Current Variables
    currentLives = 0
    currentHealth = 0
    currentStars = 0
    playerPositions = dict()

    while True:
        
        #Get Player Positions
        for conn in connections:
            if not conn[0] in playerPositions.keys():
                playerPositions[conn[0]] = [0,0,0]
            
            #X
            conn[0].send((4).to_bytes(1))
            conn[0].send(MarioXAddress.to_bytes(4)[::-1])
            playerPositions[conn[0]][0] = int.from_bytes(conn[0].recv(4)[::-1],signed=False)

            #Y
            conn[0].send((4).to_bytes(1))
            conn[0].send(MarioYAddress.to_bytes(4)[::-1])
            playerPositions[conn[0]][0] = int.from_bytes(conn[0].recv(4)[::-1],signed=False)

            #Z
            conn[0].send((4).to_bytes(1))
            conn[0].send(MarioZAddress.to_bytes(4)[::-1])
            playerPositions[conn[0]][0] = int.from_bytes(conn[0].recv(4)[::-1],signed=False)
        

        ## Get Level #
        levelNums = dict()
        for conn in connections:
            conn[0].send((3).to_bytes(1))
            conn[0].send(levelNumberAddress.to_bytes(4)[::-1])
            levelNums[conn[0]] = int.from_bytes(conn[0].recv(2)[::-1],signed=False)
        
        
        
        ## Get Area #
        areaNums = dict()
        for conn in connections:
            conn[0].send((2).to_bytes(1))
            conn[0].send(areaNumberAddress.to_bytes(4)[::-1])
            areaNums[conn[0]] = int.from_bytes(conn[0].recv(1),signed=False)

        ## If 2 players in same level & area, write icon to be at that location
        for conn1 in levelNums.keys():
            for conn2 in levelNums.keys():
                if conn1 == conn2:
                    continue
                elif (levelNums[conn1] == levelNums[conn2]) and areaNums[conn1] == areaNums[conn2]:
                    ##TODO: DRAW OTHER PLAYERS
                    pass
        
        ## Stat Syncing
        
        #Sync Lives
        if ENABLE_LIVELINK:
            for conn in connections:
                conn[0].send((2).to_bytes(1))
                conn[0].send(livesAddress.to_bytes(4)[::-1])
                tempLives = int.from_bytes(conn[0].recv(1),signed=True)
                if tempLives != currentLives:
                    print(str(conn[1]) + " Changed Lives to " + str(tempLives))
                    currentLives = tempLives
                    for conn2 in connections:
                        if conn2 != conn:
                            conn2[0].send((6).to_bytes(1))
                            conn2[0].send(livesAddress.to_bytes(4)[::-1])
                            conn2[0].send(currentLives.to_bytes(1))
        
        #Health Link
        if ENABLE_HEALTHLINK or ENABLE_DEATHLINK:
            for conn in connections:
                conn[0].send((2).to_bytes(1))
                conn[0].send(MarioHealthAddress.to_bytes(4)[::-1])
                tempHealth = int.from_bytes(conn[0].recv(1),signed=True)
                if tempHealth != currentHealth:
                    print(str(conn[1]) + " Changed Health to " + str(tempHealth))
                    if ENABLE_HEALTHLINK:
                        currentHealth = tempHealth
                        for conn2 in connections:
                            if conn2 != conn:
                                conn2[0].send((6).to_bytes(1))
                                conn2[0].send(MarioHealthAddress.to_bytes(4)[::-1])
                                conn2[0].send(currentHealth.to_bytes(1))
                    elif ENABLE_DEATHLINK and tempHealth == 0:
                        for conn2 in connections:
                            if conn2 != conn:
                                conn2[0].send((6).to_bytes(1))
                                conn2[0].send(MarioHealthAddress.to_bytes(4)[::-1])
                                conn2[0].send((0).to_bytes(1))


        #Sync Star Counts
        for conn in connections:
            conn[0].send((3).to_bytes(1)[::-1])
            conn[0].send(starCountAddress.to_bytes(4)[::-1])
            tempStars = int.from_bytes(conn[0].recv(2)[::-1],signed=False)
            if tempStars != currentStars:
                print(str(conn[1]) + " Changed Stars to " + str(tempStars))
                currentStars = tempStars
                for conn2 in connections:
                    if conn2 != conn:
                        conn2[0].send((7).to_bytes(1))
                        conn2[0].send(starCountAddress.to_bytes(4)[::-1])
                        conn2[0].send(currentStars.to_bytes(2)[::-1])
        
        #Sync EEPROM Data
        print("Syncing EEPROM")
        for conn in connections:
            conn[0].send((9).to_bytes(1))
            recvAddr = None
            while True:
                recvAddr = int.from_bytes(conn[0].recv(4)[::-1],signed=False)
                if recvAddr == 4294967295:
                    break
                newdata = int.from_bytes(conn[0].recv(4)[::-1],signed=False)
                print("EEPROM Data: " + str(recvAddr) + " : " + str(newdata))
                for conn2 in connections:
                    if conn2 == conn:
                        continue
                    
                    #Note: byte reversal technically not necessary here as values get double reversed
                    conn2[0].send((8).to_bytes(1))
                    conn2[0].send(recvAddr.to_bytes(4)[::-1])
                    conn2[0].send(newdata.to_bytes(4)[::-1])
        print("Done Syncing EEPROM")
                    



    
    



if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        acceptorSocket.close()
        for conn in connections:
            print("Closing Connection to " + str(conn[1]))
            conn[0].close()
        sys.exit()
