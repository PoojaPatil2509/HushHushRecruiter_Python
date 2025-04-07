# import streamlit as st
# import contextlib
# import io
# import json

# # Problem statements for coding challenge
# questions = [
#     {
#         'statement': 'Missing number in array: Given an array of size N-1 such that it only contains distinct integers in the range of 1 to N. Find the missing element.',
#         'example': {'N': 5, 'A': [1, 2, 3, 5], 'Output': 4},
#     },
#     {
#         'statement': 'Number of pairs:Given two arrays X and Y of positive integers, find the number of pairs such that xy > yx (raised to power of) where x is an element from X and y is an element from Y.',
#         'example': {'M': 3, 'X': [2, 1, 6], 'N': 2, 'Y': [1, 5], 'Output': 3},
#     },
#     {
#         'statement': 'Minimum Platforms:Given arrival and departure times of all trains that reach a railway station. Find the minimum number of platforms required for the railway station so that no train is kept waiting.Consider that all the trains arrive on the same day and leave on the same day. Arrival and departure time can never be the same for a train but we can have arrival time of one train equal to departure time of the other. At any given instance of time, same platform can not be used for both departure of a train and arrival of another train. In such cases, we need different platforms.',
#         'example': {'n': 6, 'arr': [900, 940, 950, 1100, 1500, 1800], 'dep': [910, 1200, 1120, 1130, 1900, 2000], 'Output': 3},
#     },
# ]

# # Initialize session state
# if 'user_data' not in st.session_state:
#     st.session_state.user_data = []

# # Streamlit UI
# st.title('Code Evaluation System')

# # Display questions and text areas for user code input
# for i, q in enumerate(questions):
#     st.write(f"Question {i + 1}: {q['statement']}")
#     st.write(f"Example: {q['example']}")
#     user_code = st.text_area(f"Enter your Python code for Question {i + 1}:", height=300)

#     # Button to evaluate the code
#     if st.button(f'Run Code for Question {i + 1}'):
#         st.write("Executing your code...")

#         # Create a function to encapsulate the user's code
#         def execute_user_code():
#             try:
#                 exec(user_code)
#             except Exception as e:
#                 st.error(f"Error during execution: {str(e)}")

#         # Capture the standard output
#         captured_output = io.StringIO()
#         with contextlib.redirect_stdout(captured_output):
#             execute_user_code()

#         # Get the user's output and expected output
#         user_output = captured_output.getvalue().strip()
#         expected_output = str(q['example']['Output']).strip()

#         # Compare the output with the expected output
#         if user_output == expected_output:
#             st.success("Correct Answer!")
#             is_correct = True
#         else:
#             st.error(f"Incorrect Answer. Expected: {expected_output}, Got: {user_output}")
#             is_correct = False

#         # Save user data
#         st.session_state.user_data.append({
#             'question': q['statement'],
#             'user_code': user_code,
#             'is_correct': is_correct
#         })

# if st.button("Submit Coding Assessment"):
#     st.write("Submitting Coding Assessment...")

#     # Save data to a JSON file (you may use a database in a real-world scenario)
#     file_path = 'user_data.json'
#     with open(file_path, 'w') as file:
#         json.dump(st.session_state.user_data, file)


import streamlit as st
import contextlib
import io
import csv

st.session_state.setdefault('show_review', False)

# Define the questions and examples
questions = [
    {
        'statement': 'Missing number in array: Given an array of size N-1 such that it only contains distinct integers in the range of 1 to N. Find the missing element.',
        'example': {'N': 5, 'A': [1, 2, 3, 5], 'Output': 4},
    },
    {
        'statement': 'Number of pairs:Given two arrays X and Y of positive integers, find the number of pairs such that xy > yx (raised to power of) where x is an element from X and y is an element from Y.',
        'example': {'M': 3, 'X': [2, 1, 6], 'N': 2, 'Y': [1, 5], 'Output': 3},
    },
    {
        'statement': 'Minimum Platforms:Given arrival and departure times of all trains that reach a railway station. Find the minimum number of platforms required for the railway station so that no train is kept waiting.Consider that all the trains arrive on the same day and leave on the same day. Arrival and departure time can never be the same for a train but we can have arrival time of one train equal to departure time of the other. At any given instance of time, same platform can not be used for both departure of a train and arrival of another train. In such cases, we need different platforms.',
        'example': {'n': 6, 'arr': [900, 940, 950, 1100, 1500, 1800], 'dep': [910, 1200, 1120, 1130, 1900, 2000], 'Output': 3},
    },
]

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = []

# Define a function to change the view to review interface
def show_review_interface():
    # Set the session state to trigger review interface display
    st.session_state.show_review = True
    # Rerun the app to reflect the changes in the UI
    st.experimental_rerun()

# Function to execute user's code
def execute_user_code(code):
    try:
        with contextlib.redirect_stdout(io.StringIO()) as captured_output:
            exec(code)
        return captured_output.getvalue().strip(), True
    except Exception as e:
        return str(e), False

# Function to display review interface
def review_interface():
    st.title("Review Candidate Answers")
    # Create a CSV file and write the data
    with open('user_data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['question', 'user_code', 'is_correct'])
        writer.writeheader()
        
        for idx, user_data in enumerate(st.session_state.user_data):
            writer.writerow(user_data)
            st.subheader(f"Question {idx + 1}")
            st.text_area(f"Answer for Question {idx + 1}:", value=user_data['user_code'], height=150, key=f"answer_{idx}", disabled=True)

    # Move the Select and Reject buttons outside the loop to have them only once
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Select"):
            st.success("Selected.")
    with col2:
        if st.button("Reject"):
            st.error("Rejected.")


# Streamlit UI for the main page
def show_main_interface():
    st.title('Code Evaluation System')
    temp_user_data = []
    
    for i, q in enumerate(questions):
        st.write(f"Question {i + 1}: {q['statement']}")
        st.write(f"Example: {q['example']}")
        user_code = st.text_area("Enter your Python code for Question {i + 1}:", height=300, key=f"code_{i}")
        temp_user_data.append({'question': q['statement'], 'user_code': user_code, 'is_correct': None})

    if st.button("Submit Coding Assessment"):
        for i, q in enumerate(questions):
            user_code = st.session_state[f"code_{i}"]
            expected_output = str(q['example']['Output']).strip()
            output, success = execute_user_code(user_code)
            is_correct = output == expected_output
            temp_user_data[i]['is_correct'] = is_correct
            
            if success:
                if is_correct:
                    st.success(f"Question {i + 1}: Correct Answer!")
                else:
                    st.error(f"Question {i + 1}: Incorrect Answer. Expected: {expected_output}, Got: {output}")
            else:
                st.error(f"Question {i + 1}: Error during execution: {output}")

        st.session_state.user_data = temp_user_data
        show_review_interface()

# Decide which interface to display based on the state
if st.session_state.show_review:
    review_interface()
else:
    show_main_interface()