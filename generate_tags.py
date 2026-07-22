# -*- coding : utf-8 -*-
import json, os, sys, util

# 加载配置
build_config = util.load_config(f"config{os.sep}build.json")
MINECRAFT_PACK_ROOT = build_config.get("pack_root", os.getenv('MINECRAFT_PACK_ROOT'))
MINECRAFT_SPYGLASSMC_ROOT = build_config.get("spyglassmc_root", os.getenv('MINECRAFT_SPYGLASSMC_ROOT'))
if build_config.get("rebuild_cache"):
    version_info = util.build_version_info(f"{MINECRAFT_SPYGLASSMC_ROOT}{os.sep}versions{os.sep}versions.json")
else:
    version_info = json.load(open(build_config['version_info_path'])) if os.path.exists(build_config['version_info_path']) else \
        util.build_version_info(f"{MINECRAFT_SPYGLASSMC_ROOT}{os.sep}versions.json")

def load_json(version: str):
    return json.load(open(os.path.expandvars(f"{MINECRAFT_SPYGLASSMC_ROOT}{os.sep}versions{os.sep}{version}{os.sep}registries.json")))

def getit(version: str, path: str, file: str):
    if version_info[version]['data_pack_version'] < 15:
        raise util.VersionIsOldError(f"{version} 数据包版本低于 15！")
    if not os.path.exists(f"{MINECRAFT_SPYGLASSMC_ROOT}{os.sep}versions{os.sep}{version}"):
        raise util.VersionNotDownloadError(f"未下载 {version} 的内容！")
    if os.path.isfile(f"{MINECRAFT_SPYGLASSMC_ROOT}{os.sep}versions{os.sep}{version}"):
        raise util.IsAFileError(f"{MINECRAFT_SPYGLASSMC_ROOT}{os.sep}versions{os.sep}{version} 是文件！")
    a = load_json(version)[path]
    if version_info[version]['data_pack_version'] < 43:
        path = path.replace('item', 'items').replace('block', 'blocks').replace('entity_type', 'entity_types')
    in_pack_dir = f"{MINECRAFT_PACK_ROOT}{os.sep}{version.replace('.', '_')}{os.sep}data{os.sep}common{os.sep}tags{os.sep}{path}"
    os.makedirs(in_pack_dir, exist_ok = True)
    b = {"values": []}
    for i in a:
        b["values"].append(f"minecraft:{i}")
    json.dump(b, open(f"{in_pack_dir}{os.sep}{file}.json", "w"), sort_keys = False, indent = 4, ensure_ascii = False)
    return

def get_biomes(version: str):
    getit(version, "worldgen/biome", "vanilla_all_biomes")
    return

def get_blocks(version: str):
    getit(version, "block", "vanilla_all_blocks")
    return

def get_damage_types(version: str):
    getit(version, "damage_type", "vanilla_all_damage_types")
    return

def get_enchantments(version: str):
    if version_info[version]['data_pack_version'] < 39:
        raise ValueError(f"{version} 没有魔咒标签！")
    getit(version, "enchantment", "vanilla_all_enchantments")
    return

def get_entity_types(version: str):
    getit(version, "entity_type", "vanilla_all_entity_types")
    return

def get_items(version: str):
    getit(version, "item", "vanilla_all_items")
    return

def get_potion(version: str):
    if version_info[version]['data_pack_version'] < 95:
        raise ValueError(f"{version} 没有药水效果标签！")
    getit(version, "potion", "vanilla_all_potions")
    return

def get_structures(version: str):
    getit(version, "worldgen/structure", "vanilla_all_structures")
    return

def getall(version: str):
    for i in [get_biomes, get_blocks, get_damage_types, get_enchantments, get_entity_types, get_items, get_potion, get_structures]:
        try:
            i(version)
        except ValueError:
            continue

def generate_tags(version_or_file: str | list):
    """生成基本标签。供其它模块或程序使用。"""
    if type(version_or_file) == str:
        if os.path.isfile(version_or_file) and os.path.dirname(version_or_file):
            for i in open(sys.argv[1]):
                getall(i.replace('\n', ''))
        else:
            getall(version_or_file)
    elif type(version_or_file) == list:
        for i in version_or_file:
            getall(i)
    else:
        raise TypeError("传入的参数不是字符串或列表类型！")

if __name__ == '__main__':
    if MINECRAFT_SPYGLASSMC_ROOT == "":
        print(f"未设置 SpyglassMC 的路径！build_tags.py 需要这个路径来获取注册表信息！", file = sys.stderr)
        exit(1)
    if MINECRAFT_PACK_ROOT == None:
        print(f"未指定数据包 pack 存放的位置！build_tags.py 需要指定数据包存放的位置来构建基本标签！", file = sys.stderr)
        exit(1)
    if len(sys.argv) != 2:
        print("用法：build_tags.py <version or version list>")
        exit(0)
    try:
        if os.path.isdir(f"{MINECRAFT_SPYGLASSMC_ROOT}{os.sep}versions{os.sep}{sys.argv[1]}"):
            getall(sys.argv[1])
        elif os.path.isfile(sys.argv[1]):
            for i in open(sys.argv[1]):
                getall(i.replace('\n', ''))
    except:
        pass
    exit(0)
