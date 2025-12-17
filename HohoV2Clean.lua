-- ============================================
-- HohoV2 - Оригинальный Game Check + БЕЗ KEY системы
-- ============================================

local GameId = game.GameId
local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local HttpService = game:GetService("HttpService")
local TeleportService = game:GetService("TeleportService")
local CoreGui = game:GetService("CoreGui")
local Debris = game:GetService("Debris")
local StarterGui = game:GetService("StarterGui")
local ContentProvider = game:GetService("ContentProvider")

repeat task.wait() until game:IsLoaded() and Players.LocalPlayer

plr = Players.LocalPlayer

local isSupport = nil
local GameList = {
    [994732206] = "e4aedc7ccd2bacd83555baa884f3d4b1", -- Blox Fruit
    [7018190066] = "bf149e75708e91ad902bd72e408fae02", -- Dead Rails
    [383310974] = "b83e9255dc81e9392da975a89d26e363", -- Adopt Me
    [4777817887] = "35ad587b07c00b82c218fcf0e55eeea6", -- Blade Ball
    [5477548919] = "0a9bfef9eb03d0cb17dd85451e4be696", -- Honkai Star Rail Simulator
    [5750914919] = "b94343ca266a778e5da8d72e92d4aab5", -- Fisch
    [3359505957] = "095fbd843016a7af1d3a9ee88714c64a", -- Collect All Pets
    [6167925365] = "e220573a9f986e150c6af8d4d1fb9b7c", -- Cong Dong Viet Nam
    [5361032378] = "ff4e04500b94246eaa3f5c5be92a8b4a", -- Sol's RNG
    [7709344486] = "1d5eea7e66ccb5ca4d11c26ff2d4c6b1", -- Steal a Brainrot
    [7326934954] = "0aa67223637322085cfeaf80ae9af69f", -- 99 Nights in the Forest
    [3149100453] = "dbe59157859f6030587fd61ad4faad75", -- Eat Blob Simulator
    [5995470825] = "83363ffca1175ef0c06d4028b77061a4", -- Hypershot
    [358276974] = "23e50d188c7e27477a1c6eacb076e2ba", -- Apocalypse Rising 2
    [7541395924] = "c924e9543f9651c9cc1afabfe1f3de65", -- Build An Island
    [6701277882] = "1c48d56d18692670e5278e1df94997d8", -- Fish It
    [953622098] = "12933a8f18ec406f1ee26bbdc3b73abf", -- Word Bomb
    [7200297228] = "da7549d939f1a496dca0b8d3610196b5", -- Loot Hero
    [7832036655] = "456662bcac892ece28c0062bbe1a7a66", -- Arena Of Blox
    [7061783500] = "2fb6765dd4c0e2894dd107dd9e14c340", -- 2 Player Battle Tycoon
}

-- Проверяем поддерживается ли игра
if GameList[GameId] then
    isSupport = true
else
    isSupport = false
end

-- ============================================
-- ОБХОД KEY СИСТЕМЫ
-- ============================================

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

-- ============================================
-- ЗАГРУЗКА СКРИПТА
-- ============================================

if isSupport then
    StarterGui:SetCore("SendNotification", {
        Title = "HohoV2 Script Loader",
        Text = "Загрузка скрипта для: " .. GameId,
        Icon = "rbxassetid://16276677105",
        Duration = 2
    })
    
    wait(0.5)
    
    local success, err = pcall(function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/kests1111/heraai/main/hhhub.lua"))()
    end)
    
    if success then
        wait(0.5)
        StarterGui:SetCore("SendNotification", {
            Title = "✓ Loaded Successfully",
            Text = "Скрипт готов к использованию!",
            Icon = "rbxassetid://16276677105",
            Duration = 3
        })
        print("[HohoV2] Скрипт успешно загружен!")
    else
        print("[HohoV2] Error: " .. tostring(err))
        StarterGui:SetCore("SendNotification", {
            Title = "✗ Load Error",
            Text = "Ошибка: " .. tostring(err):sub(1, 40),
            Icon = "rbxassetid://16276677105",
            Duration = 5
        })
    end
else
    StarterGui:SetCore("SendNotification", {
        Title = "⚠ Game Not Supported",
        Text = "Эта игра пока не поддерживается",
        Icon = "rbxassetid://16276677105",
        Duration = 3
    })
    print("[HohoV2] Game ID " .. GameId .. " is not supported")
end
