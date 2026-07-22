r'''通用库数据包构建程序，用来实现不同的构建目标。'''

import argparse
import os
import os.path
import sys
import util # 这些程序的通用函数和常量
import _build

# 构建常量
build_prog_name = "build"
build_prog_version = '1.0.0'
build_prog_description = "构建通用库，并可通过选项和配置文件来构建不同目标的通用库。"
build_porg_usage = f'''{build_prog_name} <-? | -v> | [-d] [<日志选项>] <构建目标> [<构建配置>] <面向版本> <构建元信息>'''
build_prog_epilog = f'''\
其他说明
1. build_target 当前可以为 standard 或 basic_tags，但将来会有更多构建目标；
2. 当构建目标为 standard 时，面向版本必须为 -bfav（面向全部版本）。
    standard 为所有其他构建目标和自定义构建的基础，必须保证全版本、全功能、全支持。'''

def build(build_config: dict) -> int:
    config = build_config['config']
    del build_config['config']
    LOGGER = util.LOGGER(build_config['log'], build_config['log_file'], build_config['log_level'])
    del build_config['log']
    del build_config['log_file']
    del build_config['log_level']
    build_config.update({
        "LOGGER": LOGGER,
        "rebuild_cache": build_config["rebuild_cache"] if config == None else config["rebuild_cache"],
        "version_info": build_config["version_info"] if config == None else config["version_info"],
        "spyglassmc_root": build_config["spyglassmc_root"] if config == None else config["spyglassmc_root"],
        "pack_root": build_config["pack_root"] if config == None else config["pack_root"],
        "output_dir": build_config["output_dir"] if config == None else config["output_dir"],
        # "pack_icon": build_config["pack_icon"] if config == None else config["pack_icon"],
    })
    print(build_config['library_version'], file = open(f"{build_config['output_dir']}{os.sep}CURRENT_VERSION", "w"))
    LOGGER.info("开始构建通用库……")
    result = _build.build(build_config)
    LOGGER.info("构建完毕！")
    return result

def main() -> int:
    # 设置参数
    argparser = argparse.ArgumentParser(
        add_help=False, allow_abbrev=False,
        description=build_prog_description,
        epilog=build_prog_epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prefix_chars="/-",
        prog=build_prog_name,
        usage=build_porg_usage
    )
    args_self = argparser.add_argument_group(title="自身参数")
    args_self.add_argument('-?', '-h', '-help', '--help', action='help', help="显示帮助", dest='help')
    args_self.add_argument('-v', '-version', '--version', action='version', help="显示构建程序版本", dest='version', version=build_prog_version)
    args_self.add_argument('-d', '-debug', '--debug', action='store_true', help="调试构建程序", dest='debug')
    args_self.add_argument('-p', '-pa', '-print-args', '--print-args', action='store_true', help="输出选项和参数并退出（仅用于调试）", dest='print_args')
    args_log = argparser.add_argument_group(title="日志选项")
    args_log.add_argument('-l', '-log', '--log', action='store_true', default=False, help="启用日志", dest='log')
    args_log.add_argument('-lf', '-log-file', '--log-file', default=None, help="将日志保存到，默认为标准输出", metavar='log_file', dest='log_file')
    args_log.add_argument('-ll', '-log-level', '--log-level', default="error", choices=['none', 'info', 'warn', 'error', 'debug'], help="日志级别",
                          dest="log_level")
    args_build_target = argparser.add_argument_group(title="构建目标")
    args_build_target.add_argument('-build-target', '--build-target', default='standard', help="构建目标。默认为 standard，也即打包全部文件。",
                                   metavar="build_target", dest='build_target')
    args_build_target.add_argument('-bt', '-basic-tags', '--basic-tags', action='store_const', const='basic_tags', help="构建为基本标签。", dest='build_target')
    args_build_target.add_argument('-gt', '-generate-tags', '--generate-tags', action='store_true', default=False, help="仅生成基本标签而不构建。",
                                   dest='generate_tags')
    args_build_target.add_argument('-static', '--static', action='store_const', const='static', default=None, help="构建为静态版本", dest='static_or_dynamic')
    args_build_target.add_argument('-dynamic', '--dynamic', action='store_const', const='dynamic', default=None, help="构建为动态版本", dest='static_or_dynamic')
    args_build_target_metadata = argparser.add_argument_group(title="构建元信息")
    args_build_target_metadata.add_argument('-lv', '-library-version', '--library-version', required=True, help="指定数据包通用库的版本。此选项为必须项",
                                            metavar='library_version', dest='library_version')
    args_build_target_version = argparser.add_argument_group(title="面向版本", description="下列选项均互斥，且必须选择一个。").add_mutually_exclusive_group(required=True)
    args_build_target_version.add_argument('-bfav', '-build-for-all-versions', '--build-for-all-versions', action='store_const', const='all',
                                   help="面向所有 Minecraft 版本（实际只能构建 23w18a 及以后的版本）", dest='minecraft_versions_to_build')
    args_build_target_version.add_argument('-bfsv', '-build-for-special-version', '--build-for-special-version', default=None,
                                   help="面向指定 Minecraft 版本。要构建的 Minecraft 版本不得低于 23w18a", metavar='version', dest='minecraft_versions_to_build')
    args_build_target_version.add_argument('-bfvr', '-build-for-version-range', '--build-for-version-range', nargs=2, help="面向指定 Minecraft 版本范围构建，\
起始版本和结束版本均不小于 23w18a，且结束版本必须大于起始版本", metavar=('start', 'end'), dest='minecraft_versions_to_build')
    args_build_config = argparser.add_argument_group(title="构建配置")
    args_build_config.add_argument('-c', '-config', '--config', default=None, help="指定构建配置的路径", metavar="config_path", dest='config')
    args_build_config.add_argument('-rc', '-rebuild-cache', '--rebuild-cache', action='store_true', default=False, help="重建构建过程中产生的缓存文件，默认不重建",
                                   dest='rebuild_cache')
    args_build_config.add_argument('-vi', '-version-info', '--version-info', default=f"cache{os.sep}version_info.json",
                                   help=f"版本信息的位置，默认为 cache{os.sep}version_info.json", metavar="version_info", dest="version_info")
    args_build_config.add_argument('-sr', '-spyglassmc-root', '--spyglassmc-root', default=os.getenv('MINECRAFT_SPYGLASSMC_ROOT'),
                                   help=f"SpyglassMC 的位置，默认为 {os.getenv('MINECRAFT_SPYGLASSMC_ROOT')}", metavar='spyglassmc_root', dest='spyglassmc_root')
    args_build_config.add_argument('-pr', '-pack-root', '--pack-root', default=os.getenv('MINECRAFT_PACK_ROOT'),
                                   help=f"通用库数据包的位置，默认为 {os.getenv('MINECRAFT_PACK_ROOT')}", metavar='pack_root', dest='pack_root')
    args_build_config.add_argument('-od', '-output-dir', '--output-dir', default="output", help="构建的输出目录，默认为 output", metavar='output_dir',
                                   dest='output_dir')
    # args_build_config.add_argument('-i', '-pi', '-icon', '-pack-icon', '--icon', '--pack-icon', default=None, help="数据包的图标，默认为空",
    #                                metavar='pack_icon', dest='pack_icon')
    build_config = argparser.parse_args()
    # 解析参数
    if build_config.print_args:
        print(build_config)
        return 0
    if build_config.debug:
        print(build_config)
    if build_config.build_target == "standard":
        if build_config.minecraft_versions_to_build != "all":
            print("标准构建必须为全版本，这是所有其他构建目标和自定义构建的基础。", file = sys.stderr)
            return 1
        elif build_config.static_or_dynamic:
            print("标准构建不支持选择构建为静态版本或动态版本。", file = sys.stderr)
            return 1
    try:
        util.validating_pack(build_config.pack_root)
    except Exception as e:
        print(e, file = sys.stderr)
        return 1
    if not os.path.exists(build_config.version_info):
        print("找不到版本信息文件！", file = sys.stderr)
        return 1
    elif os.path.isdir(build_config.version_info):
        print("版本信息是目录！", file = sys.stderr)
        return 1
    # 开始构建
    return build({
        "temp_pack_dir": f"temp{os.sep}pack{os.sep}{build_config.build_target}",
        "debug": build_config.debug,
        "log": build_config.log,
        "log_file": build_config.log_file,
        "log_level": build_config.log_level,
        "build_target": build_config.build_target,
        "generate_tags": build_config.generate_tags,
        "static_or_dynamic": build_config.static_or_dynamic,
        "library_version": build_config.library_version,
        "minecraft_versions_to_build": build_config.minecraft_versions_to_build,
        "config": build_config.config,
        "rebuild_cache": build_config.rebuild_cache,
        "version_info": build_config.version_info,
        "spyglassmc_root": build_config.spyglassmc_root,
        "pack_root": build_config.pack_root,
        "output_dir": build_config.output_dir,
        # "pack_icon": build_config.pack_icon,
    })

if __name__ == '__main__':
    sys.exit(main())
