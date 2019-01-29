from invoke import task

PROJECT_DIRECTORY = "cloudkeeper_os"
TEST_DIRECTORY = "tests"
CURRENT_DIRECTORY = "."


@task
def acceptance(c):
    acceptance_commands = [
        "flake8",
        f"pylint {PROJECT_DIRECTORY} {TEST_DIRECTORY}",
        "safety check --bare",
        f"bandit -r {CURRENT_DIRECTORY}",
    ]

    for command in acceptance_commands:
        command_name = command.split(" ")[0]
        print(f"Running {command_name}")
        c.run(command)
        print(f"Done {command_name}")


@task
def test(c):
    c.run("pytest --color=yes")
