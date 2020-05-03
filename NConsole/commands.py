from NConsole.console import ConsoleLogType
from os import path
import json

# Overriden by a class that handle a command
class Command:
	# Initialize a command
	def __init__(self, command: str, help_message: str, aliases=[], subcommands=[], args_accepted=[]):
		self.command = command  # The command you have to type
		self.help_message = help_message  # A description of the command
		self.aliases = aliases  # You can also write this to trigger on_command()
		self.subcommands = subcommands  # Useful for help commands
		self.args_accepted = args_accepted  # Useful for help commands
		self.vars_to_save = {}

	# vars_to_save must be a dict with key as name, and value as your var
	def set_vars_to_save(self, vars_to_save):
		self.vars_to_save = vars_to_save
	
	# Called by CommandsRegister, don't override
	def save_all(self):
		if self.vars_to_save:  # If there are vars to be saved
			file_json = open(f"{self.command}.json", "w+")
			json.dump(self.vars_to_save, file_json, indent=4)
			file_json.close()
	
	# Get data from file and save it to the right variables
	def get_savings(self):
		if self.vars_to_save:
			file_json = open(f"{self.command}.json", "r")
			data = json.load(file_json)  # Load data from the file
			file_json.close()
			for key in self.vars_to_save.keys():  # Iterate over all names of the vars that as been saved
				setattr(self, key, data[key])  # and set their value

	# You have to override this, here you handle your commands
	# ATTENTION: the first statement has to be args = args[0] or else it will be bugged
	def on_command(self, *args):
		pass


# Is a register of all commands
class CommandsRegister:
	# Initialize the class
	def __init__(self):
		self.commands = []

	# You have to pass your own command class that handles a command
	def register_command(self, command: Command):
		self.commands.append(command)

	# Return a Command from a command name, not alias
	def get_command_from_command_name(self, command_name: str) -> Command:
		for command in self.commands:
			if command_name == command.command:
				return command
	
	# Calls save_all() of all commands registered
	def save_all(self):
		for command in self.commands:
			command.save_all()
	
	# Calls get_savings() of all commands registered
	def get_savings(self):
		for command in self.commands:
			command.get_savings()

	# Called by Console, it handles input and calls on_command() of the right class
	def check_input(self, input_check: str):
		input_check = input_check.lower()  # Console is insesitive case
		input_check_splitted = input_check.split(" ")  # Split commands from other arguments
		command_name = input_check_splitted[0]  # This is the command you have typed
		args = input_check_splitted[1:]  # These are other arguments
		error_command = 0  # Useful to check if a command is valid
		max_error = 0  # Same as above
		for command in self.commands:  # Iterate over all commands that have been registered
			if not command.aliases:  # Check wether a command has aliases
				max_error += 1
				if command_name == command.command:  # If you have typed a command
					if not args:  # and you didn't pass arguments
						command.on_command()  # triggers on_command of the right class without arguments
					else:  # and you passed arguments
						command.on_command(args)  # triggers on_command of the right class with those arguments
			else:  # If command has aliases
				for alias in command.aliases:  # Iterate over all of those aliases
					max_error += 1
					if command_name == command.command or command_name == alias:  # Check wether you typed a command or an aliases
						if not args:  # if you didn't pass arguments
							command.on_command()  # triggers on_command of the right class without arguments
						else:  # and you passed arguments
							command.on_command(args)  # triggers on_command of the right class with those arguments
					else:
						error_command += 1
		if error_command == max_error:  # if you haven't typed a command (or alias), then
			print(f"\033[91m[ERROR] {command_name} is an invalid command")  # report user that that command (or alias) is inexistent
