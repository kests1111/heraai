-- ============================================
-- HohoV2 для Блокс Фрута - БЕЗ KEY системы
-- ============================================

local Players = game:GetService("Players")
local StarterGui = game:GetService("StarterGui")

repeat task.wait() until game:IsLoaded() and Players.LocalPlayer

-- GameIds для Блокс Фрута
local BloxFruitGameIds = {
    [94732206] = true,      -- старая версия
    [2753915549] = true,    -- новая версия
}

local GameId = game.GameId

if not BloxFruitGameIds[GameId] then
    StarterGui:SetCore("SendNotification", {
        Title = "❌ Wrong Game",
        Text = "Это не Блокс Фрут (GameId: " .. GameId .. ")",
        Icon = "rbxassetid://16276677105"
    })
    return
end

-- Полностью отключаем все проверки ключей
_G.script_key = "free_bypass_key"
_G.MY_KEY_IS = "free_bypass_key"
_G.KEY = "free_bypass_key"
_G.key = "free_bypass_key"
_G.HOHO_KEY = "free_bypass_key"

getgenv().script_key = "free_bypass_key"
getgenv().MY_KEY_IS = "free_bypass_key"

pcall(function()
    if writefile then
        writefile("HohoKeyV4.txt", "free_bypass_key")
    end
end)

wait(0.2)

StarterGui:SetCore("SendNotification", {
    Title = "HohoV2 Blox Fruit",
    Text = "Загрузка скрипта...",
    Icon = "rbxassetid://16276677105"
})

wait(0.3)

-- Загружаем hhhub
local success, err = pcall(function()
    loadstring(game:HttpGet("https://raw.githubusercontent.com/kests1111/heraai/main/hhhub.lua"))()
end)

if success then
    wait(0.5)
    StarterGui:SetCore("SendNotification", {
        Title = "✓ Loaded",
        Text = "Скрипт успешно запущен!",
        Icon = "rbxassetid://16276677105",
        Duration = 3
    })
    print("HHHUB для Блокс Фрута загружен!")
else
    print("Error: " .. tostring(err))
    StarterGui:SetCore("SendNotification", {
        Title = "✗ Error",
        Text = "Ошибка: " .. tostring(err):sub(1, 40),
        Icon = "rbxassetid://16276677105",
        Duration = 5
    })
end
