while true do

  emu.frameadvance()

  local handle = io.open("mk64_360_data_KD.txt", "a");

  CameraX=mainmemory.readfloat(0x1646F0, true)
  CameraY=mainmemory.readfloat(0x1646F8, true)
  CameraZ=mainmemory.readfloat(0x1646F4, true)
  
  lookX=mainmemory.readfloat(0x1646FC, true)
  lookY=mainmemory.readfloat(0x164704, true)
  lookZ=mainmemory.readfloat(0x164700, true)
  
  upX=mainmemory.readfloat(0x164708, true)
  upY=mainmemory.readfloat(0x164710, true)
  upZ=mainmemory.readfloat(0x16470C, true)
  
  lakituX=mainmemory.readfloat(0x165CFC, true)
  lakituY=mainmemory.readfloat(0x165D04, true)
  lakituZ=mainmemory.readfloat(0x165D00, true)
  
  handle:write(emu.framecount() - 1)
  handle:write(",")
  handle:write(CameraX)
  handle:write(",")
  handle:write(CameraY)
  handle:write(",")
  handle:write(CameraZ)
  handle:write(",")
  handle:write(lookX)
  handle:write(",")
  handle:write(lookY)
  handle:write(",")
  handle:write(lookZ)
  handle:write(",")
  handle:write(upX)
  handle:write(",")
  handle:write(upY)
  handle:write(",")
  handle:write(upZ)
  handle:write(",")
  handle:write(lakituX)
  handle:write(",")
  handle:write(lakituY)
  handle:write(",")
  handle:write(lakituZ)
  
  handle:write("\n")
  handle:close();

end