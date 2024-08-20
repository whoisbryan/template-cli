import typer
import commands.pipeline as cli_pipeline
import commands.test as cli_test

app = typer.Typer(help=f"Awesome CLI by OCC Infra/SRE team. 🎯")
app.add_typer(cli_pipeline.app, name="pipeline", help="Create new Harness CI pipelines.")
app.add_typer(cli_test.app, name="test", help="test propurse.")


if __name__ == "__main__":
    app()
