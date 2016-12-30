import subprocess
import time

if __name__ == '__main__':
    ssh_config = ['ssh', '-N', '-L']
    processes = []

    with open('tun.cfg') as tunnels:
        for tunnel in tunnels.readlines():
            tun_config = tunnel.split()

            if not tunnel.startswith('#') and not tunnel.startswith('\n'):
                processes.append(subprocess.Popen(ssh_config + tun_config))

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for process in processes:
                process.terminate()

            exit()
