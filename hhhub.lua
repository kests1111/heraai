--=====================================================
--  HoHo Hub Loader (Restored, No Luarmor)
--  Original repo: https://github.com/acsu123/HohoV2
--=====================================================

--// Services
local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")
local TweenService = game:GetService("TweenService")

local LocalPlayer = Players.LocalPlayer

--=====================================================
--  GAME → SCRIPT ROUTING
--=====================================================

local GAME_URLS = {
    -- Blox Fruits
    [994732206] =
        "https://raw.githubusercontent.com/acsu123/HohoV2/main/Main.lua",

    -- если есть другие игры — добавляй так:
    -- [GAME_ID] = "RAW_URL"
}

local GAME_ID = game.GameId
local SCRIPT_URL = GAME_URLS[GAME_ID]

--=====================================================
--  GAME CHECK
--=====================================================

if not SCRIPT_URL then
    warn("[HoHo Hub] This game is not supported.")
    return
end

--=====================================================
--  OPTIONAL INTRO (как в оригинале)
--=====================================================

local ScreenGui = Instance.new("ScreenGui")
ScreenGu
