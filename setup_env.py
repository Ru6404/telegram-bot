import os
import platform
import subprocess
import sys
import shutil


def run(cmd, check=True):
    """Выполнить команду в shell"""
    print(f"⚡ Запуск: {cmd}")
    subprocess.run(cmd, shell=True, check=check)


def ensure_rust():
    """Установка Rust для pydantic-core"""
    if shutil.which("cargo") is None:
        print("🦀 Rust не найден — устанавливаю...")
        if platform.system() == "Windows":
            run("powershell -Command \"Invoke-WebRequest https://win.rustup.rs -UseBasicParsing -OutFile rustup-init.exe; Start-Process rustup-init.exe -ArgumentList '-y' -Wait\"")
        else:
            run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
            rust_env = os.path.expanduser("~/.cargo/env")
            if os.path.exists(rust_env):
                print("🔧 Подключаю Rust в PATH")
                run(f"source {rust_env}", check=False)
    else:
        print("✅ Rust уже установлен")


def install_system_deps():
    """Установка системных зависимостей"""
    os_name = platform.system()
    print(f"🖥️ ОС определена: {os_name}")

    if os_name == "Linux":
        if shutil.which("apt-get"):
            run("sudo apt-get update")
            run("sudo apt-get install -y build-essential python3-dev curl pkg-config libffi-dev")
        elif shutil.which("yum"):
            run("sudo yum groupinstall -y 'Development Tools'")
            run("sudo yum install -y python3-devel curl libffi-devel")
    elif os_name == "Darwin":  # macOS
        run("xcode-select --install || true", check=False)
        if shutil.which("brew"):
            run("brew install libffi || true")
    elif os_name == "Windows":
        print("🪟 Windows: системные зависимости не требуются, пропускаю.")
    else:
        print("⚠️ ОС не распознана, установка зависимостей пропущена")


def main():
    print("🚀 Универсальная настройка окружения для pydantic-core и uvloop")

    # 1. Обновляем pip, setuptools, wheel
    run(f"{sys.executable} -m pip install --upgrade pip setuptools wheel")

    # 2. Системные зависимости
    install_system_deps()

    # 3. Rust
    ensure_rust()

    # 4. Устанавливаем пакеты
    os_name = platform.system()
    try:
        if os_name == "Windows":
            print("🪟 Устанавливаю только pydantic-core (uvloop недоступен на Windows)")
            run(f"{sys.executable} -m pip install --only-binary=:all: pydantic-core")
        else:
            run(f"{sys.executable} -m pip install --only-binary=:all: pydantic-core uvloop")
    except subprocess.CalledProcessError:
        print("⚠️ Не удалось поставить бинарники, пробую из исходников...")
        if os_name == "Windows":
            run(f"{sys.executable} -m pip install pydantic-core")
        else:
            run(f"{sys.executable} -m pip install pydantic-core uvloop")

    # 5. Проверка
    try:
        import pydantic_core
        print(f"✅ pydantic-core {pydantic_core.__version__}")
        if os_name != "Windows":
            import uvloop
            print(f"✅ uvloop {uvloop.__version__}")
        else:
            print("ℹ️ uvloop недоступен на Windows")
    except Exception as e:
        print("❌ Ошибка импорта:", e)


if __name__ == "__main__":
    main()
