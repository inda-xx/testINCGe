import os
import sys
import openai

def generate_with_retries(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating solution: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def generate_solution(api_key, branch_name):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    openai.api_key = api_key

    # Task description
    task_file = f"tasks/new_task.md"
    if not os.path.exists(task_file):
        print(f"Error: Task description not found at {task_file}")
        sys.exit(1)

    with open(task_file, "r") as f:
        task_description = f.read()

    # Messages for chat model
    messages = [
        {
            "role": "system",
            "content": (
                "You are an experienced programming instructor creating a solution for the following task."
            )
        },
        {
            "role": "user",
            "content": f"Generate a solution for the following task:\n\n{task_description}"
        }
    ]

    # Generate solution with retries
    solution = generate_with_retries(openai, messages)
    if not solution:
        print("Failed to generate solution.")
        sys.exit(1)

    # Write the solution to a markdown file
    with open("tasks/solution.md", "w") as f:
        f.write("# Solution\n\n")
        f.write(solution)

    print("Solution generated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: solution_generation.py <api_key> <branch_name>")
        sys.exit(1)

    api_key = sys.argv[1]
    branch_name = sys.argv[2]

    generate_solution(api_key, branch_name)
