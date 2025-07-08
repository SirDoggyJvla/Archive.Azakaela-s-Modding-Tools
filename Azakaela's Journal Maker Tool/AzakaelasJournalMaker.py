"""
AzakaelasJournalMaker.exe
    SHA256 B5CFDAAA89D5FD8DBCA4ED5E5DCF9A9FF5F0492C7626F6352639604523682F20
File main.pyc (main.py)
    Python 3.11.7
    Bytecode version 3495
Decompiled and edited by aoqia
"""

import os


def generate_journal_item_script(journal_name):
    return f"""module Journals
{{
    item {journal_name}
    {{
        DisplayCategory = Literature,
        Weight = 0.1,
        Type = Literature,
        DisplayName = {journal_name},
        Icon = Notebook,
        StaticModel = Newspaper,
        WorldStaticModel = Newspaper_Ground,
    }}
}}
"""


def generate_lua_file(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        journal_name = None
        page_texts = []

        for line in input_file:
            line = line.strip()
            if not line:
                continue

            if line.startswith("JournalName="):
                journal_name = line.split("=")[1].strip()
            elif line.startswith('pg'):
                page_texts.append(line.split('=')[1].strip())

    lua_code = f"""UIDisplayJournal_{journal_name} = {{}}

local currentPage = 1
local journalPages = {{
{"".join(f"    \"{text}\",\n" for text in page_texts)}
}}

local UI

function UIDisplayJournal_{journal_name}.createMenu(_player, _context, _items)
    local playerObj = getSpecificPlayer(_player)
    local items = ISInventoryPane.getActualItems(_items)
    for _, item in ipairs(items) do
        if item:getFullType() == "Journals.{journal_name or "\" then"}
            _context:addOption("Read Journal", _items, UIDisplayJournal_{journal_name or ".onDisplayJournal, playerObj, item)"}
        end
    end
end

function UIDisplayJournal_{journal_name}.onDisplayJournal(items, playerObj, item)
    if UI then
        UI:close()
    end

    UI = NewUI()

    local totalPages = {str(len(page_texts))}
    
    UI:setWidthPercent(0.3)
    UI:addText("pageNumber", "Page " .. currentPage .. " of " .. totalPages, "Small", "Center")
    UI:nextLine()

    UI:setLineHeightPercent(0.6);
    UI:addRichText("pageText", "<SIZE:medium>" .. journalPages[currentPage])
    UI:nextLine()

    UI:addEntry("pageNumberEntry", "", true)
    UI["pageNumberEntry"]:setEnterFunc(UIDisplayJournal_{journal_name or ".onPageNumberEntered)"}
    UI["pageNumberEntry"]:addArg("totalPages", totalPages)

    UI:addButton("previousButton", "Previous Page", UIDisplayJournal_{journal_name or ".onPreviousPageClicked, {totalPages = totalPages}"})
    UI:addButton("nextButton", "Next Page", UIDisplayJournal_{journal_name or ".onNextPageClicked, {totalPages = totalPages}"})

    UI:saveLayout()
end

function UIDisplayJournal_{journal_name}.onPageNumberEntered(entry, text, args)
    local pageNumber = tonumber(text)
    local totalPages = args.totalPages

    if pageNumber and pageNumber >= 1 and pageNumber <= totalPages then
        currentPage = pageNumber
        UIDisplayJournal_{journal_name or ".onDisplayJournal()"}
    end
end

function UIDisplayJournal_{journal_name}.onPreviousPageClicked(button)
    currentPage = currentPage - 1
    if currentPage < 1 then
        currentPage = 1
    end
    UIDisplayJournal_{journal_name or ".onDisplayJournal()"}
end

function UIDisplayJournal_{journal_name}.onNextPageClicked(button)
    currentPage = currentPage + 1
    local totalPages = {str(len(page_texts))}
    if currentPage > totalPages then
        currentPage = totalPages
    end
    UIDisplayJournal_{journal_name or '.onDisplayJournal()'}
end

Events.OnFillInventoryObjectContextMenu.Add(UIDisplayJournal_{journal_name}.createMenu)
"""

    lua_dir = os.path.dirname(os.path.abspath(output_file_path))

    os.makedirs(lua_dir, exist_ok=True)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(lua_code)

    journal_script_path = f"media/scripts/{journal_name}.txt"
    journal_dir = os.path.dirname(os.path.abspath(journal_script_path))
    os.makedirs(journal_dir, exist_ok=True)

    with open(journal_script_path, "w", encoding="utf-8") as output_file:
        output_file.write(generate_journal_item_script(journal_name))

    print(f"Lua file and journal script have been generated: {output_file_path}, {journal_script_path}")


def main():
    input_file_path = "input.txt"
    journal_name = None

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        for line in input_file:
            line = line.strip()
            if line.startswith("JournalName="):
                journal_name = line.split("=")[1].strip()
                break

    if not journal_name:
        print("Journal name not found in the input file.")
        return

    output_file_path = f"media/lua/client/{journal_name}.lua"
    generate_lua_file(input_file_path, output_file_path)
    print(f"Lua file and journal script have been generated: {output_file_path}, media/scripts/{journal_name}.txt")


if __name__ == "__main__":
    main()
