import shutil  # Для проверки наличия программы
import smtplib
from email.mime.text import MIMEText
from tkinter import Tk, Button, Label, Text, END, StringVar, OptionMenu
import json

# Глобальный выбор языка
current_language = "ru"

def load_languages(file_path="languages.json"):
    """Загружает словарь переводов из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки языкового файла: {e}")

LANGUAGES = load_languages()

def translate(key):
    """Получает перевод для текущего языка."""
    return LANGUAGES[current_language].get(key, key)

# Остальной код остается без изменений

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
            report.append(f"{program}: Not found. Install from {details['download_url']}")
        else:
            report.append(f"{program}: Installed version is up to date ({details['latest_version']}).")

    return "\n".join(report)

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
        raise RuntimeError(f"Error sending email: {e}")

def on_check_versions():
    report = check_versions()
    report_text.delete(1.0, END)
    report_text.insert(END, report)

def on_send_report():
    report = report_text.get(1.0, END).strip()
    if not report:
        report_text.insert(END, translate("no_report"))
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
            subject="Software Version Report",
            body=report
        )
        report_text.insert(END, translate("report_success"))
    except RuntimeError as e:
        report_text.insert(END, f"{translate('report_error')}{e}")

def on_language_change(selected_language):
    global current_language
    current_language = selected_language
    update_ui_text()

def update_ui_text():
    root.title(translate("title"))
    check_button.config(text=translate("check_button"))
    send_button.config(text=translate("send_button"))
    language_label.config(text=translate("language_label"))

if __name__ == "__main__":
    root = Tk()
    root.title(translate("title"))
    root.geometry("600x400")

    language_label = Label(root, text=translate("language_label"))
    language_label.pack(pady=5)

    language_var = StringVar(value=current_language)
    language_menu = OptionMenu(root, language_var, *LANGUAGES.keys(), command=on_language_change)
    language_menu.pack(pady=5)

    check_button = Button(root, text=translate("check_button"), command=on_check_versions)
    check_button.pack(pady=10)

    send_button = Button(root, text=translate("send_button"), command=on_send_report)
    send_button.pack(pady=10)

    report_text = Text(root, wrap="word", height=15, width=70)
    report_text.pack(pady=10)

    update_ui_text()
    root.mainloop()
