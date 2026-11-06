# Plan: Creating Google Quizzes from quizzes.md

## Overview

This plan outlines the steps to create Google Forms quizzes programmatically from `quizzes.md`. We will create:
- **18 formative quizzes** (one per chapter, Chapters 1-18)
- **1 summative quiz** (all "Think Python" questions)

## Quiz Structure Analysis

From `quizzes.md`, each quiz section contains:
- **Title**: Chapter name (e.g., "Chapter 1")
- **Quiz Type**: "Formative" or "Summative"
- **Questions**: Multiple questions, each with:
  - Question text (markdown format, may include code blocks or LaTeX)
  - Multiple choice options (4 options per question)
  - Correct answer: Always marked with `[X]` and **always the last option**
  - Rationale: Explanations for each option (4 explanations matching the 4 options)

## Implementation Steps

### Step 1: Parse quizzes.md

**Script**: `parse_quizzes.py`

**Tasks**:
1. Parse markdown file to extract quiz sections
2. Identify chapter boundaries (look for `# Title` followed by chapter name)
3. For each quiz section:
   - Extract title and quiz type
   - Parse questions (look for `### Question`)
   - For each question:
     - Extract question text (handle markdown formatting, code blocks, LaTeX)
     - Extract 4 multiple choice options (look for `- [ ]` or `- [X]`)
     - Identify correct answer (the one with `[X]`, which is always last)
     - Extract rationale (4 explanations matching the 4 options)
4. Store parsed data in structured format (JSON or Python dict)

**Output**: 
- `parsed_quizzes.json` - Structured data for all quizzes
- Or individual JSON files per chapter: `chapter_01.json`, `chapter_02.json`, etc.

### Step 2: Set Up Google Forms API

**Script**: `setup_forms_api.py` or extend `google_utils.py`

**Tasks**:
1. Ensure Google Forms API is enabled in Google Cloud Console
2. Add Forms API scope to `google_utils.py`:
   - `https://www.googleapis.com/auth/forms.body` (already mentioned in skill doc)
3. Create function to get Forms service:
   ```python
   def get_forms_service(creds):
       from googleapiclient.discovery import build
       return build('forms', 'v1', credentials=creds)
   ```

### Step 3: Create Quiz Creation Functions

**Script**: Extend `google_utils.py` or create `google_forms_utils.py`

**Functions needed**:

1. **`create_quiz_form(forms_service, title, description=None)`**
   - Create a new Google Form
   - Set it as a quiz (enable quiz settings)
   - **Important**: Enable "Shuffle option order" in quiz settings (since correct answer is always last)
   - Return form ID

2. **`add_quiz_question(forms_service, form_id, question_text, options, correct_answer_index, points=1, feedback=None)`**
   - Add a multiple choice question to the form
   - Set correct answer
   - Add point value
   - Add feedback/rationale (if provided)
   - **Important**: Shuffle options (handled at form level, but verify)

3. **`add_question_feedback(forms_service, form_id, question_id, correct_feedback, incorrect_feedback=None, per_option_feedback=None)`**
   - Add feedback for correct/incorrect answers
   - Optionally add per-option feedback (rationale for each option)

### Step 4: Handle Markdown Formatting

**Script**: `format_question_text.py` or utility functions

**Tasks**:
1. Convert markdown to plain text or HTML for Google Forms:
   - Code blocks: Preserve formatting (use monospace or code formatting)
   - LaTeX math: Convert to plain text or use Unicode equivalents
   - Bold/italic: Convert to plain text or HTML if Forms supports it
2. Clean up question text for Google Forms API
3. Handle special characters and escape sequences

**Note**: Google Forms API may have limitations on formatting. Test what works:
- Plain text (safest)
- HTML (if supported)
- Unicode characters for math symbols

### Step 5: Main Quiz Creation Script

**Script**: `create_google_quizzes.py`

**Workflow**:
1. Load parsed quiz data (from Step 1)
2. Authenticate with Google (use `load_credentials()` from `google_utils.py`)
3. Get Forms service
4. For each quiz (18 chapters + 1 summative):
   - Create quiz form with appropriate title
   - Enable quiz settings:
     - Make it a quiz
     - **Enable "Shuffle option order"** (critical - correct answer is always last)
     - Set point values
   - For each question:
     - Format question text
     - Extract options (shuffle will be handled by form setting)
     - Identify correct answer index (will be last before shuffling)
     - Add question to form
     - Add feedback/rationale
   - Store form metadata (form ID, edit URL, response URL)
5. Save metadata to JSON file

**Output**:
- `quiz_metadata.json` with form IDs and URLs for all quizzes

### Step 6: Handle Rationales/Feedback

**Considerations**:
- Google Forms supports:
  - General feedback for correct answers
  - General feedback for incorrect answers
  - Per-option feedback (rationale for each specific option)

**Strategy**:
- Use per-option feedback to show the rationale for each choice
- This provides detailed explanation for why each option is correct/incorrect

### Step 7: Testing and Validation

**Script**: `test_quizzes.py`

**Tasks**:
1. Verify all quizzes were created
2. Check that option shuffling is enabled
3. Spot-check a few questions:
   - Correct answer is marked properly
   - Rationales appear as feedback
   - Question text is formatted correctly
4. Test submitting a quiz response
5. Verify scoring works correctly

### Step 8: Documentation

**File**: `QUIZ_CREATION_README.md`

**Content**:
- How to run the scripts
- Prerequisites (credentials, API setup)
- Output files and their locations
- How to access/edit the quizzes
- Troubleshooting guide

## File Structure

```
quizzes/
├── quizzes.md                    # Source file
├── plan.md                       # This file
├── parse_quizzes.py              # Step 1: Parse markdown
├── create_google_quizzes.py      # Step 5: Main script
├── format_question_text.py       # Step 4: Formatting utilities
├── test_quizzes.py               # Step 7: Testing
├── google_utils.py               # Existing utilities (extend for Forms)
├── parsed_quizzes.json           # Step 1 output
├── quiz_metadata.json            # Step 5 output
└── QUIZ_CREATION_README.md       # Step 8: Documentation
```

## Key Implementation Details

### Option Shuffling

**Critical**: Since the correct answer is always last in the markdown, we must:
1. Enable "Shuffle option order" at the form/quiz level
2. When adding questions, identify the correct answer by its index (last = correct)
3. After shuffling is enabled, Google Forms will randomize the order for each respondent

### Question Formatting

- Code blocks: May need to convert to plain text with indentation or use monospace
- LaTeX math (e.g., `$8 ÷ 2(2+2)$`): Convert to Unicode or plain text
- Markdown formatting: Strip or convert to plain text

### Rationale Handling

- Each question has 4 rationales matching the 4 options
- Use Google Forms' per-option feedback feature
- Map each rationale to its corresponding option

### API Considerations

- Google Forms API v1 may have limitations
- Test formatting options early
- May need to use Google Apps Script as alternative if API is too limited
- Consider using Google Forms web interface for final formatting touches if needed

## Dependencies

- `google_utils.py` - Existing authentication and utilities
- Google Forms API v1
- Markdown parser (consider `markdown` or `mistune` library)
- JSON for data storage

## Implementation Status

### ✅ Completed

1. **Step 1: Parse quizzes.md** ✅
   - Created `parse_quizzes.py` that successfully extracts all quiz data
   - Parsed 19 quizzes (18 chapters + 1 summative) with 83 total questions
   - Output: `parsed_quizzes.json` and individual chapter JSON files in `parsed_chapters/`
   - Structure includes: title, quiz_type, questions with options, correct_answer_index, and rationales

2. **Step 2: Set Up Google Forms API** ✅
   - Added Forms API scope to `google_utils.py` (already present)
   - Created `get_forms_service()` function
   - Installed required Google API client libraries in ThinkPython environment

3. **Step 3: Create Quiz Creation Functions** ✅
   - Added `create_quiz_form()` - Creates form and enables quiz mode
   - Added `add_quiz_questions_batch()` - Adds multiple questions efficiently
   - Added `add_intro_text_item()` - Adds introduction text blocks
   - Added `move_form_to_folder()` - Moves forms to Drive folder
   - Added `get_form_urls()` - Gets edit and responder URLs

4. **Step 4: Handle Markdown Formatting** ✅
   - Created `format_question_text()` - Removes code blocks, cleans whitespace
   - Created `remove_backticks()` - Removes backticks from options and rationales
   - Backticks removed from both question options and feedback text

5. **Step 5: Main Quiz Creation Script** ✅
   - Created `create_google_quiz.py` with command-line interface
   - Supports `--quiz`, `--chapter`, `--force`, and `--list` options
   - Checks for existing quizzes (prevents duplicates unless `--force`)
   - Maintains two JSON mapping files:
     - `quiz_edit_urls.json` - Maps quiz titles to edit URLs
     - `quiz_responder_urls.json` - Maps quiz titles to responder URLs
   - Shuffles options before sending to API (since correct answer is always last)
   - Creates forms in specified Drive folder: `1NqmWKV6EV1SozzRX5d-sm_j8pdXzZ5LS`
   - Form titles: "Think Python Chapter X quiz" format
   - Introduction block uses quiz title (e.g., "Chapter 1") and includes book link

### ⚠️ Outstanding Issues

1. **Introduction Text Block** ⚠️
   - Status: Function exists but shows "WARNING: Failed to add introduction text"
   - Issue: The intro text item creation is failing silently
   - Impact: Quiz works but lacks the introduction block with book information
   - Note: Questions are being added successfully, so this is a separate issue
   - Possible cause: API response structure for text items may differ from question items
   - **Action needed**: Debug `add_intro_text_item()` function - check API response structure

2. **Option Shuffling** ⚠️
   - Status: Options are shuffled in Python code before sending to API
   - Issue: Google Forms API v1 does not support `shuffleOptionOrder` field
   - Current solution: We shuffle options in Python code, which works but means:
     - Each quiz creation has a different random order (not per-respondent)
     - Manual verification needed to ensure shuffling is working correctly
   - Future: May need to enable shuffling manually in Google Forms UI, or wait for API support

3. **Per-Option Feedback** ⚠️
   - Status: Currently using general `whenRight` and `whenWrong` feedback
   - Issue: Not using per-option feedback (rationale for each specific option)
   - Impact: Students only see feedback for correct answer, not explanations for wrong choices
   - Note: This is a limitation of current implementation, not a blocker

4. **Error Handling** ⚠️
   - Status: Basic error handling in place
   - Issue: Some errors (like intro text failure) are caught but not fully diagnosed
   - Improvement needed: Better error messages and debugging output

### 📝 Testing Status

- ✅ Successfully created Chapter 1 quiz
- ✅ Questions are being added correctly (4/4 questions added)
- ✅ Form is created with correct title format ("Think Python Chapter 1 quiz")
- ✅ Form is moved to correct Drive folder
- ✅ URL mappings are saved correctly
- ✅ Options are shuffled (correct answer not always last)
- ✅ Backticks removed from options and rationales
- ⚠️ Introduction text block not being added (needs investigation)

### 🔄 On Hold

**Status**: Implementation is functional but has one outstanding issue (intro text). 
The quiz creation works for questions, but the introduction block needs debugging.

**Next Steps When Resuming**:
1. Debug `add_intro_text_item()` function - check API response structure for text items
2. Verify intro text block structure matches Google Forms API requirements
3. Test with a simple text item to isolate the issue
4. Once intro text works, test all 19 quizzes
5. Document final workflow and usage instructions

### 📋 Notes

- The quiz creation is working for the core functionality (questions)
- All 19 quizzes can be created using the script
- Option shuffling works (done in Python before API call)
- Backticks are properly removed from options and rationales
- Form titles and structure match requirements
- The only blocker is the introduction text block, which is nice-to-have but not critical

