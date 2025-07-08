import uuid

# Dictionary mapping color names to RGB values
COLORS = {
    "red": (1.0, 0.6, 0.6),
    "green": (0.6, 1.0, 0.6),
    "yellow": (1.0, 1.0, 0.6),
    "cyan": (0.6, 1.0, 1.0),
    "magenta": (1.0, 0.6, 1.0),
    "orange": (1.0, 0.6, 0.6),
    "white": (1.0, 1.0, 1.0),
    "pink": (1.0, 0.6, 0.8),
    "blue": (0.6, 0.6, 1.0),
    "purple": (0.8, 0.6, 1.0),
    "lime": (0.6, 1.0, 0.8),
    "teal": (0.6, 1.0, 0.8)
}


def generate_files(input_file):
    vhs_text = ""
    lua_table = ""

    with open(input_file, "r") as file:
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
            elif "=" in line:
                color_name, text = line.split("=")
                color_name = color_name.strip()
                text = text.strip()

                if color_name in COLORS:
                    color = COLORS[color_name]
                    lines_data.append({"color": color, "text": text})

        # Generate vhs_text and lua_table
        for line_data in lines_data:
            guid = str(uuid.uuid4())
            color = line_data["color"]
            text = line_data["text"]
            r, g, b = color
            vhs_text += f'RM_{guid} = "{text}"\n'
            lua_table += f'{{ text = "RM_{guid}", r = {r}, g = {g}, b = {b}, codes = "BOR-1" }},\n'

        # Generate lua_table.txt
        with open("MyVHSTape.lua", "w") as file_lua_table:
            file_lua_table.write("-- Generated Recorded Media Data File\n")
            file_lua_table.write("RecMedia = RecMedia or {}\n\n")
            guid = str(uuid.uuid4())
            item_display_name_guid = str(uuid.uuid4())
            title_guid = str(uuid.uuid4())
            subtitle_guid = str(uuid.uuid4())
            author_guid = str(uuid.uuid4())
            extra_guid = str(uuid.uuid4())
            file_lua_table.write(f'RecMedia["{guid}"] = {{\n')
            file_lua_table.write(f'\titemDisplayName = "RM_{item_display_name_guid}",\n')
            file_lua_table.write(f'\ttitle = "RM_{title_guid}",\n')
            if subtitle:
                file_lua_table.write(f'\tsubtitle = "RM_{subtitle_guid}",\n')
            else:
                file_lua_table.write(f'\tsubtitle = nil,\n')
            file_lua_table.write(f'\tauthor = "RM_{author_guid}",\n')
            file_lua_table.write(f'\textra = "RM_{extra_guid}",\n')
            file_lua_table.write('\tspawning = 0,\n')
            file_lua_table.write(f'\tcategory = "{category}",\n')
            file_lua_table.write("\tlines = {\n")
            file_lua_table.write(lua_table)
            file_lua_table.write("\t},\n")
            file_lua_table.write("};\n")

        # Generate vhs_text.txt
        with open("Recorded_Media_EN.txt", "w") as file_vhs_text:
            file_vhs_text.write("\n")  # Line break at the start
            file_vhs_text.write(vhs_text)
            file_vhs_text.write(f'RM_{item_display_name_guid} = "{item_display_name}"\n')
            file_vhs_text.write(f'RM_{title_guid} = "{title}"\n')
            if subtitle:
                file_vhs_text.write(f'RM_{subtitle_guid} = "{subtitle}"\n')
            file_vhs_text.write(f'RM_{author_guid} = "{author}"\n')
            file_vhs_text.write(f'RM_{extra_guid} = "{extra}"\n')

    print("Files generated successfully.")


# Example usage
input_file = "input.txt"  # Replace with your input file name
generate_files(input_file)