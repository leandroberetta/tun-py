import subprocess
import time
import re


class Tunnel:

    def __init__(self, dst_port, src_host, src_port, from_host):
        self.ssh_config = ['ssh', '-o', 'ConnectTimeout=10', '-N', '-L']

        self.dst_port = dst_port
        self.src_host = src_host
        self.src_port = src_port
        self.from_host = from_host[:-1] # Removes an ending \n
        self.process = None

        self.ssh_config.append('{0}:{1}:{2}'.format(self.dst_port, self.src_host, self.src_port))
        self.ssh_config.append(self.from_host)

    def establish(self):
        if self.process and self.process.poll():
            self.process.terminate()

        self.process = subprocess.Popen(self.ssh_config)

    def terminate(self):
        self.process.terminate()

    def is_alive(self):
        return self.process.poll() is None

    def __str__(self):
        return 'tunnel: from: {0:16} : {1:6} -> to: localhost : {2:6} '.format(self.src_host, self.src_port, self.dst_port)


if __name__ == '__main__':
    tunnels = []

    def valid_tunnel(tunnel_line):
        return not tunnel_line.startswith('#') and not tunnel_line.startswith('\n')

    def tunnel_config_parser(tunnel_line):
        return re.split('[: ]', tunnel_line)

    with open('tun.cfg') as tunnels_config_file:
        tunnel_lines = filter(lambda tunnel_line: valid_tunnel(tunnel_line), tunnels_config_file.readlines())

        for tunnel_line in tunnel_lines:
            tunnel = Tunnel(*tunnel_config_parser(tunnel_line))
            tunnel.establish()
            tunnels.append(tunnel)

            print(str(tunnel))

    while True:
        try:
            for tunnel in tunnels:
                if not tunnel.is_alive():
                    print('restarting ' + str(tunnel))
                    tunnel.establish()

            time.sleep(1)
        except KeyboardInterrupt:
            for tunnel in tunnels:
                tunnel.terminate()

            exit()
