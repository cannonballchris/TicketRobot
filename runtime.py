import asyncio
import os
import pkgutil

package_list = ["discord", "dotenv", "chat_exporter"]
def load_package():
	print("___________________________")
	print("Package Manager")
	for package in package_list:
		if pkgutil.find_loader(package) is None:
			print("Modules probably not installed...running installer....")
			os.system("pip install -r requirements.txt")
		else:
			print(f"Package {package} is already installed.")
	print("___________________________")
load_package()
from dotenv import load_dotenv
from main import TicketBot
load_dotenv()
TOKEN = os.getenv("TOKEN")

def run_main():
	TicketBot().run(TOKEN)

if __name__ == "__main__":
	asyncio.run(run_main())