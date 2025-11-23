import ipaddress



def gen_ip(cidr_notation):
    """
    Generates a list of all host IP addresses within a given CIDR notation.
    """
    try:
        network = ipaddress.ip_network(cidr_notation)
        return [str(ip) for ip in network.hosts()]
    except ValueError as e:
        print(f"Error: Invalid CIDR notation - {e}")
        return []