# MY-PIEXIF - EXIF 数据编辑器

一个用于修改 JPEG 图片中 EXIF（可交换图像文件格式）元数据的 Python 工具。通过简单的命令行界面，您可以编辑相机参数、GPS 坐标和其他元数据。

## 功能特性

- ✨ 修改相机参数（ISO、光圈、曝光时间、焦距等）
- 📍 设置 GPS 坐标（纬度、经度、海拔）
- 📝 编辑图片元数据（描述、艺术家、版权等）
- 📅 修改日期/时间信息
- 🔒 安全的文件处理（永不覆盖原始文件）
- 🎯 兼容 Python 3.6+

## 系统要求

- Python 3.6 或更高版本
- 无需外部依赖（仅使用 Python 标准库）

## 安装

1. 克隆或下载此仓库：
```bash
git clone <repository-url>
cd my-piexif
```

2. 无需安装！直接运行脚本即可。

## 快速开始 / 测试

要快速测试工具，您可以运行包含的测试脚本：

```bash
chmod +x test.sh
./test.sh
```

或直接使用 bash/sh：

```bash
bash test.sh
# 或
sh test.sh
```

测试脚本将使用各种 EXIF 参数修改 `test/data/noexif.jpg`，并创建一个带时间戳后缀的新文件。

## 使用方法

### 基本语法

```bash
python3 index.py <输入文件> [输出文件] [选项]
```

### 选项说明

#### 基本信息
- `--make` - 相机品牌（如 Canon, Nikon, Sony）
- `--model` - 相机型号
- `--software` - 软件版本
- `--description` - 图片描述
- `--artist` - 艺术家/摄影师姓名
- `--copyright` - 版权信息

#### 拍摄参数
- `--iso` - ISO 感光度（如 100, 200, 400, 800）
- `--fnumber` - 光圈值（如 2.8 或 f/2.8）
- `--exposure_time` - 曝光时间（如 1/125 或 0.008）
- `--focal_length` - 焦距（单位：mm，如 50）
- `--focal_length_35mm` - 35mm 等效焦距（单位：mm）

#### 拍摄条件
- `--exposure_program` - 曝光模式（0=未定义, 1=手动, 2=自动, 3=自动程序, 4=自动包围）
- `--exposure_bias` - 曝光补偿（单位：EV，如 +0.5 或 -1.0）
- `--metering_mode` - 测光模式（0=未知, 1=平均, 2=中央重点, 3=点测, 4=多点, 5=多区域）
- `--light_source` - 光源（0=未知, 1=日光, 2=荧光, 3=钨丝灯, 4=闪光灯）
- `--white_balance` - 白平衡（0=自动, 1=手动）
- `--flash` - 闪光灯模式（0=未闪光, 1=闪光, 5=闪光但未检测到反射, 7=闪光并检测到反射）
- `--scene_capture_type` - 场景类型（0=标准, 1=风景, 2=肖像, 3=夜景）

#### 日期和时间
- `--datetime_original` - 拍摄时间（格式：YYYY:MM:DD HH:MM:SS，如 2024:12:19 10:30:00）

#### GPS 信息
- `--latitude` - 纬度（如 39.9042 表示北京）
- `--longitude` - 经度（如 116.4074 表示北京）
- `--altitude` - 海拔高度（单位：米，可选）

## 使用示例

### 修改 ISO 和光圈

```bash
python3 index.py photo.jpg --iso 400 --fnumber 2.8
```

### 修改相机品牌和型号

```bash
python3 index.py photo.jpg --make "Canon" --model "EOS 5D Mark IV"
```

### 修改多个参数

```bash
python3 index.py photo.jpg \
  --iso 800 \
  --fnumber 1.4 \
  --focal_length 85 \
  --exposure_time "1/250"
```

### 设置 GPS 坐标

```bash
python3 index.py photo.jpg \
  --latitude 25.0330 \
  --longitude 121.5654
```

### 修改日期和时间

```bash
python3 index.py photo.jpg --datetime_original "2024:12:19 10:30:00"
```

### 完整示例

```bash
python3 index.py test/data/noexif.jpg \
  --make vivo \
  --model "iQOO Z9x" \
  --software "pexif 1.0" \
  --description "美丽的风景" \
  --artist "张三" \
  --copyright "© 2024 版权所有" \
  --iso 400 \
  --fnumber f/2.8 \
  --exposure_time "1/125" \
  --focal_length 60 \
  --focal_length_35mm 75 \
  --exposure_program 2 \
  --latitude 25.0330 \
  --longitude 121.5654
```

## 文件处理

- **默认行为**：如果未指定输出文件，会在输入文件同目录下创建一个带时间戳后缀的新文件（如 `photo_modified_20241219_143204.jpg`）
- **原始文件永不覆盖** - 所有修改都会保存到新文件中
- **指定输出**：使用第二个位置参数指定自定义输出文件名

```bash
# 自动生成带时间戳的文件名
python3 index.py photo.jpg --iso 400

# 指定自定义输出文件名
python3 index.py photo.jpg output.jpg --iso 400
```

## GPS 坐标

工具使用 **WGS84 坐标系**（EXIF GPS 数据的标准格式）。所有 GPS 坐标都按照 EXIF 规范以 WGS84 格式存储。

## 项目结构

```
pexif-master/
├── index.py          # 修改 EXIF 数据的主脚本
├── pexif.py          # EXIF 操作的核心库
├── setup.py          # 包安装脚本
├── LICENSE           # MIT 许可证
├── MANIFEST.in       # 包清单文件
├── test.sh           # 测试脚本
└── test/             # 测试数据目录
    └── data/         # 用于测试的示例图片
```

## 许可证

MIT 许可证

版权所有 (c) 2025-2026 heiheihoho

详情请参阅 [LICENSE](LICENSE) 文件。

## 贡献

欢迎贡献！请随时提交问题或拉取请求。

## 注意事项

- 此工具仅修改 JPEG 文件中的 EXIF 数据
- 原始文件永不覆盖（安全第一！）
- 需要 Python 3.6+（因为使用了 f-string）
- 所有 GPS 坐标都以 WGS84 格式存储（EXIF 标准）

## 故障排除

### f-string 语法错误

如果遇到与 f-string 相关的 `SyntaxError: invalid syntax`，请确保您使用的是 Python 3.6 或更高版本：

```bash
python3 --version  # 应显示 3.6 或更高版本
```

### 文件未找到

确保输入图片路径正确且文件存在：

```bash
ls -l photo.jpg  # 检查文件是否存在
```

### 权限错误

确保您对要保存输出文件的目录具有写入权限。

## 快速开始

1. 确保已安装 Python 3.6+
2. 下载或克隆项目
3. 运行测试脚本：

```bash
chmod +x test.sh
./test.sh
```

4. 查看帮助信息：

```bash
python3 index.py --help
```

