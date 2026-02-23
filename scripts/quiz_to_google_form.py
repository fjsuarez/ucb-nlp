#!/usr/bin/env python3
"""
quiz_to_google_form.py — Convert quiz notebooks (.ipynb) to Google Forms quizzes.

Usage:
    python scripts/quiz_to_google_form.py quizzes/quiz02_representacion_texto.ipynb

    # With answer key:
    python scripts/quiz_to_google_form.py quizzes/quiz02_representacion_texto.ipynb \
        --answers quizzes/answers/quiz02_answers.json

Setup (one-time):
    1. Go to https://console.cloud.google.com/
    2. Create a project (or select an existing one)
    3. Enable the "Google Forms API" and "Google Drive API"
    4. Create OAuth 2.0 credentials (Desktop application)
    5. Download the credentials JSON file and save as:
       scripts/credentials.json
    6. Install dependencies:
       pip install google-api-python-client google-auth-oauthlib

Answer key JSON format (optional):
    {
        "1": "b",
        "2": "b",
        "5": "a",
        ...
    }
    Only include multiple-choice questions. Code/text questions are left ungraded.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes needed for Forms and Drive
SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/drive",
]

SCRIPT_DIR = Path(__file__).parent
TOKEN_PATH = SCRIPT_DIR / "token.json"
CREDENTIALS_PATH = SCRIPT_DIR / "credentials.json"


# ─────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────

def get_credentials():
    """Authenticate and return Google API credentials."""
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print(f"ERROR: No credentials file found at {CREDENTIALS_PATH}")
                print("Download OAuth 2.0 credentials from Google Cloud Console")
                print("and save as: scripts/credentials.json")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    return creds


# ─────────────────────────────────────────────
# Notebook Parsing
# ─────────────────────────────────────────────

def parse_notebook(notebook_path: str) -> dict:
    """Parse a quiz notebook and extract structured quiz data."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])
    quiz = {
        "title": "",
        "description": "",
        "sections": [],
        "questions": [],
    }

    current_section = None

    i = 0
    while i < len(cells):
        cell = cells[i]
        cell_type = cell.get("cell_type", "")
        source = "".join(cell.get("source", []))

        # Extract title from first markdown cell
        if cell_type == "markdown" and not quiz["title"]:
            title_match = re.search(r"^#\s+(.+)", source, re.MULTILINE)
            if title_match:
                quiz["title"] = _clean_markdown(title_match.group(1))
                # Extract description (everything after the title)
                desc_lines = []
                for line in source.split("\n"):
                    if line.startswith("# "):
                        continue
                    if line.startswith("## "):
                        desc_lines.append(_clean_markdown(line.lstrip("# ")))
                    elif line.strip().startswith("**") or line.strip().startswith("-"):
                        desc_lines.append(_clean_markdown(line.strip()))
                quiz["description"] = "\n".join(desc_lines)
                i += 1
                continue

        # Detect section headers
        if cell_type == "markdown" and re.search(r"###\s+Sección", source):
            section_match = re.search(r"###\s+(.+)", source)
            if section_match:
                current_section = _clean_markdown(section_match.group(1))
                quiz["sections"].append({
                    "title": current_section,
                    "question_indices": [],
                })
            i += 1
            continue

        # Detect questions
        if cell_type == "markdown":
            pregunta_match = re.search(
                r"\*\*Pregunta\s+(\d+)\.\*\*\s*(.*)", source, re.DOTALL
            )
            if pregunta_match:
                q_num = int(pregunta_match.group(1))
                q_body = pregunta_match.group(2).strip()
                question = _parse_question(q_num, q_body, source)

                quiz["questions"].append(question)
                if current_section and quiz["sections"]:
                    quiz["sections"][-1]["question_indices"].append(
                        len(quiz["questions"]) - 1
                    )

        # Skip code cells (student response cells), section headers, etc.
        i += 1

    return quiz


def _parse_question(q_num: int, q_body: str, full_source: str) -> dict:
    """Parse a single question from its markdown source."""
    # Check if it's multiple choice (has a), b), c), d) options)
    option_pattern = re.compile(
        r"^([a-d])\)\s+(.+?)(?:\s*$)", re.MULTILINE
    )
    options = option_pattern.findall(full_source)

    if options:
        # Multiple choice question
        # Extract the question text (everything before the options)
        q_text = re.split(r"\n\s*a\)", full_source)[0]
        q_text = re.sub(r"\*\*Pregunta\s+\d+\.\*\*\s*", "", q_text).strip()
        # Clean markdown formatting
        q_text = _clean_markdown(q_text)

        return {
            "number": q_num,
            "type": "multiple_choice",
            "text": q_text,
            "options": [
                {"letter": letter, "text": _clean_markdown(text.strip())}
                for letter, text in options
            ],
        }
    else:
        # Free text / code question
        q_text = re.sub(r"\*\*Pregunta\s+\d+\.\*\*\s*", "", full_source).strip()
        q_text = _clean_markdown(q_text)

        return {
            "number": q_num,
            "type": "paragraph",
            "text": q_text,
            "options": [],
        }


def _clean_markdown(text: str) -> str:
    """Remove markdown formatting for plain text display."""
    # Remove bold
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    # Remove italic
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    # Remove inline code backticks
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Remove code blocks but keep content
    text = re.sub(r"```\w*\n?", "", text)
    # Remove markdown links, keep text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove LaTeX delimiters but keep content
    text = re.sub(r"\$\$(.+?)\$\$", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\$(.+?)\$", r"\1", text)
    # Clean extra whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _single_line(text: str) -> str:
    """Collapse text to a single line (for option values)."""
    return re.sub(r"\s+", " ", text).strip()


# ─────────────────────────────────────────────
# Google Forms Creation
# ─────────────────────────────────────────────

def create_google_form(quiz: dict, answers: dict | None = None):
    """Create a Google Form quiz from parsed quiz data."""
    creds = get_credentials()
    form_service = build("forms", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # Step 1: Create the form with title
    form_body = {
        "info": {
            "title": quiz["title"],
            "documentTitle": quiz["title"],
        }
    }
    form = form_service.forms().create(body=form_body).execute()
    form_id = form["formId"]
    print(f"Created form: {form['responderUri']}")

    # Step 2: Build batch update requests
    requests = []

    # Set quiz mode and collect emails
    requests.append({
        "updateSettings": {
            "settings": {
                "quizSettings": {
                    "isQuiz": True,
                }
            },
            "updateMask": "quizSettings.isQuiz",
        }
    })

    requests.append({
        "updateSettings": {
            "settings": {
                "emailCollectionType": "VERIFIED",
            },
            "updateMask": "emailCollectionType",
        }
    })

    requests.append({
        "updateFormInfo": {
            "info": {
                "description": quiz["description"],
            },
            "updateMask": "description",
        }
    })

    # Track question index for form items
    item_index = 0

    # Group questions by sections
    if quiz["sections"]:
        for sec_idx, section in enumerate(quiz["sections"]):
            # Add section header (except for the first — use form description)
            if sec_idx > 0 or item_index > 0:
                requests.append({
                    "createItem": {
                        "item": {
                            "title": _single_line(section["title"]),
                            "description": "",
                            "pageBreakItem": {},
                        },
                        "location": {"index": item_index},
                    }
                })
                item_index += 1

            # Add questions in this section
            for q_idx in section["question_indices"]:
                question = quiz["questions"][q_idx]
                req = _build_question_request(
                    question, item_index, answers
                )
                requests.append(req)
                item_index += 1
    else:
        # No sections — just add all questions
        for question in quiz["questions"]:
            req = _build_question_request(
                question, item_index, answers
            )
            requests.append(req)
            item_index += 1

    # Step 3: Execute batch update
    if requests:
        form_service.forms().batchUpdate(
            formId=form_id,
            body={"requests": requests},
        ).execute()

    # Print summary
    print(f"\nQuiz created successfully!")
    print(f"  Title: {quiz['title']}")
    print(f"  Questions: {len(quiz['questions'])}")
    print(f"  Edit URL: https://docs.google.com/forms/d/{form_id}/edit")
    print(f"  Share URL: {form['responderUri']}")

    return form_id


def _split_title_description(text: str) -> tuple[str, str]:
    """Split text into a single-line title and a multi-line description.
    
    Google Forms API requires titles to have no newlines.
    We put the first sentence/line as title and the rest as description.
    """
    # Split on first double newline or after first sentence
    parts = text.split("\n\n", 1)
    title = _single_line(parts[0])
    description = parts[1].strip() if len(parts) > 1 else ""
    return title, description


def _build_question_request(
    question: dict, index: int, answers: dict | None
) -> dict:
    """Build a createItem request for a question."""
    q_num = question["number"]
    full_text = f"Pregunta {q_num}. {question['text']}"
    title, description = _split_title_description(full_text)
    points = 1  # Each question is worth 1 point

    if question["type"] == "multiple_choice":
        # Build options
        options = []
        correct_letter = answers.get(str(q_num)) if answers else None

        for opt in question["options"]:
            option_value = {
                "value": _single_line(f"{opt['letter']}) {opt['text']}"),
            }
            options.append(option_value)

        item = {
            "title": title,
            "description": description,
            "questionItem": {
                "question": {
                    "required": True,
                    "choiceQuestion": {
                        "type": "RADIO",
                        "options": options,
                    },
                    "grading": {
                        "pointValue": points,
                    },
                }
            },
        }

        # Set correct answer if provided
        if correct_letter:
            correct_idx = ord(correct_letter.lower()) - ord("a")
            if 0 <= correct_idx < len(options):
                correct_value = options[correct_idx]["value"]
                item["questionItem"]["question"]["grading"]["correctAnswers"] = {
                    "answers": [{"value": correct_value}]
                }

        return {"createItem": {"item": item, "location": {"index": index}}}

    else:
        # Paragraph / code question
        item = {
            "title": title,
            "description": description,
            "questionItem": {
                "question": {
                    "required": True,
                    "textQuestion": {
                        "paragraph": True,
                    },
                    "grading": {
                        "pointValue": points,
                    },
                }
            },
        }
        return {"createItem": {"item": item, "location": {"index": index}}}


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert quiz notebooks to Google Forms quizzes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "notebook",
        help="Path to the quiz notebook (.ipynb)",
    )
    parser.add_argument(
        "--answers", "-a",
        help="Path to answer key JSON file (optional)",
        default=None,
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Parse notebook and print questions without creating the form",
    )
    args = parser.parse_args()

    # Parse notebook
    print(f"Parsing {args.notebook}...")
    quiz = parse_notebook(args.notebook)

    # Load answer key if provided
    answers = None
    if args.answers:
        with open(args.answers, "r") as f:
            answers = json.load(f)
        print(f"Loaded answer key with {len(answers)} answers")

    if args.dry_run:
        print(f"\n{'='*60}")
        print(f"Title: {quiz['title']}")
        print(f"Description:\n{quiz['description']}\n")
        for section in quiz["sections"]:
            print(f"\n--- {section['title']} ---")
            for q_idx in section["question_indices"]:
                q = quiz["questions"][q_idx]
                print(f"\n  Q{q['number']} [{q['type']}]: {q['text'][:80]}...")
                if q["options"]:
                    for opt in q["options"]:
                        correct = ""
                        if answers and answers.get(str(q["number"])) == opt["letter"]:
                            correct = " ✓"
                        print(f"    {opt['letter']}) {opt['text']}{correct}")
        print(f"\nTotal questions: {len(quiz['questions'])}")
        return

    # Create Google Form
    create_google_form(quiz, answers)


if __name__ == "__main__":
    main()
