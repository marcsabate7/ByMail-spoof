config = {
	"attacker_site": b"attack.com", # attack.com
	"legitimate_site_address": b"prova@semic.es", # FROM header that is the address displayed to the final user  
	"case_id": b"server_a1", 
    # Set the victim address in the users.txt file which is placed in the same folder

	"server_mode":{
		"recv_mail_server": "", # Ip del mail server de la victima, esta se tiene que introducir al correr la herramienta
		"recv_mail_server_port": 25,
		"starttls": False,          # Missatge xifrat amb TLS -> True / No xifrat -> False
	},
}
