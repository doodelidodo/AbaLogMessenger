# AbaLogMessenger
Dieses Script führt eine Überprüfung durch, ob in einem Logfile (kann im config.json definiert werden) eine bestimmte Zeichenkette vorkommt.
Trifft dies zu, wird an die in der Config definierten Emailadressen, eine Nachricht dazu versendet. Es wird immer das neuste Logfile im Ordner für die Kontrolle genommen.

## Config File

Muss config.json heissen und beinhaltet folgende Parameter:

log_directory: wo liegt das Logfile
sender_email_address: MUSS ein Googlekonto sein, da die smtp Einstellungen darauf beruhen.
sender_email_password: Im Google Konto muss ein App Passwort definiert werden, das "normale" Loginpasswort funktioniert nicht.
receiver_email_addresses: Array von Emailadressen, an die eine Nachricht gesendet werden soll, wenn das Keyword im Logfile auftaucht
keyword_to_search: Wenn diese Zeichenkette im Logfile vorkommt, wird eine Nachricht ausgelöst
keyword_in_filename: Da in einem Logfileordner mehrere verschiedene Logfiles drin vorkommen können, kann ein Teil des Dateinahmens hier angegeben werden, dass das korrekte File durchsucht wird.

{
  "log_files": [
    {
      "log_directory": "D:/Abacus/abac/log/interfaceserver",
      "sender_email_address": "YourGooggleEmail@gmail.com",
      "sender_email_password": "APPPassword",
      "receiver_email_addresses": ["receiver@email.com", "receiver2@email.com"],
      "keyword_to_search": "Address already in use: connect",
      "keyword_in_filename": "aba-server-SRV83"
    }
  ]
}
