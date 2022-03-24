import sys
import argparse

from taser import printx


def banner():
    author = '@marcsabate7'
    version = 'v0.1.0'
    printx.colored('''                                                                                                                                                     
______        ___  ___        _  _ 
| ___ \       |  \/  |       (_)| |
| |_/ / _   _ | .  . |  __ _  _ | |
| ___ \| | | || |\/| | / _` || || |
| |_/ /| |_| || |  | || (_| || || |
\____/  \__, |\_|  |_/ \__,_||_||_|
         __/ |                     
        |___/                         
    ''', fg='blue')
    printx.colored("    Version: v0.1.0", fg="purple")
    printx.colored("    Author: @marcsabate7",fg= "purple")

def parse_args():
    print("\n")
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: Este script se utiliza para enviar correos electronicos suplantando la identidad de otra persona",usage="\n- python bymail.py \'dominio_victima\'   \n\n ** ES NECESSARIO RELLENAR 'usuarios.txt' Y 'body.txt' PARA USAR LA HERRAMIENTA ** \n ", epilog='\nEjemplo: \r\npython ' + sys.argv[0] + " facebook.com"
    )
    parser.add_argument("dominio_victima", help="Dominio de la victima. El dominio que va a ser suplantado")
    parser.add_argument("-users", required=False, help="Rellenar archivo 'usuarios.txt'. Lista de usuarios a los que enviar el correo electronico") # Quitar argumentos
    parser.add_argument("-body", required=False,help="Rellenar archivo 'body.txt'. Se puede poner tanto texto plano como HTML") # Quitar argumentos
    parser.add_argument('-v', required=False, default=False, type=bool,help='Mostrar mensajes por pantalla (True/False)')

    args = parser.parse_args()
    return args

def main():
    banner()
    
    args = parse_args()
    print(args)


if __name__ == '__main__':
    main()