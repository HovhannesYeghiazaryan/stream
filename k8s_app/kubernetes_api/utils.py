def allocate_port(used_ports: set):
    for port in range(30000, 32001):
        if port not in used_ports:
            used_ports.add(port)
            return port
    raise Exception('Port already allocated')
