import requests, json, os.path, time

MAX_FOLLOWERS = 1000
RATE_LIMIT = 1
DATA_FILE_PATH = "data.json"
DATA_FILE_STRUCTURE = {"players": []}

def init_data_file(file):
	json.dump(DATA_FILE_STRUCTURE, file)

def jprint(obj):
	# create a formatted string of the Python JSON object
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

def load_ids(data):
	ids = set()
	for player in data:
		ids.add(player["id"])
	return ids

# API Call functions
def get_person(id):
	response = requests.get(f"https://lichess.org/api/user/{id}")
	if response.status_code == 200:
		return response.json()
	else:
		return None

def get_followers(id):
	response = requests.get(f"https://lichess.org/api/user/{id}/followers")
	if response.status_code == 200:
		followers = []
		for user in response.iter_lines():
			followers.append(json.loads(user))
		return followers
	else:
		return None

# Data functions
def insert_person(person, players, ids):
	if person["id"] not in ids and person.get("title", "") is not "BOT":
		players.append(person)
		ids.add(person["id"])
		return True
	else:
		return False

def retrieve_id(id, players):
	for player in players:
		if player["id"] == id:
			return player
	return None
	
def main():
	# Check for existence of file
	print("Checking existence of file at " + os.path.realpath("") + DATA_FILE_PATH)
	if os.path.exists(DATA_FILE_PATH):
		print("File exists.")
	else:
		print("File doesn't exist.")
		# Request permission to create new file if non-existant
		if input("Create data.json (y/n)? ") == 'y':
			init_data_file(open("data.json", "w"))
			print("New data file created.")
		else:
			return
	
	# Retrieve data from file
	with open(DATA_FILE_PATH, "r") as data_file:
		data = json.load(data_file)
	
	players = data["players"]
	ids = load_ids(players)
	
	while True:
		command = input("Enter input: ")
		if command == 'q':
			break
		elif command == 'list':
			print(ids)
		elif command == 'id':
			person = retrieve_id(input("Enter id: "), players)
			if person is not None:
				print(json.dumps(person, sort_keys=True, indent=4))
			else:
				print("Invalid id.")
		elif command == 'add':
			person = get_person(input("Enter id: "))
			if person is not None:
				insert_person(person, players, ids)
			else:
				print("Invalid id.")
		elif command == 'followers':
			followers = get_followers(input("Enter id: "))
			for follower in followers:
				insert_person(follower, players, ids)
		elif command == 'recursive_followers':
			count = 0
			visited = set()
			limit = int(input("Enter limit: "))
			queue = [get_person(input("Enter id: "))]
			while queue and count <= limit:
				person = queue.pop(0)
				if person is not None and person.get("nbFollowers", 0) <= MAX_FOLLOWERS:
					followers = get_followers(person["id"])
					for follower in followers:
						if insert_person(follower, players, ids):
							count += 1
						if follower["id"] not in visited:
							queue.append(follower)
					visited.add(person["id"])
					time.sleep(RATE_LIMIT)
		elif command == 's':
			with open(DATA_FILE_PATH, "w") as data_file:
				data = json.dump(data, data_file)
		else:
			print("Invalid input.")

if __name__  == "__main__":
	main()