import os
import sys
import openai

def generate_with_retries(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:kexjobbars:third-times-the-charm:AM0eLhOv",
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating task description: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def parse_exercise_details(details):
    if details:
        parts = details.split(",")
        difficulty = parts[0].strip()
        skills = parts[1].strip() if len(parts) > 1 else "None"
        custom_prompt = parts[2].strip() if len(parts) > 2 else "General programming exercise"
        return difficulty, skills, custom_prompt
    return None, None, None

def generate_task_description(api_key, number_of_exercises, language, programming_language, *exercise_details):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    openai.api_key = api_key

    # Prepare modular prompts for each exercise considering difficulty level, language, and skill maps
    exercise_details_formatted = []
    for i, details in enumerate(exercise_details):
        difficulty, skills, custom_prompt = parse_exercise_details(details)
        if difficulty and skills and custom_prompt:
            prompt_section = f"Exercise {i+1}: Prompt: {custom_prompt}, Difficulty: {difficulty}, Skills: {skills}\n\n"
            if difficulty == "simple":
                prompt_section += (
                    "Focus on introductory concepts for beginners using basic applications of the skills. "
                    "Provide slight hints with code snippets in {programming_language}.\n"
                )
            elif difficulty == "medium":
                prompt_section += (
                    "Push students to apply skills in moderately challenging scenarios. "
                    "Include hints with short code snippets in {programming_language}, relevant to real-world applications.\n"
                )
            elif difficulty == "hard":
                prompt_section += (
                    "Challenge students with complex problems requiring deeper understanding of skills. "
                    "Provide structured hints via code snippets in {programming_language} that guide without solving.\n"
                )
            elif difficulty == "v.hard":
                prompt_section += (
                    "Present highly challenging, multi-step problems combining multiple skills. "
                    "Hints should be minimal but provide a base structure in {programming_language} to support advanced problem-solving.\n"
                )

            exercise_details_formatted.append(prompt_section.format(programming_language=programming_language))

    if not exercise_details_formatted:
        print("No valid exercises were provided.")
        sys.exit(1)

    # Modular prompt that integrates learning goals and custom prompts for specificity
    messages = [
        {
            "role": "system",
            "content": (
                "You are a highly experienced programming instructor creating exercises for a university-level programming lab. "
                "Each exercise should be challenging, educationally valuable, and focus on developing programming skills in the specified language."
                "Include brief, non-solution code snippets in each exercise as minor hints in the chosen language. "
                "These snippets should provide minimal structure to help approach the task without revealing the answer."
            )
        },
        {
            "role": "user",
            "content": f"Generate {number_of_exercises} exercises in {programming_language} following these custom details:\n\n" +
                       "\n".join(exercise_details_formatted) +
                       "\n\nEach exercise should require students to apply critical thinking and problem-solving skills."
        }
    ]

    task_description = generate_with_retries(openai, messages)
    if not task_description:
        print("Failed to generate task description.")
        sys.exit(1)

    # Write the task description to a markdown file
    with open("tasks/new_task.md", "w") as f:
        f.write("### Task Description\n\n")
        f.write(task_description)

    print("Task description generated successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: exercise_description.py <api_key> <number_of_exercises> <language> <programming_language> <exercise_1_details> [<exercise_2_details> ...]")
        sys.exit(1)

    api_key = sys.argv[1]
    number_of_exercises = sys.argv[2]
    language = sys.argv[3]
    programming_language = sys.argv[4]
    exercise_details = sys.argv[5:]

    generate_task_description(api_key, number_of_exercises, language, programming_language, *exercise_details)
