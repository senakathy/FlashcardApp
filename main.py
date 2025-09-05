# Empty list to store tasks (each task is a dictionary)
tasks = []

# Main loop – runs until user quits
while True:
    print("\nTo-Do List Menu:")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Mark task as done")
    print("4. Delete a task")
    print("5. Quit")
    
    choice = input("Enter your choice (1-5): ")
    
    if choice == '1':
        # Add a task
        task_description = input("Enter the task description: ")
        task = {
            'id': len(tasks) + 1,
            'description': task_description,
            'done': False
        }
        tasks.append(task)
        print(f"Task '{task_description}' added successfully!")
        
    elif choice == '2':
        # View tasks
        if not tasks:
            print("No tasks found!")
        else:
            print("\nYour tasks:")
            for task in tasks:
                status = "✓ Done" if task['done'] else "✗ Pending"
                print(f"{task['id']}. {task['description']} [{status}]")
                
    elif choice == '3':
        # Mark task as done
        if not tasks:
            print("No tasks to mark as done!")
        else:
            print("\nYour tasks:")
            for task in tasks:
                status = "✓ Done" if task['done'] else "✗ Pending"
                print(f"{task['id']}. {task['description']} [{status}]")
            
            try:
                task_id = int(input("Enter the task ID to mark as done: "))
                task_found = False
                for task in tasks:
                    if task['id'] == task_id:
                        if task['done']:
                            print("Task is already marked as done!")
                        else:
                            task['done'] = True
                            print(f"Task '{task['description']}' marked as done!")
                        task_found = True
                        break
                
                if not task_found:
                    print("Task ID not found!")
                    
            except ValueError:
                print("Please enter a valid number!")
                
    elif choice == '4':
        # Delete a task
        if not tasks:
            print("No tasks to delete!")
        else:
            print("\nYour tasks:")
            for task in tasks:
                status = "✓ Done" if task['done'] else "✗ Pending"
                print(f"{task['id']}. {task['description']} [{status}]")
            
            try:
                task_id = int(input("Enter the task ID to delete: "))
                task_found = False
                for i, task in enumerate(tasks):
                    if task['id'] == task_id:
                        deleted_task = tasks.pop(i)
                        print(f"Task '{deleted_task['description']}' deleted successfully!")
                        
                        # Reassign IDs to maintain sequential numbering
                        for j, remaining_task in enumerate(tasks):
                            remaining_task['id'] = j + 1
                        
                        task_found = True
                        break
                
                if not task_found:
                    print("Task ID not found!")
                    
            except ValueError:
                print("Please enter a valid number!")
        
    elif choice == '5':
        print("Goodbye!")
        break  # Exit the loop
        
    else:
        print("Invalid choice! Please enter a number between 1-5.")