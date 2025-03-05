import streamlit as st
import random
from streamlit_ace import st_ace
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_custom_embedding
from QAWithPDF.model_api import load_model  # Only import load_model here
from QAWithPDF.utils import get_learning_path_recommendations  # Import the utility function from llm_utils

# List of 50 coding questions and answers based on Striver's sheet
test_questions = {
    "What is the output of print(2 + 3)?": "5",
    "What is the syntax for a for loop in Python?": "for i in range(5):",
    "How do you create a list in Python?": "list_name = []",
    "What is the use of the 'break' statement in Python?": "To exit a loop prematurely",
    "How do you check the length of a list in Python?": "len(list_name)",
    "What is the difference between '==' and 'is' in Python?": "'==' checks for value equality, 'is' checks for identity",
    "How do you create a dictionary in Python?": "dict_name = {}",
    "What is the use of the 'continue' statement in Python?": "To skip the rest of the code inside a loop for the current iteration",
    "How do you create a set in Python?": "set_name = set()",
    "What is the use of the 'pass' statement in Python?": "To indicate an empty block of code",
    "How do you create a tuple in Python?": "tuple_name = ()",
    "What is the difference between a list and a tuple in Python?": "Lists are mutable, tuples are immutable",
    "How do you check if an item exists in a list in Python?": "item in list_name",
    "How do you create a function in Python?": "def function_name():",
    "What is the use of the 'return' statement in Python?": "To return a value from a function",
    "How do you create a class in Python?": "class ClassName:",
    "What is inheritance in Python?": "A mechanism to create a new class using an existing class",
    "How do you handle exceptions in Python?": "Using try-except blocks",
    "What is the use of the 'finally' block in Python?": "To execute code regardless of whether an exception occurs or not",
    "How do you open a file in Python?": "open('file_name')",
    "How do you read from a file in Python?": "file.read()",
    "How do you write to a file in Python?": "file.write('text')",
    "What is a module in Python?": "A file containing Python code that can be imported",
    "How do you import a module in Python?": "import module_name",
    "What is a package in Python?": "A collection of modules",
    "How do you install a package in Python?": "pip install package_name",
    "What is the use of the 'with' statement in Python?": "To wrap the execution of a block of code within methods defined by a context manager",
    "How do you create a virtual environment in Python?": "python -m venv env_name",
    "What is the use of the 'lambda' function in Python?": "To create small anonymous functions",
    "How do you sort a list in Python?": "list.sort()",
    "What is the difference between 'sort()' and 'sorted()' in Python?": "'sort()' modifies the list in place, 'sorted()' returns a new sorted list",
    "How do you reverse a list in Python?": "list.reverse()",
    "How do you iterate over a list in Python?": "for item in list_name:",
    "What is the use of the 'enumerate()' function in Python?": "To iterate over a list with an index",
    "How do you zip two lists together in Python?": "zip(list1, list2)",
    "What is a generator in Python?": "A function that returns an iterator",
    "How do you create a generator in Python?": "Using 'yield' statement",
    "What is the use of the 'map()' function in Python?": "To apply a function to all items in an iterable",
    "What is the use of the 'filter()' function in Python?": "To filter items in an iterable",
    "How do you create a list comprehension in Python?": "[expression for item in iterable]",
    "What is the use of the 'reduce()' function in Python?": "To apply a rolling computation to sequential pairs of values in an iterable",
    "How do you create a set comprehension in Python?": "{expression for item in iterable}",
    "What is the use of the 'any()' function in Python?": "To check if any element in an iterable is true",
    "What is the use of the 'all()' function in Python?": "To check if all elements in an iterable are true",
    "How do you create a dictionary comprehension in Python?": "{key: value for item in iterable}",
    "What is the use of the 'zip()' function in Python?": "To combine two or more iterables into a single iterable of tuples",
    "How do you create a nested dictionary in Python?": "nested_dict = {key: {nested_key: nested_value}}",
    "What is the use of the 'setdefault()' method in Python?": "To get the value of a key in a dictionary and set it if it doesn't exist",
    "How do you create a frozenset in Python?": "frozenset(iterable)"
}

# Coding questions and expected outputs
coding_questions = {
    "Write a Python function to check if a number is prime.": """
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
    """,
    "Write a Python function to find the factorial of a number.": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    """
}

# Function to randomly select questions
def get_random_questions(num_questions=5):
    return random.sample(list(test_questions.items()), num_questions)  # Convert to list

# Function to randomly select coding questions
def get_random_coding_question():
    return random.choice(list(coding_questions.items()))  # Convert to list

# Function to assess user and provide feedback
def assess_user(test_results):
    score = 0
    feedback = []
    for question, answer in test_results.items():
        if question == "Code":
            continue  # Skip the coding question
        if test_questions[question] == answer:
            score += 1
            feedback.append(f"Correct: {question}")
        else:
            feedback.append(f"Incorrect: {question}. Expected: {test_questions[question]}")
    level = "Beginner" if score <= 1 else "Intermediate" if score <= 3 else "Advanced"
    return level, feedback

# Function to evaluate coding answer
def evaluate_code_answer(user_code, expected_code):
    # Basic comparison (could be improved with more sophisticated analysis)
    return user_code.strip() == expected_code.strip()

# Streamlit app
def main():
    st.set_page_config("QA with Documents")
    st.title("Generative AI Learning Path")

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose Page", ["Home", "Assessment", "QA with Documents"])

    # Home page
    if page == "Home":
        st.write("Welcome to the Generative AI Learning Path!")
        st.write("Navigate to the 'Assessment' page to take the test and get your personalized learning path.")

    # Assessment page
    elif page == "Assessment":
        st.write("### Take the Test")
        questions = get_random_questions()
        user_results = {}
        for question, _ in questions:
            user_results[question] = st.text_input(question)
        
        st.write("### Coding Challenge")
        coding_question, expected_code = get_random_coding_question()
        st.write(coding_question)
        user_code = st_ace(language='python', theme='monokai', height=200)

        if st.button("Submit"):
            user_results["Code"] = user_code
            user_level, feedback = assess_user(user_results)
            if evaluate_code_answer(user_code, expected_code):
                feedback.append(f"Correct: {coding_question}")
            else:
                feedback.append(f"Incorrect: {coding_question}. Expected: {expected_code}")

            learning_path = get_learning_path_recommendations(user_level)

            st.write(f"*User Level:* {user_level}")
            st.write("*Feedback:*")
            for fb in feedback:
                st.write(f"- {fb}")

            st.write("*Suggested Learning Path:*")
            for step in learning_path:
                st.write(f"- {step}")

            st.write("You can now proceed to the 'QA with Documents' section.")

    # QA with Documents page
    
            # QA with Documents page
    elif page == "QA with Documents":
        st.header("QA with Documents (Information Retrieval)")
        
        doc = st.file_uploader("Upload your document")
        
        user_question = st.text_input("Ask your question")
        
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                document = load_data(doc)
                model = load_model()
                query_engine = download_gemini_embedding(model, document)
                
                response = query_engine.query(user_question)
                
                st.write(response.response)

if _name_ == "_main_":
    main()
