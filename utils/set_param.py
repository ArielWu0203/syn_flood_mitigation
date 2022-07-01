import click

@click.command()
@click.option('-n', help='# of nomral users', type=click.INT)
@click.option('-m', help='# of attackers', type=click.INT)
@click.option('-r', help='rate of attack')
def set_param(n, m, r):
    file_makefile=open("Makefile", 'w')
    file_template=open("makefile_template", 'r')
    old=file_template.read()
    file_makefile.write("NORMAL=%d\nATTACKER=%d\nRATE=%s\n%s" % (n, m, r, old))

if __name__ == '__main__':
    set_param()