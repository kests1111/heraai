-- ПРЯМАЯ ЗАГРУЗКА БЕЗ СИСТЕМЫ КЛЮЧЕЙ
-- Убирает весь UI и сразу загружает скрипт

local GameId = game.GameId
local Players = game:GetService("Players")
local StarterGui = game:GetService("StarterGui")

repeat task.wait() until game:IsLoaded() and Players.LocalPlayer

plr = Players.LocalPlayer

-- Сразу загружаем основной скрипт без всяких проверок
local function loadScript()
    StarterGui:SetCore("SendNotification",{
        Title = "Loading...",
        Text = "Скрипт загружается, жди...",
        Icon = "rbxassetid://16276677105"
    })
    
    wait(1)
    
    -- Загружаем твой скрипт напрямую
    pcall(function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/kests1111/heraai/main/hhhub.lua"))()
    end)
end

-- Запускаем загрузку
loadScript()
