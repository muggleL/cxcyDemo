**Fork From [luogantt/symmetry_on_stock](https://github.com/luogantt/symmetry_on_stock)**
# Windows
## 新建一空目录（如 venv ）
```
mkdir venv
```
## 创建 python 虚拟环境
```
python -m venv venv
venv\Scripts\activate.bat
```
## 安装依赖包
```
pip pip install -i https://pypi.douban.com/simple -r requests.txt
```

# Linux
## 创建 python 虚拟环境（ debian 需要提前安装 python3-venv 模块）
``` bash
mkdir venv
python -m venv ./venv
```
## 启动虚拟环境
```bash
source ./venv/bin/activate
```

## 安装依赖 (用豆瓣源加速)

```bash
pip install -i https://pypi.douban.com/simple -r requests.txt
```

## 如果运行出现 tkinter 错误，则需要安装 tk 包
### ArchLinux
```bash
sudo pacman -S tk
```
### debian 系
```bash
sudo apt install python3-tk
```
### RH 系
```bash
sudo yum install python3-tkinter
```
