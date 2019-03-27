import click

@click.group()
def cli():
    pass

@cli.group()
def bigip():
    pass

@bigip.command()
def login():
    click.echo('Logging into BIG-IP')

if __name__ == '__main__':
    cli()