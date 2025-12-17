-- ============================================
-- HohoV2 - Полностью чистая версия БЕЗ KEY системы
-- ============================================

local game = game
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local HttpService = game:GetService("HttpService")
local StarterGui = game:GetService("StarterGui")

repeat task.wait() until game:IsLoaded() and Players.LocalPlayer

-- Таблица с ссылками на скрипты по GameId
local GameScripts = {
    -- Blox Fruit
    [94732206] = "https://raw.githubusercontent.com/kests1111/heraai/main/bloxfruit.lua",
    [2753915549] = "https://raw.githubusercontent.com/kests1111/heraai/main/bloxfruit.lua",
    
    -- Pet Simulator X
    [2316994223] = "https://raw.githubusercontent.com/acsu123/HohoV2/Free/PetSimXFree.lua",
}

-- Функция для безопасной загрузки скрипта
local function LoadScript(url)
    local success, result = pcall(function()
        return game:HttpGet(url)
    end)
    
    if not success then
        print("Failed to fetch: " .. url)
        print("Error: " .. tostring(result))
        return nil
    end
    
    return result
end

-- Функция для инжекта скрипта
local function InjectScript(code)
    if not code then return false end
    
    local success, result = pcall(function()
        loadstring(code)()
    end)
    
    if not success then
        print("Failed to execute script")
        print("Error: " .. tostring(result))
        return false
    end
    
    return true
end

-- Получаем GameId текущей игры
local GameId = game.GameId

-- Проверяем есть ли скрипт для этой игры
if GameScripts[GameId] then
    print("HohoV2: Loading script for GameId " .. GameId)
    
    StarterGui:SetCore("SendNotification", {
        Title = "HohoV2 Loader",
        Text = "Загрузка скрипта для этой игры...",
        Icon = "rbxassetid://16276677105",
        Duration = 2
    })
    
    local scriptUrl = GameScripts[GameId]
    local scriptCode = LoadScript(scriptUrl)
    
    if scriptCode then
        if InjectScript(scriptCode) then
            StarterGui:SetCore("SendNotification", {
                Title = "✓ Success",
                Text = "Скрипт успешно загружен!",
                Icon = "rbxassetid://16276677105",
                Duration = 3
            })
        else
            StarterGui:SetCore("SendNotification", {
                Title = "✗ Error",
                Text = "Ошибка при загрузке скрипта",
                Icon = "rbxassetid://16276677105",
                Duration = 3
            })
        end
    else
        StarterGui:SetCore("SendNotification", {
            Title = "✗ Download Error",
            Text = "Не удалось загрузить скрипт с GitHub",
            Icon = "rbxassetid://16276677105",
            Duration = 3
        })
    end
else
    print("HohoV2: Game " .. GameId .. " is not supported yet")
    
    StarterGui:SetCore("SendNotification", {
        Title = "HohoV2",
        Text = "Эта игра пока не поддерживается (GameId: " .. GameId .. ")",
        Icon = "rbxassetid://16276677105",
        Duration = 3
    })
end
