"""
AzakaelasAudioLogGenerator.exe
    SHA256 557CBF49F8285421B254112464DE7241CEBAAE267ABBE6DCBF678B4EB741E010
File main.pyc (main.py)
    Python 3.11.7
    Bytecode version 3495
Decompiled and edited by aoqia
"""


def generate_lua_file(mod_name, audio_logs):
    return f"""-- PlaySound will return a number so we store here to stop later
local audio = 0
local updatePosition = false

function {mod_name}_SoundUpdate(player)
    if not updatePosition then return end

    player:getEmitter():setPos(player:getX() + 0.5, player:getY() + 0.5, player:getZ())
    player:getEmitter():tick()
end

function {mod_name}_StopPlayingAudioLog(items, result, player)
    if audio == 0 or not player:getEmitter():isPlaying(audio) then
        return
    end

    updatePosition = false
    player:stopOrTriggerSound(audio)
    Events.OnPlayerUpdate.Remove({mod_name}_SoundUpdate)
end

{
    "".join(f"""
function Play_{log}(items, result, player)
    audio = player:getEmitter():playSound("{log}")
    updatePosition = true
    Events.OnPlayerUpdate.Add({mod_name}_SoundUpdate)
end
""" for i, log in enumerate(audio_logs, start=1))
}
"""


def generate_item_script(mod_name, audio_logs):
    return f"""module {mod_name}
{{
{
    "".join(f"""item {log}
    {{
        Weight = 0.1,
        Type = Normal,
        DisplayName = {log},
        Icon = AudioLog,
        WorldStaticModel = VHSBox,
    }}

    recipe StopPlaying{log}
    {{
        {log},
        Result: {log},
        Category: Leisure,
        OnCreate: {mod_name}_StopPlayingAudioLog,
        RemoveResultItem: false,
    }}

    recipe Play{log}
    {{
        {log},
        Result: {log},
        Category: AudioLog,
        OnCreate: Play_{log},
        RemoveResultItem: false,
        Time: 1,
    }}
    """ for log in audio_logs)
}
}}
"""


def generate_sound_script(mod_name, audio_logs):
    return f"""module {mod_name}
{{
{
    "".join(f"""    sound {log}
    {{
        category = Object,
        clip
        {{
            file = media/sound/{log}.ogg,
            distanceMin = 5,
            distanceMax = 70,
            reverbMaxRange = 10,
            reverbFactor = 0,
            volume = 0.3,
            loop = false,
        }}
    }}
    """ for log in audio_logs)
}
}}
"""


def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    mod_name = None
    audio_logs = []

    for line in lines:
        line = line.strip()

        if line.startswith("ModName="):
            mod_name = line.split("=")[1]
        elif line.startswith("AudioLog"):
            audio_logs.append(line.split("=")[1])

    if not mod_name or not audio_logs:
        print("Invalid input format")
        return

    lua_code = generate_lua_file(mod_name, audio_logs)
    with open("output.lua", "w", encoding="utf-8") as f:
        f.write(lua_code)

    item_script = generate_item_script(mod_name, audio_logs)
    with open("output_item_script.txt", "w", encoding="utf-8") as f:
        f.write(item_script)

    sound_script = generate_sound_script(mod_name, audio_logs)
    with open("output_sound_script.txt", "w", encoding="utf-8") as f:
        f.write(sound_script)
    print("Files generated successfully.")


if __name__ == "__main__":
    main()
