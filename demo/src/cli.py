"""
Mastering Object Oriented Design, 4ed.

A demo of the CLI.
"""

import click


@click.command()
@click.option("-p", "--player", default="Simple", help="Player Class")
def main(player):
    print(f"Player set to {player}")

if __name__ == "__main__":
    main()
