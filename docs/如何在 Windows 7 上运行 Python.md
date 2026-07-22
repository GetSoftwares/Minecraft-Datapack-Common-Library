# **如何在 Windows 7 上运行 Python**

## **准备工作**

[PythonVista](https://github.com/adang1345/PythonVista)  
这个存储库专门为 Windows Vista 和 Windows Server 2008 等老系统构建 Python，并可以向上使用。比方说，如果 Python 基金会停止支持 Windows 10，那么这里构建的版本依然可以在 Windows 10 上运行。

## **安装 Python**

从 PythonVista 的 [镜像站](https://gitcode.com/gh_mirrors/py/PythonVista) 中下载 Python 3.14.x 版本。例如，你要安装 Python 3.14.6：

1. 进入该镜像站；
2. 点击 `3.14.6`；
3. 现在我们一般是运行在 64 位系统上的，则点击 `python-3.14.6-amd64-full.exe`；
4. 点击 `下载`，选择保存路径；
5. 从第 4 步中的保存路径运行 `python-3.14.6-amd64-full.exe`；
6. 根据安装程序的提示安装。这和通过官方安装程序安装是一样的步骤。

## **运行 Python**

现在输入以下命令：

```batch
python -c "print('Hello world!')"
```

当输出 "Hello World!" 时，恭喜你成功地在 Windows 7 上运行了 Python！

## 杂注

这是我在搜索如何在 Windows 7 上运行 Python 3.14 时找到的新存储库。根据 AI 翻译的内容，这个存储库是专门为官方不再支持的 Windows 版本构建新版本的 Python，并可以从 Windows Vista（Windows Server 2008）一路运行到 Windows 11（Windows Server 2005）。

哇！这是我没见过的运行方法，在这之前主要的方法是通过 VxKex-NEXT 运行，而且很繁琐（我没用过，但看它的步骤就知道并不是很简单）。  
它的应用兼容性列表中也说明由于需要为 Python 的整个过程都启用 VxKex-NEXT（安装和卸载程序需要指定版本为 Windows 10，还需要找到安装目录中的 python.exe 和 pythonw.exe 来启用它），所以建议使用便携版本的 Python。

所以我将原来通过 VxKex-NEXT 的方法（虽然还没写完）换成了现在通过 PythonVista 的方法（就是你现在看到的这个文档）。我没试，因为我用的是 Windows 10，可以运行 Python 3.14，但是这个方法对于 Windows 7 的老用户来说非常友好、方便、简单。

-- 写于 2026 年 7 月 20 日