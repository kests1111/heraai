-- HHHUB BYPASS - Обходит luamor проверку ключа
-- Работает для любых скриптов с luamor защитой

local Players = game:GetService("Players")
local StarterGui = game:GetService("StarterGui")
local HttpService = game:GetService("HttpService")

repeat task.wait() until game:IsLoaded() and Players.LocalPlayer

-- ЭТАП 1: Перехватываем httpget на уровне userdata
local originalHttpGet = game:FindService("HttpService").GetAsync

function game:HttpGet(url, ...)
    -- Перехватываем проверку ключей
    if string.find(url, "linkvertise") or string.find(url, "key") or string.find(url, "verify") then
        return HttpService:JSONEncode({
            code = "KEY_VALID",
            message = "Valid",
            valid = true
        })
    end
    
    -- Для обычных запросов используем оригинальную функцию
    local success, result = pcall(function()
        return originalHttpGet(HttpService, url, ...)
    end)
    
    return success and result or ""
end

-- ЭТАП 2: Устанавливаем переменные ДО загрузки
_G.script_key = "free_key_"..tostring(os.time())
_G.MY_KEY_IS = "free_key_"..tostring(os.time())
_G.KEY = "free_key_"..tostring(os.time())
_G.key = "free_key_"..tostring(os.time())

getgenv().script_key = _G.script_key
getgenv().MY_KEY_IS = _G.MY_KEY_IS

-- Сохраняем ключ в файл если возможно
pcall(function()
    if writefile then
        writefile("HohoKeyV4.txt", _G.script_key)
    end
end)

wait(0.3)

StarterGui:SetCore("SendNotification",{
    Title = "Script Loading",
    Text = "Загрузка hhhub без ключа...",
    Icon = "rbxassetid://16276677105"
})

wait(0.5)

-- ЭТАП 3: Загружаем hhhub с перехватом ошибок
local success, result = pcall(function()
    loadstring(game:HttpGet("https://raw.githubusercontent.com/kests1111/heraai/main/hhhub.lua"))()
end)

if success then
    StarterGui:SetCore("SendNotification",{
        Title = "✓ Success",
        Text = "HHHUB успешно загружен!",
        Icon = "rbxassetid://16276677105"
    })
else
    StarterGui:SetCore("SendNotification",{
        Title = "✗ Error",
        Text = tostring(result):sub(1, 50),
        Icon = "rbxassetid://16276677105"
    })
    print("HHHUB BYPASS ERROR: "..tostring(result))
end
