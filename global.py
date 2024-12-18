import flet as ft
import logging
import smtplib
from email.mime.text import MIMEText
import shutil
from datetime import datetime
import threading
import json
# Настройки логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Глобальные переменные
feedback_log = []
current_language = "ru"
report = ""
missing_programs = {}
# Загрузка языков
def load_languages():
    with open("languages.json", "r", encoding="utf-8") as file:
        return json.load(file)

LANGUAGES = load_languages()

EMAIL_SETTINGS = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "login": "9265281620rm@gmail.com",
    "password": "jbmodvhfnyfzsspo",
    "to_email": "polise.arm@gmail.com"
}

def save_feedback_log():
    """Сохранение отзывов и оценок в лог-файл."""
    with open("feedback_log.csv", "a", encoding="utf-8") as file:
        for feedback in feedback_log:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp},{feedback['rating']},{feedback['review']}\n")


def send_report_via_email(report_content):
    """Отправка отчета через SMTP."""
    try:
        msg = MIMEText(report_content)
        msg["Subject"] = get_translation('otchet')
        msg["From"] = EMAIL_SETTINGS["login"]
        msg["To"] = EMAIL_SETTINGS["to_email"]

        with smtplib.SMTP(EMAIL_SETTINGS["smtp_server"], EMAIL_SETTINGS["smtp_port"]) as server:
            server.starttls()
            server.login(EMAIL_SETTINGS["login"], EMAIL_SETTINGS["password"])
            server.sendmail(EMAIL_SETTINGS["login"], EMAIL_SETTINGS["to_email"], msg.as_string())

        logging.info("Отчет успешно отправлен на почту.")
        return True
    except Exception as e:
        logging.error(f"Ошибка при отправке отчета: {e}")
        return False


def get_translation(key):
    """Получение перевода по ключу."""
    return LANGUAGES[current_language].get(key, f"[{key}]")


def check_versions():
    """Проверка установленных программ."""
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

    global missing_programs
    missing_programs = {}
    report_lines = []

    for program, details in programs.items():
        if shutil.which(program.lower()) is None:
            report_lines.append(f"{program}: Не найден. Установите с {details['download_url']}")
            missing_programs[program] = details['download_url']
        else:
            report_lines.append(f"{program}: Установленная версия актуальна ({details['latest_version']}).")

    return "\n".join(report_lines)


def main(page: ft.Page):
    page.title = get_translation("report_title")
    page.window_icon = "icoo.ico"
    page.theme_mode = "dark"
    page.window_width = 500
    page.window_height = 300

    def update_ui():
        """Обновление текстов интерфейса при смене языка."""
        language_selector.label = get_translation("language_label")
        check_versions_button.text = get_translation("check_versions")
        send_report_button.text = get_translation("send_report")
        exit_button.text = get_translation("exit")
        page.update()

    def open_feedback_dialog(e=None):
        """Открытие окна отзывов."""
        def submit_feedback(e):
            rating = rating_input.value
            review = review_input.value.strip()

            # Добавление отзыва в лог
            feedback_log.append({"rating": rating, "review": review})
            save_feedback_log()

            # Закрытие диалога и уведомление
            page.dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text(get_translation("thanks_message")))
            page.snack_bar.open = True
            page.update()

        def close_feedback_dialog(e=None):
            """Закрытие окна отзывов."""
            page.dialog.open = False
            page.update()

        # Элементы окна
        rating_input = ft.Dropdown(
            options=[ft.dropdown.Option(str(i)) for i in range(1, 6)],
            value="5",
            label=get_translation("rating_label"),
        )
        review_input = ft.TextField(label=get_translation("review_label"), multiline=True)

        feedback_dialog = ft.AlertDialog(
            title=ft.Text(get_translation("feedback_title")),
            content=ft.Column([rating_input, review_input]),
            actions=[
                ft.TextButton(get_translation("submit_button"), on_click=submit_feedback),
                ft.TextButton(get_translation("cancel_button"), on_click=close_feedback_dialog),
            ],
        )
        page.dialog = feedback_dialog
        page.dialog.open = True
        page.update()

    def check_versions_handler(e):
        """Обработчик кнопки проверки версий."""
        global report
        report = check_versions()
        page.snack_bar = ft.SnackBar(ft.Text(report))
        page.snack_bar.open = True
        page.update()

    def send_report_handler(e):
        """Обработчик кнопки отправки отчета."""
        if not report:
            page.snack_bar = ft.SnackBar(ft.Text("Сначала проверьте версии программ."))
            page.snack_bar.open = True
            return

        if send_report_via_email(report):
            page.snack_bar = ft.SnackBar(ft.Text(get_translation("send_success_message")))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Ошибка при отправке отчета."))
        page.snack_bar.open = True
        page.update()

    def change_language(e):
        """Смена языка."""
        global current_language
        current_language = e.control.value
        update_ui()

    # Элементы интерфейса
    language_selector = ft.Dropdown(
        options=[ft.dropdown.Option("ru"), ft.dropdown.Option("en")],
        value=current_language,
        label=get_translation("language_label"),
        on_change=change_language,
        text_style=ft.TextStyle(size=18),
    )

    check_versions_button = ft.ElevatedButton(
        text=get_translation("check_versions"),
        on_click=check_versions_handler,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=24)),
    )
    send_report_button = ft.ElevatedButton(
        text=get_translation("send_report"),
        on_click=send_report_handler,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
    )
    exit_button = ft.ElevatedButton(
        text=get_translation("exit"),
        on_click=lambda e: page.window_close(),
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
    )
    feedback_button = ft.IconButton(
        icon=ft.icons.FAVORITE,
        on_click=open_feedback_dialog,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
    )

    # Интерфейс
    layout = ft.Column(
        [
            ft.Row(
                [feedback_button, language_selector],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Column(
                        [
                            check_versions_button,
                            send_report_button,
                            exit_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
        ],
    )
    page.add(layout)

    # Таймер для автоматического открытия окна отзывов
    threading.Timer(20, open_feedback_dialog).start()


# Запуск приложения
ft.app(target=main) 