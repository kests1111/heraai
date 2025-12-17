-- УНИВЕРСАЛЬНЫЙ ОБХОД LUAMOR - ВСТРОЕННАЯ ВЕРСИЯ
-- Сразу запускает hhhub без необходимости в переменных окружения

local Players = game:GetService("Players")
local StarterGui = game:GetService("StarterGui")
local HttpService = game:GetService("HttpService")

repeat task.wait() until game:IsLoaded() and Players.LocalPlayer

-- Перехватываем HttpGet ДО загрузки скрипта
local oldHttpGet = game.HttpGet
game.HttpGet = function(self, url, ...)
    -- Перехватываем запросы к luamor API
    if string.find(url, "sdkapi") or string.find(url, "check_key") or string.find(url, "luarmor") then
        return HttpService:JSONEncode({
            code = "KEY_VALID",
            message = "Valid",
            data = { note = "Valid" }
        })
    end
    -- Для остальных запросов используем оригинальную функцию
    return oldHttpGet(self, url, ...)
end

-- Устанавливаем переменные на случай если скрипт их проверяет
_G.script_key = "bypass_key_12345"
_G.MY_KEY_IS = "bypass_key_12345"
getgenv().script_key = "bypass_key_12345"

pcall(function()
    if writefile then
        writefile("HohoKeyV4.txt", "bypass_key_12345")
    end
end)

wait(0.3)

StarterGui:SetCore("SendNotification",{
    Title = "Loading...",
    Text = "Загрузка скрипта...",
    Icon = "rbxassetid://16276677105"
})

wait(0.7)

-- Загружаем hhhub
pcall(function()
    loadstring(game:HttpGet("https://raw.githubusercontent.com/kests1111/heraai/main/hhhub.lua"))()
end)
