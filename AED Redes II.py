import math

def menu():
    print("\nDigite a opcao desejada:")
    print("[1] - Enderecamento com classes")
    print("[2] - Enderecamento sem classes - mascara na notacao decimal")
    print("[3] - Enderecamento sem classes - mascara na notacao CIDR")
    print("[4] - Sair")
    
    return int(input())

def str_to_int(string):
    return int(string)

def convert_ip_to_int(ip):
    try:
        octetos = list(map(int, ip.split('.')))
        if len(octetos) != 4 or any(o < 0 or o > 255 for o in octetos):
            return None
        return octetos
    except ValueError:
        return None

def ip_int_to_bin(ip_int):
    return [int(bit) for octet in ip_int for bit in format(octet, '08b')]

def bin_to_int_str(binario):
    return '.'.join(str(int(''.join(map(str, binario[i*8:(i+1)*8])), 2)) for i in range(4))

def do_and(bin1, bin2):
    return [b1 & b2 for b1, b2 in zip(bin1, bin2)]

def do_or(bin1, bin2):
    return [b1 | b2 for b1, b2 in zip(bin1, bin2)]

def main():
    while True:
        opc = menu()
        
        if opc < 1 or opc > 4:
            print("Opcao Invalida")
        elif opc == 4:
            break
        else:
            ip = input("\nDigite o IP (padrao: n.n.n.n): ")
            
            ip_int = convert_ip_to_int(ip)
            if not ip_int:
                print("IP Invalido")
                continue
            
            print("IP Valido")
            ip_bin = ip_int_to_bin(ip_int)
            
            if opc == 1:
                classe = sum(ip_bin[:4])
                masc = 3 if classe < 3 else 4
                cidr = 32 - (8 * masc)
                
                print(f"IP classe {chr(65 + classe)}")
                if classe == 3:
                    print("Endereco reservado para Multicast")
                elif classe == 4:
                    print("Endereco reservado para uso futuro")
                else:
                    print(f"Mascara CIDR /{cidr}")
                    
                    bin_masc = [1] * cidr + [0] * (32 - cidr)
                    bin_masc_cmp = [1 - b for b in bin_masc]
                    
                    print(f"Mascara Decimal {bin_to_int_str(bin_masc)}")
                    print(f"Numero de Hosts {2**(8 * masc) - 2}")
                    
                    rede = do_and(ip_bin, bin_masc)
                    broadcast = do_or(ip_bin, bin_masc_cmp)
                    print(f"Endereco de rede {bin_to_int_str(rede)}")
                    print(f"Endereco de broadcast {bin_to_int_str(broadcast)}")
            
            elif opc == 2:
                mascara = input("\nDigite a Mascara na notacao decimal (padrao: n.n.n.n): ")
                masc_int = convert_ip_to_int(mascara)
                if not masc_int:
                    print("Mascara Invalida")
                    continue
                
                masc_bin = ip_int_to_bin(masc_int)
                if masc_bin != sorted(masc_bin, reverse=True):
                    print("Mascara Invalida")
                    continue
                
                print("Mascara Valida")
                cidr = sum(masc_bin)
                bin_masc_cmp = [1 - b for b in masc_bin]
                print(f"Mascara CIDR /{cidr}")
                print(f"Numero de Hosts {2**(32 - cidr) - 2}")
                
                rede = do_and(ip_bin, masc_bin)
                broadcast = do_or(ip_bin, bin_masc_cmp)
                print(f"Endereco de rede {bin_to_int_str(rede)}")
                print(f"Endereco de broadcast {bin_to_int_str(broadcast)}")
            
            elif opc == 3:
                cidr = int(input("\nDigite a Mascara na CIDR (padrao: /n): ").strip('/'))
                if not (0 <= cidr <= 32):
                    print("Mascara invalida")
                    continue
                
                print("Mascara Valida")
                bin_masc = [1] * cidr + [0] * (32 - cidr)
                bin_masc_cmp = [1 - b for b in bin_masc]
                
                print(f"Mascara decimal {bin_to_int_str(bin_masc)}")
                print(f"Mascara CIDR /{cidr}")
                print(f"Numero de Hosts {2**(32 - cidr) - 2}")
                
                rede = do_and(ip_bin, bin_masc)
                broadcast = do_or(ip_bin, bin_masc_cmp)
                print(f"Endereco de rede {bin_to_int_str(rede)}")
                print(f"Endereco de broadcast {bin_to_int_str(broadcast)}")
                
if __name__ == "__main__":
    main()
