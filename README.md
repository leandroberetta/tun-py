# tun-py

Python script to create SSH tunnels from a config file.

The tunnels configuration must be in tun.cfg with the format as follows:

  # Dev
  5555:192.168.200.100:5555 lberetta@192.168.200.100

  # Prod
  5556:192.168.200.101:5556 lberetta@192.168.200.100
  5557:192.168.200.101:5557 lberetta@192.168.200.100

The command executed (eg. Dev) will be:

ssh -N -L 5555:192.168.200.100:5555 lberetta@192.168.200.100

Finishing the script (with Ctrl+C) will terminate all tunnels.

To create the tunnels execute:

  python tun.py
