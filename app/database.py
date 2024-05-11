from pymongo import MongoClient


# Define a function to get the database and tasks collection
def get_database():

	# Connect to MongoDB server running on localhost at default port 27017
	db_client = MongoClient('localhost', 27017)

	# Access or create a database named "mydatabase"
	mydb = db_client["mydatabase"]

	# Access or create a collection named "tasks" within the "mydatabase" database
	tasks = mydb["tasks"]

	# Return references to the database and the tasks collection
	return mydb,tasks

# Define a function to add a task to the tasks collection in the database
def add_task_db(tasks,task_id,task_name, task_details,user_id):
	task_dict = {"_id":task_id, "title": task_name, "description": task_details, "user":user_id}
	tasks.insert_one(task_dict)

# Define a function to delete a task from the tasks collection in the database
def delete_task_db(tasks, task_id, user_id):
	task_dict = {"_id":task_id, "user":user_id}
	tasks.delete_one(task_dict)

#Define a function to fetch tasks associated with a specific user from the tasks collection in the database
def fetch_task_db(tasks, user_id):
	task_dict = {"user":user_id}
	task_list = tasks.find(task_dict)

	return list(task_list)





