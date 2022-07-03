import click

@click.command()
@click.option('-n', help='# of nomral users', type=click.INT)
@click.option('-m', help='# of attackers', type=click.INT)
@click.option('-r', help='rate of attack')
@click.option('-d', help='.pcap file will store in which directory')
def set_param(n, m, r, d):
    file_makefile=open("Makefile", 'w')
    file_template=open("makefile_template", 'r')
    old=file_template.read()
    file_makefile.write("NORMAL=%d\nATTACKER=%d\nRATE=%s\nTEST_DIR=%s\n%s" % (n, m, r, d, old))

if __name__ == '__main__':
    set_param()