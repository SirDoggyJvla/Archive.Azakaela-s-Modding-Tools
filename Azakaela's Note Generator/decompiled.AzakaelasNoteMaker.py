"""
AzakaelasNoteMaker.exe
    SHA256 ED88D30E5BD7337E5F19D123B832FEAF6AEE3A1CE0E4E394C847A1EA980619E6
File main.pyc (main.py)
    Python 3.11.7
    Bytecode version 3495
Decompiled and edited by aoqia
"""

import os


def generate_lua_file(mod_name, notes):
    return f"""require(\"Maps/ISMapDefinitions\")

local MINZ = 0
local MAXZ = 24

local function overlayPNG(mapUI, x, y, scale, layerName, tex, alpha)
    local texture = getTexture(tex)
    if not texture then return end
    
    local mapAPI = mapUI.javaObject:getAPIv1()
    local styleAPI = mapAPI:getStyleAPI()
    local layer = styleAPI:newTextureLayer(layerName)
    
    layer:setMinZoom(MINZ)
    layer:addFill(MINZ, 255, 255, 255, (alpha or 1.0) * 255)
    layer:addTexture(MINZ, tex)
    layer:setBoundsInSquares(x, y, x + texture:getWidth() * scale, y + texture:getHeight() * scale)
end
{"".join(f"""
local FlyerX{i} = 10
local FlyerY{i} = 10

LootMaps.Init["Note{i}"] = function(mapUI)
    local mapAPI = mapUI.javaObject:getAPIv1()
    MapUtils.initDirectoryMapData(mapUI, "media/maps/Muldraugh, KY")
    mapAPI:setBoundsInSquares(FlyerX{i}, FlyerY{i}, FlyerX{i} + 1, FlyerY{i} + 1)
    overlayPNG(mapUI, FlyerX{i}, FlyerY{i}, 1.0, "lootMapPNG", "media/ui/LootableMaps/{mod_name}_Note{i}.png", 1.0)
end
""" for i, note in enumerate(notes, start=1))}
"""


def generate_script_file(mod_name, notes):
    return f"""module {mod_name}
{{
{"".join(f"""    item Note{i}
    {{
        DisplayCategory = Cartography,
        Type = Map,
        DisplayName = {note},
        Icon = Paper,
        Weight = 0.1,
        Map = Note{i},
        WorldStaticModel = SheetOfPaper,
    }}""" for i, note in enumerate(notes, start=1))}
}}
"""


def generate_note_distributions(mod_name, notes):
    return f"""require("Items/SuburbsDistributions")
require("Items/ProceduralDistributions")

{"".join(f"""table.insert(SuburbsDistributions["all"]["inventorymale"].items, "{mod_name}.Note{i}")
table.insert(SuburbsDistributions["all"]["inventorymale"].items, 0.1)
table.insert(SuburbsDistributions["all"]["inventoryfemale"].items, "{mod_name}.Note{i}")
table.insert(SuburbsDistributions["all"]["inventoryfemale"].items, 0.1)
""" for i, note in enumerate(notes, start=1))}
"""


def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    mod_name = None
    notes = []
    spawn_on_zombies = False

    for line in lines:
        line = line.strip()
        if line.startswith("ModName="):
            mod_name = line.split("=")[1]
        else:  # inserted
            if line.startswith("IWantTheseToSpawnOnZombies="):
                spawn_on_zombies = line.split("=")[1].lower() == "true"
            else:  # inserted
                if line.startswith("Note"):
                    note = line.split("=")[1].strip()
                    notes.append(note)

    if not mod_name or not notes:
        print("Invalid input format")
        return

    lua_code = generate_lua_file(mod_name, notes)
    script_file = generate_script_file(mod_name, notes)
    lua_folder = "media/lua/client/ISUI/Maps"
    os.makedirs(lua_folder, exist_ok=True)
    scripts_folder = "media/scripts"
    os.makedirs(scripts_folder, exist_ok=True)
    lua_file_path = os.path.join(lua_folder, f"{mod_name}_ISMapDefinitions.lua")

    with open(lua_file_path, "w", encoding="utf-8") as f:
        f.write(lua_code)
    print(f"LUA file generated: {lua_file_path}")

    script_file_path = os.path.join(scripts_folder, f"{mod_name}_literature.txt")
    with open(script_file_path, "w", encoding="utf-8") as f:
        f.write(script_file)
    print(f"Script file generated: {script_file_path}")

    if not spawn_on_zombies:
        return

    server_items_folder = "media/lua/server/Items"
    os.makedirs(server_items_folder, exist_ok=True)

    note_distributions_code = generate_note_distributions(mod_name, notes)
    distributions_file_path = os.path.join(server_items_folder, f"{mod_name}_NoteDistributions.lua")
    with open(distributions_file_path, "w", encoding="utf-8") as f:
        f.write(note_distributions_code)
    print(f"Note distributions LUA file generated: {distributions_file_path}")


if __name__ == "__main__":
    main()
