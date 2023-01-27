from json import loads as json_loads

if __name__ == '__main__':
    result = ''
    with open('./cfg/hosts.json', 'r') as file:
        hosts = json_loads(file.read())
        for host in hosts:
            result += f"Host {host['Name']}\n"
            result += f"\tHostName {host['Host']}\n"
            result += f"\tUser {host['User']}\n"
            result += f"\tPort {host['Port']}\n\n"
    print(result)