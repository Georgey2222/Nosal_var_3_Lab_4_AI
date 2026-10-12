from Models.Game.game import Game
from Commands.CommandProcessor.command_processor import CommandProcessor

commands = CommandProcessor(Game(10))

while True:
    command = input("> ").strip()
    if not commands.execute(command):
        break
