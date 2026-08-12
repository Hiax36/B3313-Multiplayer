local HOST = 'localhost'
local PORT = 25565
local EEPROMOFFSET = 0x80207700
local EEPROMSIZE = 448

function connect()
  s = socket.tcp(HOST, PORT)
  if s == nil then
    print('Failed to connect to ' .. HOST .. ':' .. PORT)
    socket.sleep(1)
    return connect()
  end
  return s
end

local s = connect()

-- Create copy of EEPROM to check for differences
local EEPROMData = {}
for i = 0, EEPROMSIZE, 4 do
  EEPROMData[i/4] = memory.read_u32(EEPROMOFFSET+i)
end


print("Connected to the client at " .. HOST .. ":" .. PORT)

while true do
  local op = binary.unpack_u8(s:recv(1))

  -- MEMREAD_8
  if op == 2 then
    local addr = binary.unpack_u32(s:recv(4))
    local data = memory.read_u8(addr)
    s:send(binary.pack_u8(data))
  end

  -- MEMREAD_16
  if op == 3 then
    local addr = binary.unpack_u32(s:recv(4))
    local data = memory.read_u16(addr)
    s:send(binary.pack_u16(data))
  end

  -- MEMREAD_32
  if op == 4 then
    local addr = binary.unpack_u32(s:recv(4))
    local data = memory.read_u32(addr)
    s:send(binary.pack_u32(data))
  end

  -- MEMWRITE_8
  if op == 6 then
    local addr = binary.unpack_u32(s:recv(4))
    local data = binary.unpack_u8(s:recv(1))
    memory.write_u8(addr, data)
  end

  -- MEMWRITE_16
  if op == 7 then
    local addr = binary.unpack_u32(s:recv(4))
    local data = binary.unpack_u16(s:recv(2))
    memory.write_u16(addr, data)
  end

  -- MEMWRITE_32
  if op == 8 then
    local addr = binary.unpack_u32(s:recv(4))
    local data = binary.unpack_u32(s:recv(4))
    memory.write_u32(addr, data)
  end

  -- CHK_EEPROM
  if op == 9 then
    print("Syncing EEPROM...")
    for i = 0, EEPROMSIZE, 4 do
      local readData = memory.read_u32(EEPROMOFFSET+i)
      if readData ~= EEPROMData[i/4] then
        print("Found EEPROM Difference at " .. EEPROMOFFSET+i)
        s:send(binary.pack_u32(EEPROMOFFSET+i))
        s:send(binary.pack_u32(readData))
        EEPROMData[i/4] = readData
      end
    end
    print("Done reading EEPROM. Sending Finish Signal.")
    s:send(binary.pack_u32(4294967295))
  end
end
