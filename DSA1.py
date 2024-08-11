import tkinter as tk  # Import the tkinter library for creating the graphical user interface (GUI)
from tkinter import simpledialog, messagebox, filedialog  # Import specific functions for dialogs and file operations
import random  # Import the random library to generate random numbers
import csv  # Import the csv library to read and write CSV files
import os  # Import the os library to interact with the operating system

class QuestionBank:
    def __init__(self):
        # Initialize the QuestionBank object with empty data structures
        self.questions = {}  # A dictionary to store questions by their unique IDs
        self.topics = {}  # A dictionary to keep track of which question IDs are associated with each topic
        self.difficulty_levels = {}  # A dictionary to keep track of which question IDs are associated with each difficulty level

    def add_question(self, question_id, question, topic, difficulty):
        # Add a new question to the question bank
        self.questions[question_id] = {'question': question, 'topic': topic, 'difficulty': difficulty}

        # Update the topics dictionary to include the new question ID
        if topic not in self.topics:
            self.topics[topic] = set()  # Create a new set for this topic if it does not exist
        self.topics[topic].add(question_id)  # Add the question ID to the set for this topic

        # Update the difficulty_levels dictionary to include the new question ID
        if difficulty not in self.difficulty_levels:
            self.difficulty_levels[difficulty] = set()  # Create a new set for this difficulty level if it does not exist
        self.difficulty_levels[difficulty].add(question_id)  # Add the question ID to the set for this difficulty level

    def update_question(self, question_id, question=None, topic=None, difficulty=None):
        # Update an existing question's details
        if question_id in self.questions:
            if question:
                self.questions[question_id]['question'] = question  # Update the question text if a new one is provided
            if topic:
                old_topic = self.questions[question_id]['topic']
                # Remove the question from the old topic and add it to the new topic
                self.topics[old_topic].remove(question_id)
                if topic not in self.topics:
                    self.topics[topic] = set()  # Create a new set for the new topic if it does not exist
                self.topics[topic].add(question_id)  # Add the question ID to the set for the new topic
                self.questions[question_id]['topic'] = topic  # Update the topic for the question
            if difficulty:
                old_difficulty = self.questions[question_id]['difficulty']
                # Remove the question from the old difficulty level and add it to the new difficulty level
                self.difficulty_levels[old_difficulty].remove(question_id)
                if difficulty not in self.difficulty_levels:
                    self.difficulty_levels[difficulty] = set()  # Create a new set for the new difficulty level if it does not exist
                self.difficulty_levels[difficulty].add(question_id)  # Add the question ID to the set for the new difficulty level
                self.questions[question_id]['difficulty'] = difficulty  # Update the difficulty for the question
        else:
            print("Question not found.")  # Print a message if the question ID does not exist

    def search_questions(self, topics=None, difficulty_range=None):
        # Search for questions based on provided topics and difficulty levels
        result_ids = set(self.questions.keys())  # Start with all question IDs

        if topics:
            topic_ids = set()
            for topic in topics:
                topic_ids |= self.topics.get(topic, set())  # Combine all question IDs for the provided topics
            result_ids &= topic_ids  # Keep only those question IDs that are in the set of topic IDs

        if difficulty_range:
            difficulty_ids = set()
            for difficulty in difficulty_range:
                difficulty_ids |= self.difficulty_levels.get(difficulty, set())  # Combine all question IDs for the provided difficulties
            result_ids &= difficulty_ids  # Keep only those question IDs that are in the set of difficulty IDs

        return [self.questions[q_id] for q_id in result_ids]  # Return the details of the matching questions

    def delete_question(self, question_id):
        # Delete a question from the question bank
        if question_id in self.questions:
            question_info = self.questions.pop(question_id)  # Remove the question from the dictionary
            self.topics[question_info['topic']].remove(question_id)  # Remove the question ID from the topic set
            self.difficulty_levels[question_info['difficulty']].remove(question_id)  # Remove the question ID from the difficulty level set
            print(f"Question {question_id} deleted.")  # Print a message confirming deletion
        else:
            print("Question not found.")  # Print a message if the question ID does not exist

    def random_question(self, topic=None, difficulty=None):
        # Retrieve a random question based on optional topic and difficulty filters
        candidates = set(self.questions.keys())  # Start with all question IDs
        if topic:
            candidates &= self.topics.get(topic, set())  # Filter by the specified topic
        if difficulty:
            candidates &= self.difficulty_levels.get(difficulty, set())  # Filter by the specified difficulty

        if candidates:
            random_id = random.choice(list(candidates))  # Choose a random question ID from the filtered list
            return self.questions[random_id]  # Return the details of the selected question
        else:
            return None  # Return None if no questions match the filters

    def statistics(self):
        # Generate statistics about the question bank
        total_questions = len(self.questions)  # Count the total number of questions
        topic_distribution = {topic: len(ids) for topic, ids in self.topics.items()}  # Count questions per topic
        difficulty_distribution = {difficulty: len(ids) for difficulty, ids in self.difficulty_levels.items()}  # Count questions per difficulty level
        return {
            "total_questions": total_questions,  # Total number of questions
            "topic_distribution": topic_distribution,  # Distribution of questions by topic
            "difficulty_distribution": difficulty_distribution  # Distribution of questions by difficulty level
        }

    def save_to_file(self, filename):
        # Save all questions to a CSV file
        with open(filename, 'w', newline='') as file:  # Open the file in write mode
            writer = csv.writer(file)  # Create a CSV writer object
            writer.writerow(['ID', 'Question', 'Topic', 'Difficulty'])  # Write the header row
            for q_id, question in self.questions.items():
                # Write each question's details to the file
                writer.writerow([q_id, question['question'], question['topic'], question['difficulty']])

    def load_from_file(self, filename):
        # Load questions from a CSV file
        with open(filename, 'r', newline='') as file:  # Open the file in read mode
            reader = csv.reader(file)  # Create a CSV reader object
            next(reader)  # Skip the header row
            self.questions.clear()  # Clear the existing questions
            self.topics.clear()  # Clear the existing topics
            self.difficulty_levels.clear()  # Clear the existing difficulty levels
            for row in reader:
                q_id = int(row[0])  # Convert the ID to an integer
                question, topic, difficulty = row[1], row[2], row[3]  # Extract question details
                self.add_question(q_id, question, topic, difficulty)  # Add each question to the question bank

class QuestionBankGUI:
    def __init__(self, master, question_bank):
        self.master = master  # Reference to the main window
        self.question_bank = question_bank  # Reference to the QuestionBank instance
        
        self.master.geometry("900x600")  # Set the size of the window
        self.master.title("Question Bank Management")  # Set the title of the window
        self.master.configure(bg="#eaeaea")  # Set the background color of the window

        # Define colors for various UI elements
        self.primary_color = "#1abc9c"    # Bright teal color for primary elements
        self.secondary_color = "#34495e"  # Dark blue-gray color for secondary elements
        self.accent_color = "#e74c3c"     # Vivid red color for accents
        self.button_color = "#3498db"     # Bright blue color for buttons
        self.button_text_color = "#ffffff"  # White text color for buttons
        self.listbox_bg = "#ffffff"       # White background for the listbox
        self.listbox_fg = "#2c3e50"       # Dark text color for the listbox

        # Create and place frames within the main window
        self.main_frame = tk.Frame(master, bg=self.primary_color, padx=20, pady=20)
        self.main_frame.pack(pady=20, fill=tk.BOTH, expand=True)  # Pack the main frame with padding and expand to fill available space

        self.button_frame = tk.Frame(self.main_frame, bg=self.secondary_color, padx=10, pady=10)
        self.button_frame.pack(pady=10, fill=tk.X)  # Pack the button frame with padding and fill horizontally

        self.list_frame = tk.Frame(self.main_frame, bg=self.primary_color, padx=10, pady=10)
        self.list_frame.pack(pady=10, fill=tk.BOTH, expand=True)  # Pack the list frame with padding and expand to fill available space

        # Create buttons with improved styles and add them to the button frame
        self.create_button("Delete Question", self.delete_question_prompt).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.create_button("Add Question", self.add_question).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.create_button("Update Question", self.update_question_prompt).grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        self.create_button("Search Question", self.search_question_prompt).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.create_button("Random Question", self.random_question_prompt).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.create_button("Statistics", self.show_statistics).grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        self.create_button("Save", self.save_questions).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.create_button("Load", self.load_questions).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Create a Listbox with a scrollbar to display the list of questions
        self.questions_list = tk.Listbox(self.list_frame, bg=self.listbox_bg, fg=self.listbox_fg, font=("Helvetica", 12), selectbackground=self.accent_color, selectforeground=self.listbox_bg)
        self.scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.questions_list.yview)
        self.questions_list.config(yscrollcommand=self.scrollbar.set)
        
        self.questions_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Pack the listbox to the left side
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Pack the scrollbar to the right side

        self.refresh_questions()  # Refresh the listbox with the current questions

    def create_button(self, text, command):
        # Create a button with the specified text and command
        return tk.Button(self.button_frame, text=text, command=command, width=20, bg=self.button_color, fg=self.button_text_color, font=("Helvetica", 12, "bold"), relief="raised", borderwidth=2)

    def update_question_prompt(self):
        # Prompt the user to update an existing question
        question_id = simpledialog.askinteger("Input", "Enter the question ID to update:")  # Ask for the question ID
        if question_id in self.question_bank.questions:
            question = simpledialog.askstring("Input", "Enter the new question text (leave blank to keep current):")  # Ask for new question text
            topic = simpledialog.askstring("Input", "Enter the new topic (leave blank to keep current):")  # Ask for new topic
            difficulty = simpledialog.askstring("Input", "Enter the new difficulty (leave blank to keep current):")  # Ask for new difficulty level
            self.question_bank.update_question(question_id, question, topic, difficulty)  # Update the question in the bank
            self.refresh_questions()  # Refresh the listbox to show updated questions
            messagebox.showinfo("Success", f"Question {question_id} updated.")  # Show a success message
        else:
            messagebox.showerror("Error", "Question ID not found.")  # Show an error message if the ID is not found

    def search_question_prompt(self):
        # Prompt the user to search for questions based on topic and difficulty
        topics = simpledialog.askstring("Input", "Enter topics to search (comma-separated, leave blank if not searching by topic):")  # Ask for topics
        difficulty_range = simpledialog.askstring("Input", "Enter difficulty levels to search (comma-separated, leave blank if not searching by difficulty):")  # Ask for difficulty levels

        if topics:
            topics = [topic.strip() for topic in topics.split(",")]  # Split and strip the topic list
        else:
            topics = None  # If no topics are provided, set to None

        if difficulty_range:
            difficulty_range = [difficulty.strip() for difficulty in difficulty_range.split(",")]  # Split and strip the difficulty list
        else:
            difficulty_range = None  # If no difficulty levels are provided, set to None

        results = self.question_bank.search_questions(topics=topics, difficulty_range=difficulty_range)  # Search for questions
        if results:
            result_text = "\n".join([f"Question: {q['question']}, Topic: {q['topic']}, Difficulty: {q['difficulty']}" for q in results])  # Format the results
            messagebox.showinfo("Search Results", result_text)  # Show the search results in a message box
        else:
            messagebox.showinfo("Search Results", "No matching questions found.")  # Show a message if no results are found

    def random_question_prompt(self):
        # Prompt the user to get a random question based on optional filters
        topic = simpledialog.askstring("Input", "Enter the topic (leave blank for any topic):")  # Ask for a topic
        difficulty = simpledialog.askstring("Input", "Enter the difficulty level (leave blank for any difficulty):")  # Ask for a difficulty level

        question = self.question_bank.random_question(topic=topic, difficulty=difficulty)  # Get a random question
        if question:
            messagebox.showinfo("Random Question", f"Question: {question['question']}, Topic: {question['topic']}, Difficulty: {question['difficulty']}")  # Show the random question
        else:
            messagebox.showinfo("Random Question", "No matching questions found.")  # Show a message if no questions match

    def show_statistics(self):
        # Show statistics about the question bank
        stats = self.question_bank.statistics()  # Get the statistics
        stats_text = f"Total Questions: {stats['total_questions']}\n"  # Format the total number of questions
        stats_text += "Topic Distribution:\n"
        for topic, count in stats['topic_distribution'].items():
            stats_text += f"  {topic}: {count}\n"  # Format the distribution of questions by topic
        stats_text += "Difficulty Distribution:\n"
        for difficulty, count in stats['difficulty_distribution'].items():
            stats_text += f"  {difficulty}: {count}\n"  # Format the distribution of questions by difficulty
        messagebox.showinfo("Statistics", stats_text)  # Show the statistics in a message box

    def save_questions(self):
        # Save all questions to a CSV file
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save as")  # Ask for a filename to save
        if filename:
            self.question_bank.save_to_file(filename)  # Save the questions to the specified file
            messagebox.showinfo("Success", f"Questions saved successfully to {filename}.")  # Show a success message
        else:
            messagebox.showerror("Error", "Filename cannot be empty.")  # Show an error message if the filename is empty

    def load_questions(self):
        # Load questions from a CSV file
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Open file")  # Ask for a filename to open
        if filename:
            if os.path.exists(filename):
                self.question_bank.load_from_file(filename)  # Load the questions from the specified file
                self.refresh_questions()  # Refresh the listbox to show the loaded questions
                messagebox.showinfo("Success", f"Questions loaded successfully from {filename}.")  # Show a success message
            else:
                messagebox.showerror("Error", "File not found.")  # Show an error message if the file does not exist
        else:
            messagebox.showerror("Error", "Filename cannot be empty.")  # Show an error message if the filename is empty

    def refresh_questions(self):
        # Update the listbox to display the current questions
        self.questions_list.delete(0, tk.END)  # Clear the listbox
        for q_id, question in self.question_bank.questions.items():
            # Insert each question's details into the listbox
            self.questions_list.insert(tk.END, f"ID: {q_id}, Question: {question['question']}, Topic: {question['topic']}, Difficulty: {question['difficulty']}")

    def add_question(self):
        # Prompt the user to add a new question
        question = simpledialog.askstring("Input", "Enter the question:")  # Ask for the question text
        topic = simpledialog.askstring("Input", "Enter the topic:")  # Ask for the topic
        difficulty = simpledialog.askstring("Input", "Enter the difficulty level:")  # Ask for the difficulty level
        question_id = len(self.question_bank.questions) + 1  # Generate a new ID for the question
        self.question_bank.add_question(question_id, question, topic, difficulty)  # Add the new question to the question bank
        self.refresh_questions()  # Refresh the listbox to show the new question

    def delete_question_prompt(self):
        # Prompt the user to delete a question
        question_id = simpledialog.askinteger("Input", "Enter the question ID to delete:")  # Ask for the question ID
        if question_id in self.question_bank.questions:
            self.question_bank.delete_question(question_id)  # Delete the question from the bank
            self.refresh_questions()  # Refresh the listbox to reflect the deletion
            messagebox.showinfo("Success", f"Question {question_id} deleted.")  # Show a success message
        else:
            messagebox.showerror("Error", "Question ID not found.")  # Show an error message if the ID is not found

if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    question_bank = QuestionBank()  # Create a QuestionBank instance
    app = QuestionBankGUI(root, question_bank)  # Create the GUI with the question bank
    root.mainloop()  # Start the main event loop to run the application
