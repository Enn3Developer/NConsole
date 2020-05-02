from NConsole.commands import Command, CommandsRegister
from NConsole.console import Console, ConsoleLogType

commands_register = CommandsRegister()  # Initialize CommandsRegister
console = Console("> ", commands_register)  # Initialize Console


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help", "Type help to see this", aliases=["h"])  # Setup the command class
    
    def on_command(self, *args):
        message = ""  # Initialize the message to be printed
        for command in commands_register.commands:  # Iterate over all commands registered
            command_message = f"{command.command} -> {command.help_message}\n"  # Add command-specific information
            message = f"{message}{command_message}"  # Add those information to the message
        message = message[:-1]  # Get rid of the last \n
        console.log(ConsoleLogType.INFO, message)  # Use Console to print that message


def start():
    commands_register.register_command(HelpCommand())  # Register the command class


def main():
    start()
    while True:
        console.update()  # Update the console


if __name__ == "__main__":
    main()