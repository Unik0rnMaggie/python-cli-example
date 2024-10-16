import subprocess
import shlex
import json
import click

def run_command(command):
    """
    Runs a shell command and returns the output.

    Args:
        command (str): The command to run.

    Returns:
        str: The output of the command.
    """
    cmd = shlex.split(command)
    output = subprocess.check_output(cmd)
    return output

def run_lsblk(device):
    """
    Runs lsblk command and produces JSON output.

    Args:
        device (str): The device name.

    Returns:
        dict: The device information.
    """
    command = 'lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT'
    output = run_command(command)
    devices = json.loads(output)['blockdevices']
    for parent in devices:
        if parent['name'] == device:
            return parent
        for child in parent.get('children', []):
            if child['name'] == device:
                return child
    return None

@click.command()
@click.option('--verbose', '-v', is_flag=True)
@click.argument('device')
def main(device, verbose):
    """
    Main function to run the lsblk command.

    Args:
        device (str): The device name.
        verbose (bool): Verbose flag.
    """
    print(f"Device: {device}")
    print(f"Verbose: {verbose}")
    print(f"{run_lsblk(device)}")