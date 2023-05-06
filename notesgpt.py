import openai
import textwrap
import argparse
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_gpt_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert content summarizer with an MBA from Harvard."},
                  {"role": "user", "content": f"Please summarize the following text, only use the highst-value points based on an audience interested in careers, leadership, and building trust. Include the beginning timestamp at the start of the summary: {text}"}],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.2,
    )
    print(response.choices[0].message['content'].strip())
    return response.choices[0].message['content'].strip()

def generate_podcast_notes(summary):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert content summarizer and show notes writer."},
                  {"role": "user", "content": (
                      f"Generate podcast show notes for an audience of knowledge workers over 21 years old, "
                      f"interested in careers, leadership, teamwork, and trust "
                      f"create a title, subtitle, and 4 sentence summary at the beginning covering what the episode is about "
                      f"followed by a bulleted list of up to 20 points. keep each key point at 1 sentence "
                      f"At the very end, create bullets of chapter titles using 4 words or less based on key points with starting timestamp {summary}"
                  )}],
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.2,
    )
    return response.choices[0].message['content'].strip()


def process_text(input_text, max_chunk_length=2048):
    chunks = textwrap.wrap(input_text, max_chunk_length)
    return chunks

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove extra spaces and line breaks
    content = ' '.join(content.split())

    return content


def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    # Setup argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Generate podcast show notes from a text file.")
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument("output_file", help="Path to the output file.")
    args = parser.parse_args()

    # Read the input text from the specified file
    input_text = read_file(args.input_file)

    # Break the input text into smaller chunks
    text_chunks = process_text(input_text)

    # Get the GPT summary for each chunk
    summarized_chunks = [get_gpt_summary(chunk) for chunk in text_chunks]

    # Combine the summarized chunks into a single summary
    consolidated_summary = " ".join(summarized_chunks)

    # Generate podcast show notes based on the consolidated summary
    podcast_show_notes = generate_podcast_notes(consolidated_summary)

    # Write the podcast show notes to the specified output file
    write_file(args.output_file, podcast_show_notes)

    print("Podcast show notes have been written to:", args.output_file)

if __name__ == "__main__":
    main()
