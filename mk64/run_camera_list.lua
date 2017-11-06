fh,err = io.open("mk64_360_data_KD_30fps_angles.txt")
if err then print("OOps"); return; end

local lines = {}

while true do
        line = fh:read()
        if line == nil then break end
        table.insert(lines, line)
        --console.log(line)
end
fh:close()

-- 3C064270  LUI A2
-- 34C60000  ORI A2, A2
-- 08033CCC J
-- 00000000 NOP
mainmemory.write_u32_be(0x500000, 0x3C064270)
mainmemory.write_u32_be(0x500004, 0x34C60000)
mainmemory.write_u32_be(0x500008, 0x08033CCC)
mainmemory.write_u32_be(0x50000C, 0)

-- 3C064270  LUI A2
-- 34C60000  ORI A2, A2
-- 08033C40 J


for k, line in pairs(lines) do
  -- Get the data to use
  coord = {}
  for word in string.gmatch(line, '([^,]+)') do
      --console.log(word)
      table.insert(coord, tonumber(word))
  end
  
  console.log("Frame " .. coord[1] .. " image " .. coord[2])
  
  -- Advance to the desired frame
  frame_number = tonumber(coord[1])
  while (emu.framecount() < (frame_number - 1)) do
    emu.frameadvance()
  end
    
  if (emu.framecount() ~= (frame_number - 1)) then
    console.log("ERROR")
    break
  end
  
  -- Save the current state to be restored later
  savestate.saveslot(9)
  
  -- Bizhawk's saved framebuffer is slightly compressed. 
  -- Because we do a visual comparison step later, we need the screenshots to be identical
  -- If the first frame doesn't work, it will look different than the other non-working screenshots due to this compression.
  -- I believe that loading the state then immediately loading it again will load that frame buffer on screen to be screenshotted like the later screenshots.
  savestate.loadslot(9)
  
  -- Ensure the correct directory exists
  os.execute("mkdir M:/N64_360/mk64/images/raw/" .. coord[1])
  
  -- Record what the previous frame looked like, for comparison
  client.screenshot("M:/N64_360/mk64/images/raw/" .. coord[1] .. "/prev_1.png")
  
  emu.frameadvance()
  
  savestate.saveslot(8)
  savestate.loadslot(8)
  -- Record what another previous frame looked like, for comparison
  client.screenshot("M:/N64_360/mk64/images/raw/" .. coord[1] .. "/prev.png")
 
 
 
  
  -- Override assembly instructions to prevent the game from changing our camera numbers
  mainmemory.write_u32_be(0x1e964, 0)
  mainmemory.write_u32_be(0x1e970, 0)
  mainmemory.write_u32_be(0x1e978, 0)
  mainmemory.write_u32_be(0x1e984, 0)
  mainmemory.write_u32_be(0x1e990, 0)
  mainmemory.write_u32_be(0x1e9a0, 0)
  mainmemory.write_u32_be(0x1e840, 0)
  mainmemory.write_u32_be(0x1e848, 0)
  mainmemory.write_u32_be(0x1e854, 0)
  mainmemory.write_u32_be(0x1e85c, 0)
  mainmemory.write_u32_be(0x1e86c, 0)
  mainmemory.write_u32_be(0x1e87c, 0)
  mainmemory.write_u32_be(0x151d8, 0)
  mainmemory.write_u32_be(0x151dc, 0)
  mainmemory.write_u32_be(0x151e4, 0)
  mainmemory.write_u32_be(0x152ac, 0)
  mainmemory.write_u32_be(0x152d4, 0)
  mainmemory.write_u32_be(0x152cc, 0)
  
  -- Override assembly instructions to prevent the game from changing lakitu's position
  mainmemory.write_u32_be(0x7A704, 0)
  mainmemory.write_u32_be(0x7A71C, 0)
  mainmemory.write_u32_be(0x7A774, 0)
  mainmemory.write_u32_be(0x7a464, 0)
  mainmemory.write_u32_be(0x7a468, 0)
  mainmemory.write_u32_be(0x7a46c, 0)
  
  -- Override the FOV
  mainmemory.write_u32_be(0x2a5a54, 0x0C140000)
  
  -- Disable the HUD
  mainmemory.write_u8(0x0DC5B9, 0)
  
  -- Inject new camera values
  mainmemory.writefloat(0x1646F0, coord[3], true)
  mainmemory.writefloat(0x1646F8, coord[4], true)
  mainmemory.writefloat(0x1646F4, coord[5], true)
  
  mainmemory.writefloat(0x1646FC, coord[6], true)
  mainmemory.writefloat(0x164704, coord[7], true)
  mainmemory.writefloat(0x164700, coord[8], true)
  
  mainmemory.writefloat(0x164708, coord[9], true)
  mainmemory.writefloat(0x164710, coord[10], true)
  mainmemory.writefloat(0x16470C, coord[11], true)
  
  -- Inject Lakitu's position
  mainmemory.writefloat(0x165CFC, coord[12], true)
  mainmemory.writefloat(0x165D04, coord[13], true)
  mainmemory.writefloat(0x165D00, coord[14], true)
 
  -- Frame advance
  emu.frameadvance()
  emu.frameadvance()
  client.screenshot("M:/N64_360/mk64/images/raw/" .. coord[1] .. "/" .. coord[2] .. "_0.png")
  
  emu.frameadvance()
  client.screenshot("M:/N64_360/mk64/images/raw/" .. coord[1] .. "/" .. coord[2] .. "_1.png")

  -- load state
  savestate.loadslot(9)
end