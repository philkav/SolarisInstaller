from configparser import ConfigParser
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt
from pathlib import Path


console = Console()

def prompt_for_dir(message):
    dirname = Path(Prompt.ask(f"[bold]{message}[/bold]", default="/var/tmp", show_default=True))
    if not dirname.is_dir():
        create = Prompt.ask(f"Path '{dirname}' does not exist. Would you like to create it?", choices=["Y", "N"], show_choices=True)
        if create.upper() == 'Y':
            try:
                dirname.mkdir()
            except OSError as e:
                console.print(f"[bold red]Fail: [/bold red][white]Issue creating {dirname}[/white]")
                console.print(f"[bold yellow]Reason: [/bold yellow][white]{e}[/white]")
        else:
            console.print(f"[yellow]Skipping creation of {dirname}[/yellow]")
    return str(dirname)

class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = ConfigParser()
        if not self.filepath.exists():
            self.create()
        self.data.read(filepath)

    def create(self):
        console.print("SolarisInstaller will enter configuration phase for first run")
        cp = ConfigParser()

        cp['path'] = {}
        cp['path']['iso_home'] = prompt_for_dir("Enter the directory where ISO files will be stored")
        cp['path']['iso_fs_home'] = prompt_for_dir("Enter the directory where ISO files will be extracted")
        cp['path']['ai_manifest_home'] = prompt_for_dir("Enter the directory where AI Manifests will be stored")
        cp['path']['sc_profile_home'] = prompt_for_dir("Enter the directory where System Configuration Profiles will be stored")

        console.print(f"Creating config file at [bold blue]{self.filepath}[/bold blue]")
        self.filepath.touch(mode=0o600)
        with open(self.filepath, 'w') as cfgfile:
            cp.write(cfgfile)

    def show_pretty(self):
        # Collect data into a list first
        print_data = []
        for section in self.data.sections():
            for option in self.data[section]:
                print_data.append(
                    f"[bold]{section}.{option}[/bold]: [yellow]{self.data[section][option]}[/yellow]"
                )

        # Data is formatted as a list, print it
        console.print(
            Panel(
                '\n'.join(print_data),
                title=f"[bold white]Configuration[/bold white]: [blue]{self.filepath}[/blue]",
                expand=False,
                border_style="green"
            )
        )
