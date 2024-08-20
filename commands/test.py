import typer
import questionary
import src.harness.harness_api as harness_api

from rich import print
from rich.padding import Padding
from rich.progress import Progress, SpinnerColumn, TextColumn


app = typer.Typer()


@app.command()
def test_harness_api():

    org_id_list = list(harness_api.get_orgs().keys())

    questions = [
        {
            'type': 'text',
            'name': 'SERVICE_NAME',
            'message': "What's your service name"
        },
        {
            'type': 'select',
            'name': 'ORG_ID',
            'message': 'Select Oganization',
            'qmark': "🔎",
            'pointer': "👉",
            'choices': org_id_list
        },
        # {
        #     'type': 'select',
        #     'name': 'PROJECT_ID',
        #     'message': 'Select Project',
        #     'qmark': "🔎",
        #     'pointer': "👉",
        #     "when": lambda x: x["ORG_ID"] != "",
        #     'choices': "hols"
        # }
    ]

    answers = prompt(questions)
    projects = list(harness_api.get_projects_in_org(answers["ORG_ID"]).keys())

    print(projects)

    print(answers)

    # org_name_selected = questionary.select("Select organization:",choices=org_list,qmark="🔎",pointer="👉").ask()
    
    raise typer.Exit()

@app.command()
def test_interactive_input():
    
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
                                choices=[item['identifier'] for item in harness_api.get_templates_dir()]).ask()


    # SERVICE_NAME = 
    # print(SERVICE_NAME)
    #Dir with all substitutions in templates.
    template_values = {
        "SERVICE_NAME" : SERVICE_NAME,
        "SERVICE_NAME_UNDERSCORE" : SERVICE_NAME.replace("-","_") if "-" in SERVICE_NAME else SERVICE_NAME,
        "ORG_ID" : ORG_ID,
        "PROJECT_ID" : PROJECT_ID,
        "TEMPLATE_ID" : TEMPLATE_ID
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Creating pipeline...", total=None)
        response = harness_api.create_pipeline(template_values)
    
    if response.status_code > 200 and response.status_code < 400:
        print(Padding(f"[i bold]Done[/i bold] ✅", 1))
    else:
        import sys
        sys.stderr.write()
        sys.stdout.write()
        print("fatal error", file=sys.stderr)


    