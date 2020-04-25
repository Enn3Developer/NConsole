from enum import Enum

# Various type of log
class ConsoleLogType(Enum):
	INFO = 1  # INFO = normal output
	WARN = 2  # WARN = something that has not to happen, but isn't fatal
	ERROR = 3  # ERROR = the name explains itself

class Console:
	# Initialize the console passing the input_prefix and the CommandsRegister
	def __init__(self, input_prefix: str, commands_register):
		self.input_prefix = f"\033[0m{input_prefix}"
		self.commands_register = commands_register

	# Update itself, you have to call it in a while True:
	def update(self):
		input_updated = input(self.input_prefix)
		self.commands_register.check_input(input_updated)

	# Use this instead of print()
	def log(self, type_log: ConsoleLogType, *args):
		message = ""
		if type_log == ConsoleLogType.INFO:
			message = "\033[92m[INFO] "
		elif type_log == ConsoleLogType.WARN:
			message = "\033[93m[WARNING] "
		else:
			message = "\033[91m[ERROR] "
		for arg in args:
			message = f"{message}{arg}"
		print(message)
