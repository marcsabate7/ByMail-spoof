config = {
	"attacker_site": b"attack.com", # attack.com
	"legitimate_site_address": b"prova@semic.es", # cabecera FROM que es la que el usuario final vera
	"victim_address": b"msabate@semic.es", # cabecera RCPT TO 
	"case_id": b"server_a1", 

	"server_mode":{
		"recv_mail_server": "", # Ip del mail server de la victima, esta se tiene que introducir al correr la herramienta
		"recv_mail_server_port": 25,
		"starttls": False,          # Missatge xifrat amb TLS -> True / No xifrat -> False
	},

}
