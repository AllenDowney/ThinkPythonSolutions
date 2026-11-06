#!/usr/bin/env python3
"""
Parse quizzes.md to extract structured quiz data.

Extracts:
- Quiz title and type
- Questions with multiple choice options
- Correct answers (marked with [X], always last)
- Rationales for each option

Output: JSON file with structured quiz data
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


def parse_quizzes(md_file: str) -> List[Dict[str, Any]]:
    """
    Parse quizzes.md and extract all quiz data.
    
    Returns:
        List of quiz dictionaries, each containing:
        - title: str
        - quiz_type: str ("Formative" or "Summative")
        - questions: List of question dicts
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    quizzes = []
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        # Look for quiz start: "# Title" followed by title
        if lines[i].strip() == '# Title' and i + 1 < len(lines):
            title = lines[i + 1].strip()
            i += 2
            
            # Skip empty lines
            while i < len(lines) and not lines[i].strip():
                i += 1
            
            # Look for "## Quiz Type"
            quiz_type = None
            if i < len(lines) and lines[i].strip() == '## Quiz Type':
                if i + 1 < len(lines):
                    quiz_type = lines[i + 1].strip()
                i += 2
            
            # Skip empty lines and region markers
            while i < len(lines) and (not lines[i].strip() or 
                                      lines[i].strip().startswith('<!--')):
                i += 1
            
            # Parse questions until next "# Title" or end of file
            questions = []
            while i < len(lines):
                # Check if we've hit the next quiz
                if lines[i].strip() == '# Title':
                    break
                
                # Look for question start
                if lines[i].strip() == '### Question':
                    question = parse_question(lines, i)
                    if question:
                        questions.append(question)
                        # Move past this question
                        i = question.get('_end_line', i + 1)
                    else:
                        i += 1
                else:
                    i += 1
            
            if title and quiz_type and questions:
                quizzes.append({
                    'title': title,
                    'quiz_type': quiz_type,
                    'questions': questions
                })
        else:
            i += 1
    
    return quizzes


def parse_question(lines: List[str], start_idx: int) -> Optional[Dict[str, Any]]:
    """
    Parse a single question starting at start_idx.
    
    Returns:
        Dictionary with:
        - question_text: str
        - options: List[str]
        - correct_answer_index: int (always len(options) - 1)
        - rationales: List[str]
        - _end_line: int (for tracking position)
    """
    i = start_idx + 1
    question_text_parts = []
    options = []
    rationales = []
    correct_answer_index = None
    
    # Collect question text (until we hit options)
    while i < len(lines):
        line = lines[i].strip()
        
        # Stop if we hit next question or section
        if line.startswith('###') or line == '# Title':
            break
        
        # Check if this is an option (starts with "- [")
        if line.startswith('- ['):
            break
        
        # Collect question text (skip empty lines at start)
        if line or question_text_parts:
            question_text_parts.append(line)
        
        i += 1
    
    question_text = '\n'.join(question_text_parts).strip()
    
    # Parse options
    option_index = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Stop if we hit next question, section, or rationale
        if (line.startswith('###') or 
            line == '# Title' or
            line.startswith('<!--')):
            break
        
        # Check for option
        if line.startswith('- ['):
            # Extract option text (remove checkbox)
            option_text = re.sub(r'^- \[[ X]\]\s*', '', line).strip()
            options.append(option_text)
            
            # Check if this is the correct answer
            if '[X]' in line or '[x]' in line:
                correct_answer_index = option_index
        
        i += 1
        option_index += 1
    
    # Skip empty lines and look for rationale
    while i < len(lines) and (not lines[i].strip() or 
                               lines[i].strip().startswith('<!--')):
        i += 1
    
    # Parse rationale section
    if i < len(lines) and ('### Rationale' in lines[i] or '### Rationales' in lines[i]):
        i += 1
        while i < len(lines):
            line = lines[i].strip()
            
            # Stop if we hit next question or section
            if (line.startswith('###') or 
                line == '# Title' or
                (line.startswith('<!--') and line.endswith('-->'))):
                break
            
            # Collect rationale lines (each starts with "- ")
            if line.startswith('- '):
                # Remove the leading "- " and strip
                rationale_text = line[2:].strip()
                rationales.append(rationale_text)
            
            i += 1
    
    # Validate we have a complete question
    if not question_text or not options:
        return None
    
    # If no correct answer found, assume last option (as per plan)
    if correct_answer_index is None:
        correct_answer_index = len(options) - 1
    
    # Ensure we have rationales for all options (pad if needed)
    while len(rationales) < len(options):
        rationales.append("")
    
    return {
        'question_text': question_text,
        'options': options,
        'correct_answer_index': correct_answer_index,
        'rationales': rationales[:len(options)],  # Only take as many as options
        '_end_line': i
    }


def clean_text(text: str) -> str:
    """Clean and normalize text for Google Forms."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    return text


def save_quizzes_json(quizzes: List[Dict[str, Any]], output_file: str):
    """Save parsed quizzes to JSON file."""
    # Remove internal tracking fields
    cleaned_quizzes = []
    for quiz in quizzes:
        cleaned_quiz = {
            'title': quiz['title'],
            'quiz_type': quiz['quiz_type'],
            'questions': []
        }
        for q in quiz['questions']:
            cleaned_q = {
                'question_text': clean_text(q['question_text']),
                'options': [clean_text(opt) for opt in q['options']],
                'correct_answer_index': q['correct_answer_index'],
                'rationales': [clean_text(r) for r in q['rationales']]
            }
            cleaned_quiz['questions'].append(cleaned_q)
        cleaned_quizzes.append(cleaned_quiz)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_quizzes, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(cleaned_quizzes)} quizzes to {output_file}")
    print(f"Total questions: {sum(len(q['questions']) for q in cleaned_quizzes)}")


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    md_file = script_dir / 'quizzes.md'
    output_file = script_dir / 'parsed_quizzes.json'
    
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return
    
    print(f"Parsing {md_file}...")
    quizzes = parse_quizzes(str(md_file))
    
    if not quizzes:
        print("Error: No quizzes found")
        return
    
    print(f"\nFound {len(quizzes)} quizzes:")
    for quiz in quizzes:
        print(f"  - {quiz['title']}: {quiz['quiz_type']} ({len(quiz['questions'])} questions)")
    
    save_quizzes_json(quizzes, str(output_file))
    
    # Also save individual chapter files
    output_dir = script_dir / 'parsed_chapters'
    output_dir.mkdir(exist_ok=True)
    
    for quiz in quizzes:
        # Create safe filename
        safe_title = re.sub(r'[^a-zA-Z0-9_]+', '_', quiz['title']).strip('_')
        chapter_file = output_dir / f"{safe_title}.json"
        
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(quiz, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved individual file: {chapter_file}")


if __name__ == '__main__':
    main()

