-- HohoV2 Advanced Bypass v2
-- Перехватываем luamor декодер и функции проверки

local Players = game:GetService("Players")
local StarterGui = game:GetService("StarterGui")
local HttpService = game:GetService("HttpService")

repeat task.wait() until game:IsLoaded() and Players.LocalPlayer

-- ЭТАП 1: Перехватываем loadstring ДО загрузки скрипта
local originalLoadstring = loadstring
local bypassedLoadstring = function(source, env)
    if type(source) == "string" then
        -- Если это луамор обфусцированный код - подменяем проверку ключа
        source = source:gsub("local%s+key%s*=%s*[\"'].-[\"']", "local key = 'bypass_key'")
        source = source:gsub("if%s+key%s*~=%s*[\"'].-[\"']", "if false")
        source = source:gsub("KEY_VALID", "true")
        source = source:gsub("Invalid%s+Key", "Valid Key")
    end
    return originalLoadstring(source, env or getfenv(2))
end

-- Переопределяем loadstring
loadstring = bypassedLoadstring
_G.loadstring = bypassedLoadstring

-- ЭТАП 2: Устанавливаем переменные
_G.HohoKey = "bypass"
_G.HOHO_KEY = "bypass"
_G.MY_KEY_IS = "bypass"
_G.Script_Key = "bypass"
_G.KEY = "bypass"
_G.key = "bypass"

-- Подменяем require для перехвата модулей
local originalRequire = require
_G.require = function(mod)
    local result = originalRequire(mod)
    if type(result) == "table" then
        result.key = "bypass"
        result.KEY = "bypass"
    end
    return result
end

wait(0.3)

StarterGui:SetCore("SendNotification",{
    Title = "HohoV2 Loader",
    Text = "Инициализация байпасса...",
    Icon = "rbxassetid://16276677105"
})

wait(0.5)

-- ЭТАП 3: Загружаем скрипт с перехватом
local success, err = pcall(function()
    local scriptData = game:HttpGet("https://raw.githubusercontent.com/acsu123/HOHO_H/main/Loading_UI")
    
    -- Проходим скрипт и убираем проверки ключа
    scriptData = scriptData:gsub("tonumber%(KEY%)", "1")
    scriptData = scriptData:gsub("KEY%s*==%s*nil", "false")
    scriptData = scriptData:gsub("check%-key", "check_bypass")
    
    originalLoadstring(scriptData)()
end)

if success then
    wait(1)
    StarterGui:SetCore("SendNotification",{
        Title = "Success! ✓",
        Text = "HohoV2 загружен без ключа!",
        Icon = "rbxassetid://16276677105"
    })
else
    print("Bypass Error: " .. tostring(err))
    StarterGui:SetCore("SendNotification",{
        Title = "Error",
        Text = tostring(err):sub(1, 50),
        Icon = "rbxassetid://16276677105"
    })
end
