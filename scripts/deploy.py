import click
from ape import project
from ape.cli import (
    ape_cli_context,
    get_user_selected_account,
    network_option,
    NetworkBoundCommand,
)


@click.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
def cli(cli_ctx, network):
    network = cli_ctx.provider.network.name
    if network == "local" or network.endswith("-fork"):
        account = cli_ctx.account_manager.test_accounts[0]
    else:
        account = get_user_selected_account()

    account.deploy(project.WETH9)
