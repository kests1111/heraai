-- HohoV2 Bypass - Simple Version
-- Запускает HohoV2/Loading_UI без необходимости в ключе

local Players = game:GetService("Players")
local StarterGui = game:GetService("StarterGui")
local HttpService = game:GetService("HttpService")

repeat task.wait() until game:IsLoaded() and Players.LocalPlayer

-- Устанавливаем фейк-ключ ПЕРЕД загрузкой скрипта
_G.HohoKey = "bypass_free_key_"..tostring(os.time())
_G.HOHO_KEY = "bypass_free_key_"..tostring(os.time())
_G.MY_KEY_IS = "bypass_free_key_"..tostring(os.time())
_G.Script_Key = "bypass_free_key_"..tostring(os.time())

getgenv().HohoKey = _G.HohoKey
getgenv().HOHO_KEY = _G.HOHO_KEY
getgenv().MY_KEY_IS = _G.MY_KEY_IS
getgenv().Script_Key = _G.Script_Key

-- Подменяем функцию для проверки ключа (если она существует)
local oldHttpGet = game.HttpGet
game.HttpGet = function(self, url, ...)
    -- Перехватываем Linkvertise проверку
    if string.find(url, "linkvertise") or string.find(url, "key") or string.find(url, "verify") then
        return HttpService:JSONEncode({code = 200, success = true, valid = true})
    end
    -- Для остальных запросов используем оригинальную функцию
    return oldHttpGet(self, url, ...)
end

wait(0.3)

StarterGui:SetCore("SendNotification",{
    Title = "HohoV2 Loader",
    Text = "Загрузка скрипта без ключа...",
    Icon = "rbxassetid://16276677105"
})

wait(0.7)

-- Загружаем основной скрипт HohoV2
local success, err = pcall(function()
    loadstring(game:HttpGet("https://raw.githubusercontent.com/acsu123/HOHO_H/main/Loading_UI"))()
end)

if success then
    StarterGui:SetCore("SendNotification",{
        Title = "Success",
        Text = "Скрипт успешно загружен!",
        Icon = "rbxassetid://16276677105"
    })
else
    StarterGui:SetCore("SendNotification",{
        Title = "Error",
        Text = "Ошибка: "..tostring(err),
        Icon = "rbxassetid://16276677105"
    })
    print("Error: "..tostring(err))
end
