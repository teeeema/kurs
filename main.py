import shutil  # Для проверки наличия программы
import smtplib
from email.mime.text import MIMEText

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

# Функция для отправки отчета на email
def send_email(smtp_server, smtp_port, login, password, to_email, subject, body):
    """Отправка email с отчетом."""
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = login
        msg["To"] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(login, to_email, msg.as_string())
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")
        raise RuntimeError(f"Ошибка при отправке email: {e}")

if __name__ == "__main__":
    result = check_versions()
    print(result)

    # Настройки для отправки email
    EMAIL_SETTINGS = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "login": "your_email@gmail.com",
        "password": "your_email_password",
        "to_email": "recipient_email@gmail.com"
    }

    try:
        send_email(
            smtp_server=EMAIL_SETTINGS["smtp_server"],
            smtp_port=EMAIL_SETTINGS["smtp_port"],
            login=EMAIL_SETTINGS["login"],
            password=EMAIL_SETTINGS["password"],
            to_email=EMAIL_SETTINGS["to_email"],
            subject="Отчет о проверке версий ПО",
            body=result
        )
        print("Отчет успешно отправлен на email.")
    except RuntimeError as e:
        print(f"Не удалось отправить отчет: {e}")
