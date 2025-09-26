# EasyKiConverter 打包说明

## 打包前准备

1. 确保项目根目录下的 `even` 文件夹中包含完整的虚拟环境
2. 确保所有依赖包已正确安装在虚拟环境中

## 打包步骤

### Linux平台打包
```bash
cd output
bash build_linux.sh
```

### Windows平台打包
```cmd
cd output
build_windows.bat
```

### macOS平台打包
```bash
cd output
bash build_macos.sh
```

## 打包配置文件说明

- `build.spec` - 通用配置文件，适用于Linux平台
- `build_windows.spec` - Windows平台专用配置文件，包含图标支持
- `build_macos.spec` - macOS平台专用配置文件，包含APP打包支持

## 打包结果

打包完成后，可执行文件将位于 `output/dist/` 目录中：
- Linux: `dist/EasyKiConverter`
- Windows: `dist\EasyKiConverter.exe`
- macOS: `dist/EasyKiConverter.app`

## 注意事项

1. 打包过程可能需要几分钟时间，请耐心等待
2. 打包前会自动清理之前的构建文件
3. 生成的可执行文件为独立应用，无需安装Python环境即可运行
4. 如果遇到打包错误，请检查虚拟环境中的依赖包是否完整
5. 各平台使用不同的spec文件以优化打包结果