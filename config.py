config = {
	"attacker_site": b"attack.com", 
	"legitimate_site_address": b"Departamento de Tecnologia - HSM <tic@gss.cat>",   # Address you want to display to the final user  
	"case_id": b"1",    # Select mode in cases.py file

    # Marcos Palacios Cenizo <marcos.palacios@infojobs.com.br>
    
    # Set the victim/s address (people you want to send the mail to) in the users.txt file

	"server_mode":{
		"recv_mail_server": "",     #Leave it empty this will be caught automatically querying the vixitm MX server
		"recv_mail_server_port": 25,
		"starttls": True,           # With cipher starttls -> True / Withour cipher starttls -> False
	},
}
