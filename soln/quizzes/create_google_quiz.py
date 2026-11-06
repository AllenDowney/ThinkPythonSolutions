#!/usr/bin/env python3
"""
Create a Google Forms quiz from parsed quiz data.

This script creates a single quiz based on command-line arguments.
It checks if the quiz already exists and maintains mapping files for URLs.

Usage:
    python create_google_quiz.py --quiz "Chapter 1"
    python create_google_quiz.py --chapter 1
    python create_google_quiz.py --quiz "Think Python" --force
"""

import json
import argparse
import sys
import random
from pathlib import Path
from typing import Dict, Optional

# Add current directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from google_utils import (
    load_credentials, get_forms_service, get_services,
    create_quiz_form, add_quiz_questions_batch,
    move_form_to_folder, get_form_urls, add_intro_text_item
)


# Drive folder ID for Think Python quizzes
QUIZZES_FOLDER_ID = '1NqmWKV6EV1SozzRX5d-sm_j8pdXzZ5LS'


def load_parsed_quizzes(quizzes_file: str) -> list:
    """Load parsed quizzes from JSON file."""
    with open(quizzes_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_quiz(quizzes: list, title: Optional[str] = None, 
              chapter: Optional[int] = None) -> Optional[Dict]:
    """
    Find a quiz by title or chapter number.
    
    Parameters:
    -----------
    quizzes : list
        List of quiz dictionaries
    title : str, optional
        Quiz title to search for
    chapter : int, optional
        Chapter number (1-18) to search for
    
    Returns:
    --------
    dict : Quiz dictionary or None if not found
    """
    if chapter is not None:
        # Search for "Chapter N" format
        title = f"Chapter {chapter}"
    
    if title:
        for quiz in quizzes:
            if quiz['title'].lower() == title.lower():
                return quiz
    
    return None


def load_url_mappings(edit_urls_file: str, responder_urls_file: str) -> tuple:
    """
    Load URL mapping files.
    
    Returns:
    --------
    tuple : (edit_urls_dict, responder_urls_dict)
    """
    edit_urls = {}
    responder_urls = {}
    
    if Path(edit_urls_file).exists():
        with open(edit_urls_file, 'r', encoding='utf-8') as f:
            edit_urls = json.load(f)
    
    if Path(responder_urls_file).exists():
        with open(responder_urls_file, 'r', encoding='utf-8') as f:
            responder_urls = json.load(f)
    
    return edit_urls, responder_urls


def save_url_mappings(edit_urls: Dict, responder_urls: Dict,
                     edit_urls_file: str, responder_urls_file: str):
    """Save URL mapping files."""
    with open(edit_urls_file, 'w', encoding='utf-8') as f:
        json.dump(edit_urls, f, indent=2, ensure_ascii=False)
    
    with open(responder_urls_file, 'w', encoding='utf-8') as f:
        json.dump(responder_urls, f, indent=2, ensure_ascii=False)


def format_question_text(text: str) -> str:
    """
    Format question text for Google Forms.
    
    Removes markdown code blocks and converts to plain text.
    Preserves code formatting by keeping backticks for readability.
    """
    # Remove triple backticks and code block markers
    text = text.replace('```', '')
    
    # Clean up excessive whitespace
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
        elif cleaned_lines and cleaned_lines[-1]:  # Add single blank line
            cleaned_lines.append('')
    
    return '\n'.join(cleaned_lines).strip()


def remove_backticks(text: str) -> str:
    """
    Remove backticks from text (used for code formatting in markdown).
    
    Google Forms doesn't format backticks, so we remove them for cleaner display.
    """
    if not text:
        return text
    
    # Remove backticks but preserve the content
    text = text.replace('`', '')
    
    return text


def create_quiz_from_data(forms_service, drive_service, quiz_data: Dict,
                          folder_id: str) -> Optional[tuple]:
    """
    Create a Google Forms quiz from quiz data.
    
    Parameters:
    -----------
    forms_service : Resource
        Google Forms API service
    drive_service : Resource
        Google Drive API service
    quiz_data : dict
        Quiz data dictionary with title, quiz_type, and questions
    folder_id : str
        Drive folder ID to move form to
    
    Returns:
    --------
    tuple : (form_id, edit_url, responder_url) or None on failure
    """
    title = quiz_data['title']
    quiz_type = quiz_data.get('quiz_type', 'Formative')
    questions = quiz_data['questions']
    
    print(f"\nCreating quiz: {title} ({quiz_type})")
    print(f"  Questions: {len(questions)}")
    
    # Create form title: "Think Python Chapter 1 quiz" or "Think Python Summative quiz"
    if title.startswith("Chapter "):
        form_title = f"Think Python {title} quiz"
    else:
        form_title = f"Think Python {title} quiz"
    
    # Create the form (no description - we'll add intro text as first item)
    form_id = create_quiz_form(forms_service, form_title)
    if not form_id:
        print("ERROR: Failed to create form")
        return None
    
    print(f"  ✓ Created form: {form_id}")
    
    # Add introduction text as first block
    # Use the quiz title (e.g., "Chapter 1") as the intro block title
    book_url = "https://allendowney.github.io/ThinkPython/"
    
    if title.startswith("Chapter "):
        intro_text = (
            f"This quiz relates to {title} of *Think Python 3e*.\n\n"
            f"For more information about the book, visit:\n"
            f"{book_url}\n\n"
            f"Each question has multiple choice answers. "
            f"After submitting, you'll see feedback explaining the correct answer."
        )
    else:
        # Summative quiz
        intro_text = (
            f"This is a summative quiz covering material from *Think Python 3e*.\n\n"
            f"For more information about the book, visit:\n"
            f"{book_url}\n\n"
            f"Each question has multiple choice answers. "
            f"After submitting, you'll see feedback explaining the correct answer."
        )
    
    print("  Adding introduction text...")
    # Use the quiz title (e.g., "Chapter 1") as the intro block title
    intro_item_id = add_intro_text_item(
        forms_service, form_id, title, intro_text, location_index=0
    )
    if intro_item_id:
        print("  ✓ Added introduction text")
    else:
        print("  WARNING: Failed to add introduction text")
    
    # Prepare questions data for batch creation
    questions_data = []
    for q in questions:
        question_text = format_question_text(q['question_text'])
        options = q['options'].copy()  # Make a copy to avoid modifying original
        correct_index = q['correct_answer_index']
        rationales = q['rationales'].copy()  # Make a copy to match shuffled options
        
        # Remove backticks from options and rationales
        options = [remove_backticks(opt) for opt in options]
        rationales = [remove_backticks(rat) for rat in rationales]
        
        # Shuffle options and update correct answer index
        # Create list of (option, rationale, is_correct) tuples
        option_data = [(opt, rat, i == correct_index) 
                      for i, (opt, rat) in enumerate(zip(options, rationales))]
        
        # Shuffle the options
        random.shuffle(option_data)
        
        # Extract shuffled options and rationales, find new correct index
        shuffled_options = []
        shuffled_rationales = []
        new_correct_index = None
        
        for i, (opt, rat, is_correct) in enumerate(option_data):
            shuffled_options.append(opt)
            shuffled_rationales.append(rat)
            if is_correct:
                new_correct_index = i
        
        # Create feedback text using the correct answer's rationale
        # (Backticks already removed above)
        correct_feedback = None
        if new_correct_index is not None and new_correct_index < len(shuffled_rationales):
            correct_feedback = shuffled_rationales[new_correct_index]
        
        # Create "when wrong" feedback with general guidance
        incorrect_feedback = "Please review the material and try again."
        
        questions_data.append({
            'question_text': question_text,
            'options': shuffled_options,
            'correct_answer_index': new_correct_index,
            'points': 1,
            'correct_feedback': correct_feedback,
            'incorrect_feedback': incorrect_feedback
        })
    
    # Add all questions in batch (starting at index 1 since intro is at 0)
    print(f"  Adding {len(questions_data)} questions...")
    item_ids = add_quiz_questions_batch(
        forms_service, form_id, questions_data, 
        shuffle_option_order=True, starting_index=1
    )
    
    if len(item_ids) != len(questions_data):
        print(f"  WARNING: Expected {len(questions_data)} questions, got {len(item_ids)}")
    else:
        print(f"  ✓ Added {len(item_ids)} questions")
    
    # Move form to folder
    try:
        move_form_to_folder(drive_service, form_id, folder_id)
        print(f"  ✓ Moved form to Drive folder")
    except Exception as e:
        print(f"  WARNING: Failed to move form to folder: {e}")
    
    # Get URLs
    edit_url, responder_url = get_form_urls(form_id)
    
    return form_id, edit_url, responder_url


def main():
    parser = argparse.ArgumentParser(
        description='Create a Google Forms quiz from parsed quiz data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_google_quiz.py --quiz "Chapter 1"
  python create_google_quiz.py --chapter 5
  python create_google_quiz.py --quiz "Think Python" --force
  python create_google_quiz.py --list
        """
    )
    
    parser.add_argument('--quiz', type=str,
                       help='Quiz title (e.g., "Chapter 1" or "Think Python")')
    parser.add_argument('--chapter', type=int, choices=range(1, 19),
                       help='Chapter number (1-18)')
    parser.add_argument('--force', action='store_true',
                       help='Recreate quiz even if it already exists')
    parser.add_argument('--list', action='store_true',
                       help='List all available quizzes')
    parser.add_argument('--quizzes-file', type=str,
                       default='parsed_quizzes.json',
                       help='Path to parsed quizzes JSON file')
    parser.add_argument('--edit-urls-file', type=str,
                       default='quiz_edit_urls.json',
                       help='Path to edit URLs mapping file')
    parser.add_argument('--responder-urls-file', type=str,
                       default='quiz_responder_urls.json',
                       help='Path to responder URLs mapping file')
    parser.add_argument('--folder-id', type=str,
                       default=QUIZZES_FOLDER_ID,
                       help='Drive folder ID for quizzes')
    
    args = parser.parse_args()
    
    # Get script directory (already defined at top for imports)
    quizzes_file = script_dir / args.quizzes_file
    edit_urls_file = script_dir / args.edit_urls_file
    responder_urls_file = script_dir / args.responder_urls_file
    
    # Load parsed quizzes
    if not quizzes_file.exists():
        print(f"ERROR: {quizzes_file} not found")
        print("Please run: python parse_quizzes.py")
        return 1
    
    print("Loading parsed quizzes...")
    quizzes = load_parsed_quizzes(str(quizzes_file))
    print(f"✓ Loaded {len(quizzes)} quizzes")
    
    # List available quizzes
    if args.list:
        print("\nAvailable quizzes:")
        for quiz in quizzes:
            print(f"  - {quiz['title']} ({quiz['quiz_type']}, {len(quiz['questions'])} questions)")
        return 0
    
    # Find the quiz to create
    if not args.quiz and not args.chapter:
        print("ERROR: Must specify --quiz or --chapter")
        parser.print_help()
        return 1
    
    quiz_data = find_quiz(quizzes, title=args.quiz, chapter=args.chapter)
    if not quiz_data:
        print(f"ERROR: Quiz not found")
        if args.chapter:
            print(f"  Searched for: Chapter {args.chapter}")
        else:
            print(f"  Searched for: {args.quiz}")
        print("\nAvailable quizzes:")
        for quiz in quizzes:
            print(f"  - {quiz['title']}")
        return 1
    
    quiz_title = quiz_data['title']
    
    # Load URL mappings
    edit_urls, responder_urls = load_url_mappings(
        str(edit_urls_file), str(responder_urls_file)
    )
    
    # Check if quiz already exists
    if quiz_title in edit_urls and not args.force:
        print(f"\nQuiz '{quiz_title}' already exists!")
        print(f"  Edit URL: {edit_urls[quiz_title]}")
        print(f"  Responder URL: {responder_urls.get(quiz_title, 'N/A')}")
        print("\nUse --force to recreate it")
        return 0
    
    if args.force and quiz_title in edit_urls:
        print(f"\n⚠️  Recreating quiz '{quiz_title}' (--force specified)")
    
    # Authenticate
    print("\nAuthenticating with Google...")
    creds = load_credentials()
    if not creds:
        print("ERROR: Failed to load credentials")
        return 1
    print("✓ Credentials loaded")
    
    # Get services
    forms_service = get_forms_service(creds)
    drive_service, _ = get_services(creds)
    
    if not forms_service or not drive_service:
        print("ERROR: Failed to get API services")
        return 1
    print("✓ API services connected")
    
    # Create the quiz
    result = create_quiz_from_data(
        forms_service, drive_service, quiz_data, args.folder_id
    )
    
    if not result:
        print("ERROR: Failed to create quiz")
        return 1
    
    form_id, edit_url, responder_url = result
    
    # Update URL mappings
    edit_urls[quiz_title] = edit_url
    responder_urls[quiz_title] = responder_url
    
    save_url_mappings(edit_urls, responder_urls,
                     str(edit_urls_file), str(responder_urls_file))
    
    print("\n" + "=" * 70)
    print("Quiz created successfully!")
    print("=" * 70)
    print(f"Title: {quiz_title}")
    print(f"Form ID: {form_id}")
    print(f"\nEdit URL (owner):")
    print(f"  {edit_url}")
    print(f"\nResponder URL (share with students):")
    print(f"  {responder_url}")
    print("=" * 70)
    print(f"\n✓ URL mappings saved to:")
    print(f"  - {edit_urls_file}")
    print(f"  - {responder_urls_file}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

