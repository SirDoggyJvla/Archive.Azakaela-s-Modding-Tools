"""
AzakaelasDistributionMaker.exe
    SHA256 53B552AD0C91F617355EC3CBC6F2E27845E179574AB5E58B8BC1B0AD4EA9672A
File main.pyc (main.py)
    Python 3.11.7
    Bytecode version 3495
Decompiled and edited by aoqia
"""

import json
import re
import tkinter as tk
from tkinter import filedialog, ttk

container_list = []
procedural_container_list = []
procedural_container_list_lower = []
items = []


def add_item():
    item_frame = ttk.Frame(items_frame)
    item_frame.pack(pady=10)
    item_full_name_entry = ttk.Entry(item_frame, width=30)
    item_full_name_entry.grid(row=0, column=0, padx=5)
    all_containers_button = ttk.Button(item_frame, text="+ All Containers",
                                       command=lambda: add_container(item_frame, all_containers=True))
    all_containers_button.grid(row=0, column=1, padx=5)
    procedural_containers_button = ttk.Button(
        item_frame, text="+ Procedural Containers", command=lambda: add_container(item_frame, all_containers=False))
    procedural_containers_button.grid(row=0, column=2, padx=5)
    delete_button = ttk.Button(item_frame, text="Delete", command=lambda: delete_item(item_frame))
    delete_button.grid(row=0, column=3, padx=5)
    containers = []
    items.append((item_frame, item_full_name_entry, containers,
                 all_containers_button, procedural_containers_button, delete_button))


def add_container(item_frame, all_containers=True):
    item = next((item for item in items if item[0] == item_frame), None)
    if item:
        container_frame = ttk.Frame(item[0])
        container_frame.grid(row=len(item[2]) + 2, column=0, columnspan=3, pady=5)
        container_combobox = ttk.Combobox(container_frame)
        container_combobox.grid(row=0, column=0, padx=5)
        container_combobox["values"] = container_list if all_containers else procedural_container_list
        container_combobox.current(0)
        chance_entry = ttk.Entry(container_frame, width=10)
        chance_entry.grid(row=0, column=1, padx=5)
        item[2].append((container_combobox, chance_entry))


def delete_item(item_frame):
    item = next((item for item in items if item[0] == item_frame), None)
    if item:
        items.remove(item)
        item_frame.destroy()


def save_data():
    filename = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON Files", "*.json")])
    if filename:
        data = []

        for item in items:
            item_full_name = item[1].get()
            all_containers = item[2]

            containers = []
            for container in all_containers:
                container_name = container[0].get()
                chance = container[1].get()
                containers.append({"container_name": container_name, "chance": chance})
            data.append({"item_full_name": item_full_name, "containers": containers})
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file)
            print("Data saved successfully.")


def open_data():
    filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if len(filename) == 0:
        return

    clear_items()
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

        for item_data in data:
            item_frame = ttk.Frame(items_frame)
            item_frame.pack(pady=10)
            item_full_name_entry = ttk.Entry(item_frame, width=30)
            item_full_name_entry.grid(row=0, column=0, padx=5)
            item_full_name_entry.insert(tk.END, item_data["item_full_name"])
            all_containers_button = ttk.Button(item_frame, text="+ All Containers",
                                               command=lambda: add_container(item_frame, all_containers=True))
            all_containers_button.grid(row=0, column=1, padx=5)
            procedural_containers_button = ttk.Button(
                item_frame, text="+ Procedural Containers", command=lambda: add_container(item_frame, all_containers=False))
            procedural_containers_button.grid(row=0, column=2, padx=5)
            delete_button = ttk.Button(item_frame, text="Delete", command=lambda: delete_item(item_frame))
            delete_button.grid(row=0, column=3, padx=5)

            containers = []
            for container_data in item_data["containers"]:
                container_frame = ttk.Frame(item_frame)
                container_frame.grid(row=len(containers) + 2, column=0, columnspan=3, pady=5)
                container_combobox = ttk.Combobox(container_frame)
                container_combobox.grid(row=0, column=0, padx=5)

                container_combobox["values"] = container_list \
                    if container_data["container_name"].lower() in procedural_container_list_lower \
                    else procedural_container_list

                container_combobox.set(container_data["container_name"])
                chance_entry = ttk.Entry(container_frame, width=10)
                chance_entry.grid(row=0, column=1, padx=5)
                chance_entry.insert(tk.END, container_data["chance"])
                containers.append((container_combobox, chance_entry))
            items.append((item_frame, item_full_name_entry, containers,
                          all_containers_button, procedural_containers_button, delete_button))
    update_scrollable_region()


def clear_items():
    for item in items:
        item[0].destroy()
    items.clear()
    update_scrollable_region()


def update_scrollable_region():
    canvas.configure(scrollregion=canvas.bbox("all"))


def import_from_script(items_frame):
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if len(filename) == 0:
        return

    with open(filename, "r", encoding="utf-8") as file:
        script_data = file.read()

    module_name_match = re.search("module\\s+(\\w+)", script_data)
    module_name = module_name_match.group(1) if module_name_match else ""

    item_pattern = "item\\s+(\\w+)"
    item_names = re.findall(item_pattern, script_data)
    for item_name in item_names:
        add_item()
        item = items[-1]
        item[1].insert(tk.END, f"{module_name}.{item_name}")

        container_pattern = "container\\s+(\\w+)"
        container_matches = re.findall(container_pattern, script_data)
        for container_name in container_matches:
            add_container(item[0], all_containers=True)
            container_item = item[2][-1]
            container_item[0].set(container_name)
    print("Items added from script:")

    for item in items:
        print(item[1].get())
    update_scrollable_region()


def generate_lua_file():
    lua_code = \
        """
-- Start of automatically generated distribution file.

--[[

Automatically generated distribution file!
Tool created by Azakaela! THE GODDESS OF SECRETS MWAHAHAH UWU

Thanks for the tool Azakaela! Notes from aoqia:
I decompiled this tool from the original exe file as
    the source code for some of the programs were not available.
This tool is mostly legacy now, and you should instead be using for loops
    to loop over tables containing your containers/items stuff.
If you need help with that, check out the pzwiki page (under "A better way to handle this..."):
    https://pzwiki.net/wiki/Procedural_distributions#How_to_add_your_own_items_to_distributions
    or ask in the Project Zomboid Modding Community Discord server.

--]]

require(\"Items/SuburbsDistributions\")
require(\"Items/ProceduralDistributions\")


"""

    for item in items:
        item_full_name = item[1].get()
        all_containers = item[2]

        for container in all_containers:
            container_name = str(container[0].get())
            chance = str(container[1].get())

            if container_name.lower() in procedural_container_list_lower:
                lua_code +=  f"""
table.insert(ProceduralDistributions.list[\"{container_name}\"].items, \"{item_full_name}\")
table.insert(ProceduralDistributions.list[\"{container_name}\"].items, {chance})

"""
            else:
                lua_code += f"""
table.insert(SuburbsDistributions[\"all\"][\"{container_name}\"].items, \"{item_full_name}\")
table.insert(SuburbsDistributions[\"all\"][\"{container_name}\"].items, {chance})

"""

    with open("output.lua", "w", encoding="utf-8") as lua_file:
        lua_file.write(lua_code)
        lua_file.write("-- End of generated file.\n")

    print("Lua file generated successfully.")


def main():
    with open("all_containers", "r", encoding="utf-8") as container_file:
        for line in container_file:
            container_list.append(line.strip())

    with open("procedural_containers", "r", encoding="utf-8") as procedural_file:
        for line in procedural_file:
            container_name = line.strip()
            procedural_container_list.append(container_name)
            procedural_container_list_lower.append(container_name.lower())

    root.mainloop()


root = tk.Tk()
root.title("Azakaela's Distribution Generator")

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save", command=save_data)
file_menu.add_command(label="Save As", command=save_data)
file_menu.add_command(label="Open", command=open_data)
menu_bar.add_cascade(label="File", menu=file_menu)
items_menu = tk.Menu(menu_bar, tearoff=0)
items_menu.add_command(label="Import from script", command=lambda: import_from_script(items_frame))
menu_bar.add_cascade(label="Items", menu=items_menu)
root.config(menu=menu_bar)

controls_frame = ttk.Frame(root)
controls_frame.pack(pady=10)
add_item_button = ttk.Button(controls_frame, text="+ Add Item", command=add_item)
add_item_button.pack(side=tk.LEFT)
generate_button = ttk.Button(controls_frame, text="Generate Lua File!", command=generate_lua_file)
generate_button.pack(side=tk.LEFT, padx=10)

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
items_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=items_frame, anchor=tk.NW)


if __name__ == "__main__":
    main()
