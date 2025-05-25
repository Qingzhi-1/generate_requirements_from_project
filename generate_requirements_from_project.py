import os
import re
import pkg_resources

# 标准库列表（常用的，避免误加）
STANDARD_LIBS = {
    'os', 'sys', 're', 'time', 'random', 'threading', 'traceback', 'typing',
    'logging', 'ast', 'concurrent', 'collections', 'functools', 'itertools',
    'math', 'statistics', 'json', 'http', 'subprocess', 'unittest', 'platform'
}

def extract_modules_from_file(filepath):
    modules = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("import "):
                parts = re.findall(r'import (\S+)', line)
                for part in parts:
                    modules.add(part.split('.')[0])
            elif line.startswith("from "):
                parts = re.findall(r'from (\S+)', line)
                for part in parts:
                    modules.add(part.split('.')[0])
    return modules

def scan_all_py_files(project_dir):
    all_modules = set()
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                modules = extract_modules_from_file(file_path)
                all_modules.update(modules)
    return all_modules

def get_installed_versions(modules):
    result = []
    for module in sorted(modules):
        if module in STANDARD_LIBS:
            continue
        try:
            dist = pkg_resources.get_distribution(module)
            result.append(f"{dist.project_name}=={dist.version}")
        except Exception:
            print(f"[跳过] 未识别模块或未安装：{module}")
    return result

def main():
    project_dir = "."  # 当前目录，也可以手动设置为你的项目目录路径
    print("📁 正在扫描项目目录...")
    all_modules = scan_all_py_files(project_dir)
    print(f"🔍 发现模块数量：{len(all_modules)}")

    requirements = get_installed_versions(all_modules)

    with open("requirements.txt", "w", encoding="utf-8") as f:
        for line in requirements:
            f.write(line + "\n")

    print("✅ 已生成 requirements.txt 文件")

if __name__ == "__main__":
    main()
