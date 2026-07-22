import os, os.path, util, sys, shutil

from pack_build import *

def build(build_config):
    LOGGER = build_config["LOGGER"]
    shutil.rmtree(build_config['temp_pack_dir'], True)
    if not os.path.exists(build_config["version_info"]):
        LOGGER.warn("版本信息不存在，正在重建……")
        util.build_version_info(f"{build_config['spyglassmc_root']}{os.sep}versions.json", True, build_config["version_info"])
    version_info = util.load_config(build_config["version_info"])
    if build_config["generate_tags"]:
        if type(build_config['minecraft_versions_to_build']) == list:
            LOGGER.info(f"正在生成版本列表。起点：{build_config['minecraft_versions_to_build'][0]}，终点：{build_config['minecraft_versions_to_build'][1]}")
            versions = util.generate_version_list(build_config['minecraft_versions_to_build'][0], build_config['minecraft_versions_to_build'][1], version_info)
        else:
            if build_config['minecraft_versions_to_build'] != 'all':
                versions = build_config['minecraft_versions_to_build']
            else:
                LOGGER.info("正在生成所有版本列表……")
                versions = util.generate_all_versions_list(version_info)
        from generate_tags import generate_tags
        try:
            LOGGER.info("开始生成标签")
            generate_tags(versions)
        except (util.IsAFileError, util.VersionNotDownloadError) as e:
            if build_config["debug"]:
                raise e
            print(e, file = sys.stderr)
            return 2
        except TypeError:
            if build_config["debug"]:
                raise TypeError("构建程序内部错误：参数类型不正确！")
            print("构建程序内部错误：参数类型不正确！", file = sys.stderr)
            return 3
    else:
        match build_config["build_target"]:
            case "standard":
                try:
                    LOGGER.info("开始构建目标 standard……")
                    return build_standard(build_config)
                except NameError:
                    LOGGER.error(f"不存在构建目标 {build_config['build_target']} 的构建程序！")
                    if build_config["debug"]:
                        raise NameError(f"不存在构建目标 {build_config['build_target']} 的构建程序！")
                    print(f"不存在构建目标 {build_config['build_target']} 的构建程序！", file = sys.stderr)
                    return 2
            case "basic_tags":
                try:
                    LOGGER.info("开始构建目标 basic_tags……")
                    return build_basic_tags(build_config)
                except NameError:
                    if build_config["debug"]:
                        raise NameError(f"不存在构建目标 {build_config['build_target']} 的构建程序！")
                    print(f"不存在构建目标 {build_config['build_target']} 的构建程序！", file = sys.stderr)
                    return 2
                except util.IsAFileError:
                    if type(build_config['minecraft_versions_to_build']) == str:
                        if build_config["debug"]:
                            raise util.IsAFileError(f"版本 {build_config['minecraft_versions_to_build']} 是文件！预期是文件夹。")
                        print(f"版本 {build_config['minecraft_versions_to_build']} 是文件！预期是文件夹。", file = sys.stderr)
                        return 2
                except OSError:
                    if type(build_config['minecraft_versions_to_build']) == str:
                        if build_config["debug"]:
                            raise OSError(f"你还未下载版本 {build_config['minecraft_versions_to_build']} 的内容！")
                        print(f"你还未下载版本 {build_config['minecraft_versions_to_build']} 的内容！", file = sys.stderr)
                        return 2
                except TypeError:
                    if build_config["debug"]:
                        raise TypeError("构建程序内部错误：参数类型不正确！")
                    print("构建程序内部错误：参数类型不正确！", file = sys.stderr)
                    return 3
            case _:
                LOGGER.error(f"不存在构建目标 {build_config['build_target']}！")
                if build_config["debug"]:
                    raise ValueError(f"不存在构建目标 {build_config['build_target']}！")
                print(f"不存在构建目标 {build_config['build_target']}！", file = sys.stderr)
                return 2