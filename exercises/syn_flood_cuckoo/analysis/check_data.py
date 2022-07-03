import click

@click.command()
@click.option('-n', help='# of nomral users', type=click.INT)
@click.option('-m', help='# of attackers', type=click.INT)
@click.option('-r', help='rate of attack')
def check_data(n, m, r):
    domain='10.0.2.'
    # Check syn/ack
    ip=set()
    f=open('n%d_m%d_r%s.txt' % (n, m, r))
    for packet in f.readlines():
        (timestamp, flag, src_ip, dst_ip) = [t(s) for t,s in zip((float,str, str, str),packet.split())]
        if(flag=='SA'):
            ip.add(dst_ip)
    print("%d/%d" % (len(ip), n+m))

if __name__ == '__main__':
    check_data()