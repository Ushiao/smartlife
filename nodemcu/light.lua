-- file: light.lua
local module = {}
function module.start()  

--[[
D0 = 1
D1 = 2
D2 = 3
D3 = 4
CH_1 = 5
CH_2 = 6
CH_3 = 7
CH_4 = 8
]]
gpio_map = {1,2,3,4,5,6,7,8}
gpio_map_rf = {1,2,3,4}
gpio_map_wifi = {5,6,7,8}

for idx=1, #gpio_map do
    pin = gpio_map[idx]
    gpio.mode(pin, gpio.OUTPUT)
end
last_wifi_time = 0
last_rf_time = 0

url = 'http://服务器地址/smartlife/static/light.html'
tmr.alarm(0, 1000, 1, function ()
    http.get(url, nil, function(code, data)
        if (code < 0) then
          print("HTTP request failed")
        else
            dt = sjson.decode(data)
            for k, v in pairs(dt) do 
                if k == "rf" then
                    part_data = v[1]
                    part_time = tonumber(v[2])
                    if last_rf_time == 0 then
                        last_rf_time = part_time
                    else
                        if part_time > last_rf_time then
                            for mode_idx=1, #part_data do
                                mode = part_data[mode_idx]
                                for idx=1,4 do
                                    v = string.sub(mode, idx,idx)
                                    gpio.write(gpio_map_rf[idx], tonumber(v))
                                end
                                tmr.delay(600000)
                                for idx=1,4 do
                                    gpio.write(gpio_map_rf[idx], 0)
                                end
                                tmr.delay(300000)
                            end
                            last_rf_time = part_time
                        end
                    end
                elseif k == "wifi" then
                    part_data = v[1]
                    part_time = tonumber(v[2])
                    if last_wifi_time == 0 then
                        last_wifi_time = part_time
                    else
                        if part_time > last_wifi_time then
                            for idx=1,4 do
                                v = string.sub(part_data, idx,idx)
                                gpio.write(gpio_map_wifi[idx], tonumber(v))
                            end
                            last_wifi_time = part_time
                        end
                    end
                end
            end             
        end
    end)
end)
end
return module  
