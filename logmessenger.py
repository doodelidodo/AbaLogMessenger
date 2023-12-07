import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import logging
from datetime import datetime

def setup_logging():
    log_file_path = r'D:\Abacus\logmessenger\logfile.log'

    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())  # Hiermit werden die Log-Einträge auch auf der Konsole angezeigt

def send_email(subject, body, sender_email, sender_password, receiver_email):
    try:
        # E-Mail-Server-Einstellungen (für Gmail)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Erstelle das MIME-Objekt
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Füge den E-Mail-Text hinzu
        msg.attach(MIMEText(body, 'plain'))

        # Verbindung zum SMTP-Server herstellen
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Anmelden
        server.login(sender_email, sender_password)

        # E-Mail senden
        server.sendmail(sender_email, receiver_email, msg.as_string())
        logging.info("E-Mail erfolgreich gesendet.")

    except smtplib.SMTPException as e:
        logging.error(f"Fehler beim Senden der E-Mail: {e}")

    finally:
        # Verbindung trennen
        server.quit()

def main():
    setup_logging()

    # Lade Konfigurationsdatei
    config_path = r'D:\Abacus\logmessenger\config.json'

    if not os.path.exists(config_path):
        logging.error("Die Konfigurationsdatei existiert nicht.")
        return

    with open(config_path, 'r') as config_file:
        try:
            config_data = json.load(config_file)

            # Überprüfe, ob die erforderlichen Optionen vorhanden sind
            if "log_files" not in config_data:
                logging.error("Die erforderlichen Optionen sind nicht vorhanden.")
                return

            log_files = config_data["log_files"]

            for log_file_config in log_files:
                # Verzeichnis mit Log-Dateien
                log_directory = log_file_config.get('log_directory')

                # Sender-E-Mail-Einstellungen
                sender_email_address = log_file_config.get('sender_email_address')
                sender_email_password = log_file_config.get('sender_email_password')

                # Empfänger-E-Mail-Einstellungen
                receiver_email_addresses = log_file_config.get('receiver_email_addresses', [])

                # Keyword zum Suchen im Dateinamen
                keyword_to_search = log_file_config.get('keyword_to_search')
                keyword_in_filename = log_file_config.get('keyword_in_filename')

                # Liste aller Log-Dateien im Verzeichnis, die das Keyword im Namen haben
                log_files = [file for file in os.listdir(log_directory) if keyword_in_filename in file]
                log_files.sort(reverse=True)

                # Wähle die neueste Log-Datei aus
                if log_files:
                    newest_log_file = log_files[0]
                    log_file_path = os.path.join(log_directory, newest_log_file)

                    with open(log_file_path, "r") as log_file:
                        log_content = log_file.read()

                    # Suche nach der Zeichenkette
                    if keyword_to_search in log_content:
                        logging.info(f"Zeichenkette '{keyword_to_search}' in der Log-Datei {newest_log_file} gefunden.")
                        subject = f"Fehlermeldung: {keyword_to_search} ({newest_log_file})"
                        body = f"Die Zeichenkette '{keyword_to_search}' wurde in der Log-Datei {newest_log_file} gefunden."
                        for receiver_email in receiver_email_addresses:
                            send_email(subject, body, sender_email_address, sender_email_password, receiver_email)
                    else:
                        logging.info(f"Keine Zeichenkette '{keyword_to_search}' in der Log-Datei {newest_log_file} gefunden.")
                else:
                    logging.info(f"Keine Log-Dateien mit '{keyword_to_search}' im Namen im Verzeichnis gefunden.")
        except json.JSONDecodeError as e:
            logging.error(f"Fehler beim Lesen der Konfigurationsdatei: {e}")

if __name__ == "__main__":
    main()
