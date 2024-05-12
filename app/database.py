from pymongo import MongoClient



# Define a function to get the database and tasks collection
def get_database():
	global db_client, mydb, tasks, comments, db_name
	# Connect to MongoDB server running on localhost at default port 27017
	db_client = MongoClient('localhost', 27017)
	db_name = "mydatabase"

	# Access or create a database named "mydatabase"
	mydb = db_client[db_name]

	# Access or create a collection named "tasks" within the "mydatabase" database
	tasks = mydb["tasks"]

	# Return references to the database and the tasks collection
	return mydb

# Define a function to add a task to the tasks collection in the database
def add_task_db(mydb, task_id,task_name, task_details, due, user_id):
	task_dict = {"_id":task_id, "title": task_name, "notes": task_details, "due": due, "user": user_id}
	if len(list(tasks.find(task_dict))) == 0:
		mydb.tasks.insert_one(task_dict)
	else:
		print("task already exists")

# Define a function to delete a task from the tasks collection in the database
def delete_task_db(mydb, task_id, user_id):
	task_dict = {"_id":task_id, "user": user_id}
	if len(list(tasks.find(task_dict))) > 0:
		mydb.tasks.delete_one(task_dict)
	else:
		print("task does not exists")

#Define a function to update tasks associated with a specific user from the tasks collection in the database
def update_task_db(mydb, tasks, user_id):
    for task in tasks:
        print(task)
        task_dict = {"_id": task["id"], "user": user_id}
        update_data = {"$set": {
            "title": task["title"], 
            "notes": task.get("notes"),  # Use empty string as default if 'notes' is not provided
            "due": task.get("due")  # Use None as default if 'due' is not provided
        }}
        
        # The update_one method will update the document if it exists, or insert it if it does not (upsert=True)
        result = mydb.tasks.update_one(task_dict, update_data, upsert=True)
        
        # You can print the result of the update to check how many documents were matched and modified
        print(f"Documents matched: {result.matched_count}, Documents modified: {result.modified_count}")

#Define a function to fetch tasks associated with a specific user from the tasks collection in the database
def fetch_task_db(mydb, user_id):
	task_dict = {"user":user_id}
	task_list = mydb.tasks.find(task_dict)
	result = list(task_list)
	return result[::-1]




