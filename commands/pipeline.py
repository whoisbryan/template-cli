import subprocess, typer, questionary

import src.pipeline.template as template
import src.harness.harness_api as harness_api

from typing_extensions import Annotated
from rich import print
from rich.text import Text
from rich.padding import Padding

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

app = typer.Typer()


@app.command()
def create(
        # service_name: Annotated[str, typer.Argument(help="Pipeline service name")],
        # pull_request: Annotated[bool, typer.Option(help="Create Pull Request to your repo")] = False,
        # interactive: Annotated[bool, typer.Option(help="Interactive CLI")] = True,
    ):

    '''
    Add new Harness CI pipeline for your service.
    '''

    SERVICE_NAME = questionary.text("What's your service name?",
                                    instruction="(Same as repo name)",
                                    validate=lambda text: len(text) > 0).ask()

    ORG_ID = questionary.select("Select your team",
                                qmark="🔎",
                                pointer="👉",
                                choices=[item['identifier'] for item in harness_api.get_orgs()]).ask() # only show org id

    projects_by_org = harness_api.get_projects_in_org(ORG_ID)

    PROJECT_ID = questionary.select("Select project",
                                qmark="🔎",
                                pointer="👉",
                                choices=[item['identifier'] for item in projects_by_org]).ask()
    
    TEMPLATE_ID = questionary.select("Select pipeline template to use",
                                qmark="🔎",
                                pointer="👉",
                                instruction="(If protos then select Golang B)",
                                choices=[item['identifier'] for item in harness_api.get_templates_dir()]).ask()

    template_values = {
        "SERVICE_NAME" : SERVICE_NAME,
        "SERVICE_NAME_UNDERSCORE" : SERVICE_NAME.replace("-","_") if "-" in SERVICE_NAME else SERVICE_NAME,
        "ORG_ID" : ORG_ID,
        "PROJECT_ID" : PROJECT_ID,
        "TEMPLATE_ID" : TEMPLATE_ID
    }

    print(Padding(f"Creating pipeline for: [i bold]{SERVICE_NAME}[/i bold] :slightly_smiling_face:", 1))
    description = Padding(f"Creating pipeline for: [i bold]{SERVICE_NAME}[/i bold] :slightly_smiling_face:", 1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        progress.add_task(description="Progresing...", total=None)
        template.create_files(template_values)
        response = harness_api.create_pipeline(template_values)

    if response.status_code > 200 and response.status_code < 400:
        print(Padding(f"[i bold]Done[/i bold] ✅", 1))
    else:
        error_msg = Text(response.json().get("message"))
        error_msg.stylize("bold red")
        print(Padding("[red bold]Error[/red bold] 😵", (0, 1)))
        print(Padding(error_msg, (0, 1)))
