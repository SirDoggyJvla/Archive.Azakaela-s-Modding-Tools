"""
Azakaelas Recorded Media Maker.exe
    SHA256 CA708E90251D7B81FC543FCAF81CDC43FBC16A8CDA1F465482F83BA6FF4EAAF3
File main.pyc (main.py)
    Python 3.11.7
    Bytecode version 3495
Decompiled and edited by aoqia
"""

import uuid

COLORS = {
    "white": (1.0, 1.0, 1.0),
    "red": (1.0, 0.6, 0.6),
    "orange": (1.0, 0.6, 0.6),
    "yellow": (1.0, 1.0, 0.6),
    "lime": (0.6, 1.0, 0.8),
    "green": (0.6, 1.0, 0.6),
    "teal": (0.6, 1.0, 0.8),
    "cyan": (0.6, 1.0, 1.0),
    "blue": (0.6, 0.6, 1.0),
    "purple": (0.8, 0.6, 1.0),
    "magenta": (1.0, 0.6, 1.0),
    "pink": (1.0, 0.6, 0.8),
}


def generate_files(input_file):
    vhs_text = ""
    lua_table = ""

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        item_display_name = ""
        title = ""
        subtitle = None
        author = ""
        extra = ""
        category = ""
        lines_data = []

        for line in lines:
            line = line.strip()

            if line.startswith("displayname="):
                item_display_name = line.split("= ")[1]
            elif line.startswith("title="):
                title = line.split("= ")[1]
            elif line.startswith("subtitle="):
                subtitle = line.split("= ")[1]
            elif line.startswith("author="):
                author = line.split("= ")[1]
            elif line.startswith("extra="):
                extra = line.split("= ")[1]
            elif line.startswith("category="):
                category = line.split("= ")[1]
            else:
                if "=" in line:
                    color_name, text = line.split("=")
                    color_name = color_name.strip()
                    text = text.strip()
                    if color_name in COLORS:
                        color = COLORS[color_name]
                        lines_data.append({"color": color, "text": text})

        for line_data in lines_data:
            guid = str(uuid.uuid4())
            color = line_data["color"]
            text = line_data["text"]
            r, g, b = color
            vhs_text += f"RM_{guid} = \"{text}\"\n"
            lua_table += f"{{ text = \"RM_{guid}\", r = {r}, g = {g}, b = {b}, codes = \"BOR-1\" }},\n"

        with open("MyVHSTape.lua", "w", encoding="utf-8") as file_lua_table:
            guid = str(uuid.uuid4())
            item_display_name_guid = str(uuid.uuid4())
            title_guid = str(uuid.uuid4())
            subtitle_guid = str(uuid.uuid4())
            author_guid = str(uuid.uuid4())
            extra_guid = str(uuid.uuid4())

            file_lua_table.write("-- Generated Recorded Media Data File\n")
            file_lua_table.write("RecMedia = RecMedia or {}\n\n")
            file_lua_table.write(f"RecMedia[\"{guid}\"] = {{\n")
            file_lua_table.write(f"\titemDisplayName = \"RM_{item_display_name_guid}\",\n")
            file_lua_table.write(f"\ttitle = \"RM_{title_guid}\",\n")

            if subtitle:
                file_lua_table.write(f"\tsubtitle = \"RM_{subtitle_guid}\",\n")
            else:
                file_lua_table.write("\tsubtitle = nil,\n")

            file_lua_table.write(f"\tauthor = \"RM_{author_guid}\",\n")
            file_lua_table.write(f"\textra = \"RM_{extra_guid}\",\n")
            file_lua_table.write("\tspawning = 0,\n")
            file_lua_table.write(f"\tcategory = \"{category}\",\n")
            file_lua_table.write("\tlines = {\n")
            file_lua_table.write(lua_table)
            file_lua_table.write("\t},\n")
            file_lua_table.write("};\n")

        with open("Recorded_Media_EN.txt", "w", encoding="utf-8") as file_vhs_text:
            file_vhs_text.write("\n")
            file_vhs_text.write(vhs_text)
            file_vhs_text.write(f"RM_{item_display_name_guid} = \"{item_display_name}\"\n")
            file_vhs_text.write(f"RM_{title_guid} = \"{title}\"\n")

            if subtitle:
                file_vhs_text.write(f"RM_{subtitle_guid} = \"{subtitle}\"\n")

            file_vhs_text.write(f"RM_{author_guid} = \"{author}\"\n")
            file_vhs_text.write(f"RM_{extra_guid} = \"{extra}\"\n")

    print("Files generated successfully.")


def main():
    generate_files("input.txt")


if __name__ == "__main__":
    main()
