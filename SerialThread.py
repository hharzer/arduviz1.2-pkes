##@package SerialThread
# This module provides a thread, for reading and writing data over the serial interface.
#
import threading
import serial
import time
import Queue



## 
# Thread for the Serial Communication, from python client to arduino.
# @param self.InputQueue The InputQueue for raw data.
# @param self.autoreconnect A flag for autoreconnect.
# @param self.connected Saves current connected state.
# @param self.HSstr The Handshakestring.
# @param self.HSnum The hashvalue of the Handshakestring.
# @param self.Connection The connection via the pyserial library.
# @param self.firstselectedport Saves the first selected port.
# @param self.Connection.port The connections' port.
# @param self.baudrate The connections' baudrate.
# @param self.keeprunning flag that allows the ObjectHandler to end the thread, it is checked in the runs' while loop

class SerialCom(threading.Thread):

    lock = threading.Lock()

    ## Construcor of the SerialCom class.
    # Port is the Linux port /dev/ttyACM0 by default.
    #
    def __init__(self,autoreconnect,port="/dev/ttyACM0", baud=9600, Handshakestr="AVH"):
        
        threading.Thread.__init__(self)

        self.InputQueue = Queue.Queue()
        self.autoreconnect = autoreconnect

        self.availableBlocks = 0
        self.connected = False
        self.HSstr = Handshakestr
        self.HSnum = self.hashHS(Handshakestr)
        self.Connection = serial.Serial()
        self.firstselectedport = port
        self.Connection.port = (port) 
        
        self.baudrate = baud

        self.keeprunning = True # flag that allows the object handler to end the thread, it is checked in the runs' while loop
    
    ## Destructor
    # Closing connection and runs the thread deconstructor
    def __del__(self):
        self.closecon()
        threading.Thread.__del__(self)


    ## Starts the 'main loop' of the SerialThread
    # Includes opening of connection, Handshake, switchingPort in case of problems
    # reading and writing bytes to inputqueue
    def run(self):
        connection_tries = 0
        print ">SerialThread started"

        while(not self.connected and self.keeprunning):
            time.sleep(0.5)
           ## print ">Trying to connect to:",self.Connection.port ,"!"
            try:
                self.opencon()
                self.waitHS()

            except Exception as e:

                connection_tries += 1
                if(connection_tries >= 5 and not self.autoreconnect): ## no connection seems possible to this port
                    self.keeprunning = False
                    break 

            # so far so good now endless readbytes
            while(self.connected):
           ##     print ">Connected!"
                try:
                    self.readbytes()
                except Exception, e:
                    time.sleep(0.5)
                    self.reset()
        
        print ">SerialThread ended."
    ##
    # Opens a serial connection.
    #
    def opencon(self):
        self.Connection.open()
        self.Connection.close()
        self.Connection.open()

    ##
    # Closes a serial connection.
    #
    def closecon(self):
        self.Connection.close()

    ##
    # Read infinity amount of bytes
    #
    def readbytes(self):
    	blockprogress = 0
    	# skip remaining AVH's
    	in_byte = self.Connection.read(1)

    	while(in_byte != '#'):
    		in_byte = self.Connection.read(1)
    	blockprogress += 1

    	self.InputQueue.put(in_byte)

        while 1:
            in_byte = self.Connection.read(1)

            if((in_byte == '#') or (in_byte == '+')):
                blockprogress += 1

            if((in_byte != '')):
                self.InputQueue.put(in_byte)

            if(blockprogress == 2):
                self.availableBlocks += 1
                blockprogress = 0

    ##
    # Hashes the handshakestring.
    #
    def hashHS(self,str):
    	x = 0
    	for i in range (0,len(str)):
    		x += ord(str[i])
    	return x

    ##
    # Waits for the handshake.
    # If the handshakestring is received, it is send to the arduino.
    #
    def waitHS(self):
        tries = 0
    	in_bytes = self.Connection.read(3)
    	while(self.hashHS(in_bytes) != self.HSnum):
            tries = tries + 1
            in_bytes = self.Connection.read(3)
            if tries >= 10:
                raise Exception

    	self.Connection.write(self.HSstr)	
    	self.connected = True

    ## Sends a callback, with the related uid.
    # 
    def sendCB(self,*args):
        mes = "!" + str(args[1].Uid)
        print "SENDINGCB: ", mes
        self.Connection.write(mes)

    ## Sends a text with the related uid.
    #  
    def sendTxt(self,*args):
        mes = "?"+ str(args[1].Uid) + args[1].text
        print "SENDINGTXT: ", mes
        self.Connection.write(mes)
    
    ## Resets all connection related member variables.
    # 
    def reset(self):
        self.closecon()
        self.connected = False
        self.InputQueue = Queue.Queue()
        self.availableBlocks = 0

    ## sets 'self.Connection.port', to the wanted.
    # 
    def setport(self,port="/dev/ttyACM0"):
        self.Connection.port = port ##port for actual connection

    ## Switches port automatically.
    # E.g. /dev/ttyACM0 to /dev/ttyACM1.
    # But only in an intern modulo range.
    def switchport(self):
        self.closecon()
        print int(self.firstselectedport[-1])
        print "self.Connection.port:", self.Connection.port
        port = self.Connection.port[:-1] + str(  (int(self.Connection.port[-1]) + 1) % (int(self.firstselectedport[-1])+2) ) 
      ##  self.port = self.port[:-1] + str ( int(self.port[-1] + 1) % 2 )
        print "switchingPort to ", port
        self.setport(port)

    ## Returns the amount of the currently available blocks.
    #
    def get_blockamount(self):
        return self.availableBlocks

    ## Gets the next block from the inputqueue.
    # Sideeffect, deletes the block from queue as well, decrements availableblocks from Serial Com
    def getnextblock(self):
        print ">getnextblock"
        block = []
        startsign = self.InputQueue.get()

        while(startsign != '#' and startsign != '+'): ##delete unwanted before block
            startsign = self.InputQueue.get()

        block.append(startsign) 

        cur = None

        while(self.InputQueue.qsize() > 0): ## startsign == endsign
            cur = self.InputQueue.get()
            block.append(cur)

            if cur == startsign:
                break

        self.availableBlocks = self.availableBlocks - 1
        
        return block