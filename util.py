import json, os, os.path, string, sys, time

__all__ = [
    # 函数
    'build_default_config', 'build_version_info', 'load_config', 'validating_pack',
    # 异常
    'SpyglassMCError', 'VersionNotDownloadError', 'MinecraftPackError', 'InvalidCharactersError', 'IsAFileError', 'MissingRequiredFliedError', 'VersionIsOldError',
    # 常量
    'PACK_MCMETA'
]

PACK_MCMETA = 'pack.mcmeta'

class LOGGER():
    """简易的日志记录器。"""
    def __init__(self, log: bool, log_file: str = None, log_level: str = "error"):
        self.log = log
        self.log_level = log_level
        if log_file:
            if not os.path.exists(os.path.dirname(log_file)):
                os.makedirs(os.path.dirname(log_file), exist_ok = True)
            self.log_file = open(log_file, "a+", encoding = "utf-8")
        else:
            self.log_file = sys.stderr

    def info(self, msg):
        if self.log:
            if self.log_level in ['info', 'warn', 'error', 'debug']:
                print(f"{time.strftime('[%Y-%m-%d] [%H:%M:%S]')} [INFO] {msg}", file = self.log_file)

    def warn(self, msg):
        if self.log:
            if self.log_level in ['warn', 'error', 'debug']:
                print(f"{time.strftime('[%Y-%m-%d] [%H:%M:%S]')} [WARN] {msg}", file = self.log_file)

    def error(self, msg):
        if self.log:
            if self.log_level in ['error', 'debug']:
                print(f"{time.strftime('[%Y-%m-%d] [%H:%M:%S]')} [ERROR] {msg}", file = self.log_file)

    def debug(self, msg):
        if self.log:
            if self.log_level in ['debug']:
                print(f"{time.strftime('[%Y-%m-%d] [%H:%M:%S]')} [DEBUG] {msg}", file = self.log_file)

class SpyglassMCError(Exception):
    """SpyglassMC 错误的基类。"""
    pass

class VersionNotDownloadError(SpyglassMCError):
    """SpyglassMC 中不存在该版本（通常是未下载对应版本的文件）的错误。"""
    def __init__(self, message):
        self.message = message
        super(VersionNotDownloadError, self).__init__(self.message)

class MinecraftPackError(Exception):
    """数据包错误的基类。"""
    pass

class InvalidCharactersError(MinecraftPackError):
    """存在非法字符的错误。"""
    def __init__(self, message):
        self.message = message
        super(InvalidCharactersError, self).__init__(self.message)

class IsAFileError(OSError):
    """目标是文件的错误。"""
    def __init__(self, message):
        self.message = message
        super(IsAFileError, self).__init__(self.message)

class MissingRequiredFliedError(MinecraftPackError):
    """数据包缺失关键字段的错误。"""
    def __init__(self, message):
        self.message = message
        super(MissingRequiredFliedError, self).__init__(self.message)

class VersionIsOldError(MinecraftPackError):
    """游戏版本低于 23w18a。当前还不支持为低于 23w18a 的版本构建。"""
    def __init__(self, message):
        self.message = message
        super(VersionIsOldError, self).__init__(self.message)

def build_version_info(versions_json: str, directly_output: bool = False, output_path: str = f"cache{os.sep}version_info.json") -> dict | None:
    r'''构建版本信息。版本信息会包含版本 ID 和其数据版本、数据包版本和资源包版本。

    参数：

    versions_json: 从 SpyglassMC 下载的 versions.json 的文件路径。

    output_path: 版本信息输出到的路径。默认为 build/version_info.json。仅当 directly_output 为 True 时生效。

    directly_output: 是否直接输出版本信息。如果为 False，则返回版本信息以供脚本和模块使用，否则输出到 output_path 指定的路径。'''
    version_info = {}
    for version in reversed(json.load(open(versions_json))):
        version_info[version['id']] = {
            "data_version": version['data_version'],
            "data_pack_version": version['data_pack_version'],
            "data_pack_version_minor": version['data_pack_version_minor'],
            "resource_pack_version": version['resource_pack_version'],
            "resource_pack_version_minor": version['resource_pack_version_minor']
        }
    if directly_output:
        if os.path.dirname(output_path):
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path), exist_ok = True)
        dump_json(version_info, output_path)
    else:
        return version_info

def build_default_config(config_path):
    config = {
        "$schema": "../schema/config.schema.json",
        "rebuild_cache": False,
        "spyglassmc_root": os.getenv("MINECRAFT_SPYGLASSMC_ROOT"),
        "version_info_path": f"config{os.sep}version_info.json",
        "pack_root": os.getenv("MINECRAFT_PACK_ROOT"),
        "output_dir": "output"
    }
    dump_json(config, config_path, "w", encoding = "utf-8")
    return config

def dump_json(obj, path):
    json.dump(obj, open(path, "w", encoding = "utf-8"), sort_keys = False, indent = 4, ensure_ascii = False)

def generate_version_list(start: str, end: str, version_info: dict) -> list:
    if version_info[start]['data_pack_version'] < 15:
        raise ValueError(f"开始版本 {start} 小于 23w18a！")
    if version_info[end]['data_pack_version'] < 15:
        raise ValueError(f"结束版本 {end} 小于 23w18a！")
    versions = list(version_info.keys())
    return versions[versions.index(start):versions.index(end) + 1]

def generate_all_versions_list(version_info: dict) -> list:
    versions = list(version_info.keys())
    return versions[versions.index("23w18a"):]

def load_config(config_path: str) -> dict:
    """加载构建配置。

    参数：

    config_path: 配置文件的路径

    返回：

    配置文件中的配置

    当配置文件解码错误时，会重建默认配置并返回；当找不到文件或者为目录时会引发 OSError 异常。"""
    if os.path.exists(config_path):
        try:
            config = json.load(open(config_path, encoding = "utf-8"))
        except json.JSONDecodeError:
            return build_default_config(config_path)
        except OSError as e:
            raise e
        else:
            return config
    else:
        return build_default_config(config_path)

def validating_pack(pack_path: str):
    """验证是否是有效的数据包。"""
    if not os.path.exists(pack_path):
        raise OSError(f"找不到数据包 {pack_path}！")
    elif os.path.isfile(pack_path):
        raise IsAFileError(f"数据包 {pack_path} 是文件！")
    elif not os.path.exists(f"{pack_path}{os.sep}{PACK_MCMETA}"):
        raise OSError(f"找不到数据包 {pack_path} 的元信息文件！")
    else:
        try:
            pack_meta = json.load(open(f"{pack_path}{os.sep}pack.mcmeta", encoding = "utf-8"))
        except json.JSONDecodeError:
            raise json.JSONDecodeError("无效的元信息文件！")
        # {}
        if type(pack_meta) != dict:
            raise TypeError(f"数据包 {pack_path} 的元信息不是对象格式！")
        # {}, but missing "pack"
        if pack_meta.get("pack") == None:
            raise MissingRequiredFliedError(f'数据包 {pack_path} 缺少必须字段 pack！')
        # {"pack": {}}
        if type(pack_meta["pack"]) != dict:
            raise TypeError(f"数据包 {pack_path} 的 pack 字段不是对象格式！")
        # {"pack": {}}, but missing "description"
        if pack_meta["pack"].get("description") == None:
            raise MissingRequiredFliedError(f'数据包 {pack_path} 的 pack 字段缺少必须字段 description！')
        # {"pack": {"description": text_component}}, text_component: "" | {} | []
        if type(pack_meta["pack"]["description"]) not in [str, dict, list]:
            raise TypeError(f"数据包 {pack_path} 的描述不是文本组件！")
        if pack_meta.get("overlays"):
            # {"overlays": {}}
            if type(pack_meta["overlays"]) != dict:
                raise TypeError(f"数据包 {pack_path} 的 overlays 字段不是对象格式！")
            # {"overlays": {}}, but missing "entries"
            if pack_meta["overlays"].get("entries") == None:
                raise MissingRequiredFliedError(f'数据包 {pack_path} 的 overlays 字段缺少必须字段 entries！')
            # {"overlays": {"entries": []}}
            if type(pack_meta["overlays"]["entries"]) != list:
                raise TypeError(f"数据包 {pack_path} 中 overlays 的 entries 字段不是列表格式！")
            for overlay in pack_meta["overlays"]["entries"]:
                # {"overlays": {"entries": [{}]}}
                if type(overlay) != dict:
                    raise TypeError(f"覆盖对象 {overlay} 不是对象格式！")
                # {"overlays": {"entries": [{}]}}, but missing "directory" in "$.overlays.entries[*]"
                if overlay.get("directory") == None:
                    raise MissingRequiredFliedError(f"覆盖对象 {overlay} 缺少 directory 字段！")
                # {"overlays": {"entries": [{"directory": ""}]}}
                if type(overlay["directory"]) != str:
                    raise TypeError(f"覆盖对象 {overlay} 的 directory 字段不是字符串格式！")
                # {"overlays": {"entries": [{"directory": "abcdefghijklmnopqrstuvwxyz0123456789-_"}]}}
                for char in overlay["directory"]:
                    if char not in ''.join([string.ascii_lowercase, string.digits, '_', '-']):
                        raise InvalidCharactersError(f"叠加目录 {overlay['directory']} 存在非法字符！")
