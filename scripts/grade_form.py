#!/usr/bin/env python3
"""
grade_form.py — Fetch and grade Google Forms quiz responses.

Usage:
    # Grade with auto-graded results from Google Forms
    python scripts/grade_form.py FORM_ID

    # Grade with local answer key (for custom grading)
    python scripts/grade_form.py FORM_ID --answers quizzes/answers/quiz02_answers.json

    # Export to CSV
    python scripts/grade_form.py FORM_ID --csv grades/quiz02_grades.csv

Example:
    python scripts/grade_form.py 1Iext-BaXmTnCnl8EefRk5HtaLU5MxAD_XS6xr9zXECI
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Re-use auth from quiz_to_google_form
sys.path.insert(0, str(Path(__file__).parent))
from quiz_to_google_form import get_credentials

from googleapiclient.discovery import build


def fetch_form_structure(form_service, form_id: str) -> dict:
    """Fetch the form structure to map question IDs to titles."""
    form = form_service.forms().get(formId=form_id).execute()
    
    question_map = {}  # questionId -> {title, index, points}
    items = form.get("items", [])
    q_index = 0
    
    for item in items:
        question_item = item.get("questionItem")
        if question_item:
            q_index += 1
            question = question_item.get("question", {})
            q_id = question.get("questionId", "")
            grading = question.get("grading", {})
            points = grading.get("pointValue", 1)
            
            # Determine question type and options
            q_type = "text"
            choice_options = []
            if "choiceQuestion" in question:
                q_type = "choice"
                for opt in question["choiceQuestion"].get("options", []):
                    choice_options.append(opt.get("value", ""))
            
            # Extract question number from title
            title = item.get("title", "")
            num_match = re.search(r"Pregunta\s+(\d+)", title)
            q_num = int(num_match.group(1)) if num_match else q_index
            
            question_map[q_id] = {
                "title": title,
                "number": q_num,
                "index": q_index,
                "points": points,
                "type": q_type,
                "options": choice_options,
            }
    
    return {
        "title": form.get("info", {}).get("title", ""),
        "questions": question_map,
        "total_points": sum(q["points"] for q in question_map.values()),
    }


def fetch_responses(form_service, form_id: str) -> list[dict]:
    """Fetch all responses from the form."""
    responses = []
    page_token = None
    
    while True:
        result = form_service.forms().responses().list(
            formId=form_id,
            pageToken=page_token,
        ).execute()
        
        responses.extend(result.get("responses", []))
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    
    return responses


def grade_responses(
    form_structure: dict,
    responses: list[dict],
    answer_key: dict | None = None,
) -> list[dict]:
    """Grade all responses and return structured results."""
    question_map = form_structure["questions"]
    total_points = form_structure["total_points"]
    results = []
    
    for resp in responses:
        response_id = resp.get("responseId", "")
        submitted = resp.get("lastSubmittedTime", "")
        answers = resp.get("answers", {})
        
        student_result = {
            "response_id": response_id,
            "submitted": submitted,
            "email": "",
            "score": 0,
            "total": total_points,
            "answers": {},
            "details": [],
        }
        
        # Check for respondent email
        if "respondentEmail" in resp:
            student_result["email"] = resp["respondentEmail"]
        
        for q_id, q_info in question_map.items():
            q_num = q_info["number"]
            q_points = q_info["points"]
            answer_data = answers.get(q_id, {})
            
            # Get the student's answer text
            text_answers = answer_data.get("textAnswers", {})
            answer_list = text_answers.get("answers", [])
            student_answer = answer_list[0].get("value", "") if answer_list else ""
            
            # Grade based on Google Forms built-in grading
            grade = answer_data.get("grade", {})
            points_earned = grade.get("score", 0) if grade else 0
            correct = grade.get("correct", None) if grade else None
            
            # If we have a local answer key, use it for choice questions
            if answer_key and str(q_num) in answer_key and q_info["type"] == "choice":
                correct_letter = answer_key[str(q_num)].lower()
                correct_idx = ord(correct_letter) - ord("a")
                options = q_info.get("options", [])
                
                # Get the correct answer text from the options list
                correct_text = options[correct_idx] if correct_idx < len(options) else ""
                
                # Try matching by letter prefix first (e.g. "b) ...")
                student_letter = ""
                letter_match = re.match(r"^([a-d])\)", student_answer.strip())
                if letter_match:
                    student_letter = letter_match.group(1).lower()
                    correct = student_letter == correct_letter
                else:
                    # Match by comparing answer text directly to the correct option
                    correct = student_answer.strip() == correct_text.strip()
                
                points_earned = q_points if correct else 0
            
            student_result["score"] += points_earned
            student_result["answers"][q_num] = student_answer
            student_result["details"].append({
                "question": q_num,
                "answer": student_answer[:60],
                "points": points_earned,
                "max_points": q_points,
                "correct": correct,
                "type": q_info["type"],
            })
        
        results.append(student_result)
    
    # Sort by submission time
    results.sort(key=lambda r: r["submitted"])
    return results


def print_results(form_structure: dict, results: list[dict]):
    """Print a formatted grade report."""
    title = form_structure["title"]
    total = form_structure["total_points"]
    n_questions = len(form_structure["questions"])
    
    print(f"\n{'='*70}")
    print(f"  RESULTADOS: {title}")
    print(f"  {len(results)} respuestas | {n_questions} preguntas | {total} puntos")
    print(f"{'='*70}\n")
    
    if not results:
        print("  No hay respuestas aún.")
        return
    
    # Per-student results
    scores = []
    for i, r in enumerate(results, 1):
        email = r["email"] or f"Estudiante {i}"
        score = r["score"]
        pct = (score / total * 100) if total > 0 else 0
        scores.append(score)
        
        # Status emoji
        if pct >= 80:
            status = "🟢"
        elif pct >= 60:
            status = "🟡"
        else:
            status = "🔴"
        
        submitted = r["submitted"][:19].replace("T", " ") if r["submitted"] else "?"
        
        print(f"  {status} {email:<35} {score:>3}/{total}  ({pct:5.1f}%)  [{submitted}]")
        
        # Show details for wrong/ungraded answers
        wrong = [d for d in r["details"] if d["correct"] is False]
        ungraded = [d for d in r["details"] if d["correct"] is None and d["type"] == "text"]
        
        if wrong:
            wrong_nums = ", ".join(f"P{d['question']}" for d in wrong)
            print(f"       ❌ Incorrectas: {wrong_nums}")
        if ungraded:
            ungraded_nums = ", ".join(f"P{d['question']}" for d in ungraded)
            print(f"       📝 Pendientes de revisar: {ungraded_nums}")
    
    # Summary statistics
    if scores:
        import statistics
        avg = statistics.mean(scores)
        median = statistics.median(scores)
        std = statistics.stdev(scores) if len(scores) > 1 else 0
        min_s, max_s = min(scores), max(scores)
        
        print(f"\n{'─'*70}")
        print(f"  📊 ESTADÍSTICAS")
        print(f"     Promedio:  {avg:.1f}/{total} ({avg/total*100:.1f}%)")
        print(f"     Mediana:   {median:.1f}/{total}")
        print(f"     Desv. Est: {std:.1f}")
        print(f"     Mín/Máx:   {min_s}/{total} — {max_s}/{total}")
        
        # Distribution
        ranges = {"0-59%": 0, "60-79%": 0, "80-100%": 0}
        for s in scores:
            pct = s / total * 100
            if pct >= 80:
                ranges["80-100%"] += 1
            elif pct >= 60:
                ranges["60-79%"] += 1
            else:
                ranges["0-59%"] += 1
        
        print(f"\n  📈 DISTRIBUCIÓN")
        for rng, count in ranges.items():
            bar = "█" * count
            print(f"     {rng:>8}: {bar} ({count})")
    
    # Per-question analysis
    print(f"\n{'─'*70}")
    print(f"  📋 ANÁLISIS POR PREGUNTA")
    
    q_stats = defaultdict(lambda: {"correct": 0, "wrong": 0, "ungraded": 0})
    for r in results:
        for d in r["details"]:
            q = d["question"]
            if d["correct"] is True:
                q_stats[q]["correct"] += 1
            elif d["correct"] is False:
                q_stats[q]["wrong"] += 1
            else:
                q_stats[q]["ungraded"] += 1
    
    for q_num in sorted(q_stats.keys()):
        s = q_stats[q_num]
        total_answered = s["correct"] + s["wrong"]
        pct = (s["correct"] / total_answered * 100) if total_answered > 0 else 0
        bar = "█" * int(pct / 5)
        ungraded_mark = f" (+{s['ungraded']} pendientes)" if s["ungraded"] > 0 else ""
        print(f"     P{q_num:>2}: {pct:5.1f}% correcto {bar}{ungraded_mark}")
    
    # Show paragraph answers that need manual grading
    ungraded_questions = set()
    for r in results:
        for d in r["details"]:
            if d["correct"] is None and d["type"] == "text":
                ungraded_questions.add(d["question"])
    
    if ungraded_questions:
        print(f"\n{'─'*70}")
        print(f"  ✏️  RESPUESTAS PENDIENTES DE CALIFICAR")
        for q_num in sorted(ungraded_questions):
            q_info = None
            for q in form_structure["questions"].values():
                if q["number"] == q_num:
                    q_info = q
                    break
            
            print(f"\n  Pregunta {q_num}: {q_info['title'][:60] if q_info else ''}...")
            for i, r in enumerate(results, 1):
                email = r["email"] or f"Estudiante {i}"
                answer = r["answers"].get(q_num, "(sin respuesta)")
                print(f"    [{email}]:")
                # Indent the answer
                for line in answer.split("\n"):
                    print(f"      {line}")
    
    print(f"\n{'='*70}")


def export_csv(form_structure: dict, results: list[dict], csv_path: str):
    """Export grades to CSV."""
    os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)
    
    q_numbers = sorted(
        set(d["question"] for r in results for d in r["details"])
    )
    
    headers = ["Email/Estudiante", "Enviado"] + \
              [f"P{q}" for q in q_numbers] + \
              ["Puntaje", "Total", "Porcentaje"]
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i, r in enumerate(results, 1):
            email = r["email"] or f"Estudiante {i}"
            submitted = r["submitted"][:19].replace("T", " ") if r["submitted"] else ""
            
            row = [email, submitted]
            for q_num in q_numbers:
                detail = next(
                    (d for d in r["details"] if d["question"] == q_num), None
                )
                if detail:
                    row.append(f"{detail['points']}/{detail['max_points']}")
                else:
                    row.append("")
            
            pct = (r["score"] / r["total"] * 100) if r["total"] > 0 else 0
            row.extend([r["score"], r["total"], f"{pct:.1f}%"])
            writer.writerow(row)
    
    print(f"\n✅ Exportado a: {csv_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and grade Google Forms quiz responses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "form_id",
        help="Google Forms ID (from the edit URL)",
    )
    parser.add_argument(
        "--answers", "-a",
        help="Path to answer key JSON (optional, overrides Forms auto-grading for MC)",
        default=None,
    )
    parser.add_argument(
        "--csv", "-c",
        help="Export grades to CSV file",
        default=None,
    )
    args = parser.parse_args()
    
    # Load answer key
    answer_key = None
    if args.answers:
        with open(args.answers, "r") as f:
            answer_key = json.load(f)
        print(f"Loaded answer key with {len(answer_key)} answers")
    
    # Authenticate and build service
    creds = get_credentials()
    form_service = build("forms", "v1", credentials=creds)
    
    # Fetch form structure
    print("Fetching form structure...")
    form_structure = fetch_form_structure(form_service, args.form_id)
    
    # Fetch responses
    print("Fetching responses...")
    responses = fetch_responses(form_service, args.form_id)
    print(f"Found {len(responses)} responses")
    
    # Grade
    results = grade_responses(form_structure, responses, answer_key)
    
    # Display
    print_results(form_structure, results)
    
    # Export CSV if requested
    if args.csv:
        export_csv(form_structure, results, args.csv)


if __name__ == "__main__":
    main()
