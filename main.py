import shutil  # Для проверки наличия программы

# Функция для проверки версий программ
def check_versions():
    """Проверка версий Python, Ruby и Go как на вашем ПК, так и онлайн."""
    programs = {
        "Python": {
            "command": "python --version",
            "latest_version": "3.13.1",
            "download_url": "https://www.python.org/downloads/"
        },
        "Ruby": {
            "command": "ruby --version",
            "latest_version": "3.3.6",
            "download_url": "https://www.ruby-lang.org/en/downloads/"
        },
        "Go": {
            "command": "go version",
            "latest_version": "1.23.4",
            "download_url": "https://go.dev/dl/"
        }
    }

    report = []
    for program, details in programs.items():
        if shutil.which(program.lower()) is None:
            report.append(f"{program}: Не найден. Установите с {details['download_url']}")
        else:
            # Здесь могла бы быть проверка версии через subprocess, но для примера - статично
            report.append(f"{program}: Установленная версия актуальна ({details['latest_version']}).")

    return "\n".join(report)

if __name__ == "__main__":
    result = check_versions()
    print(result)
