# **Minecraft Datapack Common Library**

一个预存了许多常见玩法和数据包开发所需的数据包内容的 Minecraft Java 版 1.20+ 数据包通用库。
通用库预存的标签和注册表内容可以直接使用，省去了自己造轮子的烦恼。

## **你只想要用生成的数据包？**

从 output 目录里下载生成的数据包即可。
如果你是玩家，你要用到的数据包依赖于通用库，则通过 [releases](https://github.com/GetSoftwares/Minecraft-Datapack-Common-Library/releases) 下载。

## **使用通用库开发数据包**

当前只实现了标签。

你可以让结构在所有生物群系中生成，只需要在结构定义文件的 "biomes" 字段指定为 `#common:vanilla_all_biomes`：

```json
{
    "type": "minecraft:jigsaw",
    "biomes": "#common:vanilla_all_biomes",
    // 省略其它字段
}
```

也可以让火在任何方块上都能永久燃烧：

```json
{
    // 省略其它字段
    "default_clock": "minecraft:overworld",
    "has_ceiling": false,
    "has_ender_dragon_fight": false,
    "has_skylight": true,
    "height": 384,
    "infiniburn": "#common:vanilla_all_blocks",
    // 省略其它字段
}
```

只需要在需要使用标签的地方换成通用库提供的标签就可以实现一些特性或玩法了。

更多例子请参见 [文档](docs/文档.md)。

## **构建通用库**

### **准备工作**

7-Zip、Git、VSCode 或 VSCodium、Python 3.14

for Windows 7：Git 2.35.2、VSCode 1.70.3、[PythonVista](https://gitcode.com/gh_mirrors/py/PythonWin7)

for Windows 8.1：Git 2.54.x、VSCode 1.79.2

因为通用库就是用 Python 辅助构建的，所以需要安装 Python。

### **搭建工作环境**

安装上述工具，然后运行 build_devenv.cmd。

**注意**
安装 Python 时要勾上 `Add Python <Python Version> to PATH`，不然 cmd 会报错找不到 python。

for Windows 7：通过 PythonVista 项目来运行 Python 3.14。请参见 [如何在 Windows 7 上运行 Python](docs/如何在 Windows 7 上运行 Python.md)。

由于数据包开发依赖 SpyglassMC 的文件，因此需要克隆 SpyglassMC 存储库。在另外的一个目录中运行

```
git clone https://github.com/GetSoftwares/SpyglassMCFiles
```

来克隆存储库，然后需要设置 MINECRAFT_SPYGLASSMC_ROOT 环境变量为你克隆的位置，重新打开或重启计算机来应用更改。

### **推荐的扩展**

在首次打开工作区时，VSCode 应该会通过通知提示你安装推荐的扩展，其中包括 syntax-mcfunction、Datapack Helper Plus by Spyglass 和 Python。
syntax-mcfunction 用于 Minecraft 函数的语法高亮；
Datapack Helper Plus by Spyglass 则用于提供数据包开发的资源、语法检查、自动纠错、自动补全等功能；
Python 和 Pylance 则提供了 Python 支持，可以编写 Python 代码来简化开发过程，比如你要批量修改方块掉落物来实现随机掉落玩法。
只需要点击“安装”，VSCode 就会安装推荐的扩展。如果 VSCode 没有提示，你需要手动安装这些扩展。

### **开始构建**

在开始构建前，请先运行 devenv.cmd 来进入开发环境。构建程序不支持在没有进入开发环境的情况下启动构建。
运行 build.py -h 来输出帮助，然后根据你想要构建的目标输入对应选项即可。
例子：
构建标准版本：`build.py -bfav -lv 1.0.0`
构建基本标签静态版本：`build.py -bfav -s -lv 1.0.0`
构建基本标签动态版本：`build.py -bfav -t -lv 1.0.0`
构建面向 1.21 到 1.21.11 版本的通用库：`build.py -bfvr 1.21 1.21.11 -lv 1.0.0`
构建好的通用库会放到 output 下。将输出的通用库放到你的数据包项目并解压，就可以在你的项目中使用你自己的通用库构建版本。

一般你不需要自行构建通用库，因为通用库本身已经包含了许多常见玩法所需的资源。构建自己的通用库的原因通常是只面向特定的 Minecraft 版本的构建，或者只用到了某个元素。

## **需要帮助？**

查看 [文档](docs/文档.md) 和 [术语](docs/文档.md)。

## **LICENSE**

[MIT](LICENSE)
