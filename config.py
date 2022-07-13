config = {
	"attacker_site": b"attack.com", 
	"legitimate_site_address": b"Unitat d'Informatica - UdL <informatica@udl.cat>",   # Address you want to display to the final user
	"case_id": b"1",    # Select mode in cases.py file

    # 2 address formats: 
    # Unitat d'Informatica - HSM <tic@gss.cat>
    # <tic@gss.cat>

	"server_mode":{
		"recv_mail_server": "",     #Leave it empty this will be caught automatically querying the vixitm MX server
		"recv_mail_server_port": 25,
		"starttls": True,           # With cipher starttls -> True / Withour cipher starttls -> False
	},
}
