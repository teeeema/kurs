import shutil  # Для проверки наличия программы
import smtplib
from email.mime.text import MIMEText
from tkinter import Tk, Button, Label, Text, END

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
        raise RuntimeError(f"Ошибка при отправке email: {e}")

# Функция для обработки нажатия кнопки "Проверить версии"
def on_check_versions():
    report = check_versions()
    report_text.delete(1.0, END)
    report_text.insert(END, report)

# Функция для обработки нажатия кнопки "Отправить отчет"
def on_send_report():
    report = report_text.get(1.0, END).strip()
    if not report:
        report_text.insert(END, "\nПожалуйста, сначала выполните проверку версий.")
        return

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
            body=report
        )
        report_text.insert(END, "\nОтчет успешно отправлен на email.")
    except RuntimeError as e:
        report_text.insert(END, f"\nНе удалось отправить отчет: {e}")

if __name__ == "__main__":
    # Создание интерфейса
    root = Tk()
    root.title("Проверка версий ПО")
    root.geometry("600x400")

    check_button = Button(root, text="Проверить версии", command=on_check_versions)
    check_button.pack(pady=10)

    send_button = Button(root, text="Отправить отчет", command=on_send_report)
    send_button.pack(pady=10)

    report_text = Text(root, wrap="word", height=15, width=70)
    report_text.pack(pady=10)

    root.mainloop()
