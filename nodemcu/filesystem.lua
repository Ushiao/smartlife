-- file system


-- list all files
function list()
    l = file.list();
    for k,v in pairs(l) do
      print("name:"..k..", size:"..v)
    end
end

-- open file in flash:
function read(filename)
    if file.open(filename) then
      print(file.read())
      file.close()
    end
end

read('light.lua')