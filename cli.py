import click
import os
import json
from .client import Client

@click.group()
def cli():
    """Main CLI group"""
    pass

@click.command()
@click.argument('content')
@click.option('--is-read', is_flag=True, help='Mark the mem as read.')
@click.option('--is-archived', is_flag=True, help='Mark the mem as archived.')
@click.option('--scheduled-for', default=None, help='Time the mem should resurface.')
@click.option('--created-at', default=None, help='Time the mem was created.')
@click.option('--mem-id', default=None, help='ID to assign to the new mem.')
def create_mem(content, is_read, is_archived, scheduled_for, created_at, mem_id):
    """Create a new mem with the specified content and options"""
    api_token = os.getenv("API_ACCESS_TOKEN")
    if not api_token:
        click.echo("API_ACCESS_TOKEN environment variable not set.")
        return

    client = Client(api_token)
    response = client.create_mem(content, is_read, is_archived, scheduled_for, created_at, mem_id)
    click.echo(response)

@click.command()
@click.argument('file_path')
def create_mem_from_file(file_path):
    """Create a new mem by uploading a markdown file"""
    api_token = os.getenv("API_ACCESS_TOKEN")
    if not api_token:
        click.echo("API_ACCESS_TOKEN environment variable not set.")
        return

    client = Client(api_token)
    response = client.create_mem_from_file(file_path)
    click.echo(response)

@click.command()
@click.argument('mems', type=click.File('r'))
def batch_create_mems(mems):
    """Batch create mems from a JSON file"""
    api_token = os.getenv("API_ACCESS_TOKEN")
    if not api_token:
        click.echo("API_ACCESS_TOKEN environment variable not set.")
        return

    client = Client(api_token)
    mems_list = json.load(mems)
    response = client.batch_create_mems(mems_list)
    click.echo(response)

@click.command()
@click.argument('mem_id')
@click.argument('content')
def append_to_mem(mem_id, content):
    """Append content to an existing mem"""
    api_token = os.getenv("API_ACCESS_TOKEN")
    if not api_token:
        click.echo("API_ACCESS_TOKEN environment variable not set.")
        return

    client = Client(api_token)
    response = client.append_to_mem(mem_id, content)
    click.echo(response)

cli.add_command(create_mem)
cli.add_command(create_mem_from_file)
cli.add_command(batch_create_mems)
cli.add_command(append_to_mem)

if __name__ == "__main__":
    cli()
