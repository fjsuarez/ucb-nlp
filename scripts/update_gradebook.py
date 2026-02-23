#!/usr/bin/env python3
"""
Utilidad para gestionar el gradebook maestro del curso NLP.

Uso:
    # Ver el gradebook actual (tabla formateada)
    python update_gradebook.py show

    # Actualizar una nota
    python update_gradebook.py set --student "diego.lewensztain" --assessment "Quiz 2" --grade 8

    # Importar notas desde un CSV de quiz (con emails)
    python update_gradebook.py import --csv grades/quiz01_grades.csv --assessment "Quiz 1" \\
        --manual '{"P2": {"diego.lewensztain": 1, "nicole.lozada": 0}}'

    # Ver resumen de notas finales con ponderación
    python update_gradebook.py summary
"""

import argparse
import csv
import json
import os
import sys

GRADEBOOK_PATH = os.path.join(os.path.dirname(__file__), "..", "grades", "gradebook.csv")

WEIGHTS = {
    "Quiz 1": 1, "Quiz 2": 1, "Quiz 3": 1, "Quiz 4": 1, "Quiz 5": 1,
    "Quiz 6": 1, "Quiz 7": 1, "Quiz 8": 1, "Quiz 9": 1, "Quiz 10": 1,
    "Tarea 1": 10, "Tarea 2": 10, "Examen Parcial": 20,
    "Tarea 3": 10, "Tarea 4": 10, "Proyecto Final": 30,
}

QUIZ_COLS = [f"Quiz {i}" for i in range(1, 11)]
MAX_QUIZ = 10  # each quiz is out of 10


def read_gradebook():
    """Lee el gradebook CSV y retorna headers + filas."""
    with open(GRADEBOOK_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)
    return headers, rows


def write_gradebook(headers, rows):
    """Escribe el gradebook CSV."""
    with open(GRADEBOOK_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def find_student(rows, query):
    """Busca un estudiante por email parcial o nombre."""
    query_lower = query.lower()
    matches = []
    for row in rows:
        if query_lower in row["Email"].lower() or query_lower in row["Estudiante"].lower():
            matches.append(row)
    return matches


def cmd_show(args):
    """Muestra el gradebook en formato tabla."""
    headers, rows = read_gradebook()

    # Calculate column widths
    col_widths = {}
    for h in headers:
        col_widths[h] = max(len(h), max((len(str(row.get(h, ""))) for row in rows), default=0))

    # Print header
    header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
    print(header_line)
    print("-+-".join("-" * col_widths[h] for h in headers))

    # Print rows
    for row in rows:
        print(" | ".join(str(row.get(h, "")).ljust(col_widths[h]) for h in headers))

    print(f"\n📊 {len(rows)} estudiantes registrados")


def cmd_set(args):
    """Establece una nota para un estudiante y evaluación."""
    headers, rows = read_gradebook()

    if args.assessment not in headers:
        print(f"❌ Evaluación '{args.assessment}' no encontrada.")
        print(f"   Disponibles: {', '.join(h for h in headers if h not in ('Estudiante', 'Email'))}")
        sys.exit(1)

    matches = find_student(rows, args.student)
    if len(matches) == 0:
        print(f"❌ Estudiante '{args.student}' no encontrado.")
        sys.exit(1)
    elif len(matches) > 1:
        print(f"⚠️  Múltiples coincidencias para '{args.student}':")
        for m in matches:
            print(f"   - {m['Estudiante']} ({m['Email']})")
        sys.exit(1)

    student = matches[0]
    old_val = student.get(args.assessment, "")
    student[args.assessment] = str(args.grade)
    write_gradebook(headers, rows)

    print(f"✅ {student['Estudiante']} - {args.assessment}: {old_val or '(vacío)'} → {args.grade}")


def cmd_summary(args):
    """Muestra un resumen ponderado de notas (rendimiento actual + proyección)."""
    headers, rows = read_gradebook()

    # Assessment max scores: quizzes out of 10, tareas/examen/proyecto out of 100
    ASSESSMENT_MAX = {}
    for col in QUIZ_COLS:
        ASSESSMENT_MAX[col] = MAX_QUIZ
    for a in ("Tarea 1", "Tarea 2", "Examen Parcial", "Tarea 3", "Tarea 4", "Proyecto Final"):
        ASSESSMENT_MAX[a] = 100

    # Weight per individual quiz = total quiz weight / number of quizzes
    QUIZ_WEIGHT_EACH = 10.0 / 10  # 10% total spread across 10 quizzes = 1% each

    print("=" * 70)
    print("RESUMEN DE NOTAS - NLP UCB")
    print("=" * 70)

    for row in rows:
        print(f"\n📋 {row['Estudiante']} ({row['Email']})")
        print("-" * 55)

        earned_pts = 0.0      # weighted points earned
        available_pts = 0.0   # weighted points available (only graded assessments)

        # --- Quizzes ---
        quiz_scores = []
        for qcol in QUIZ_COLS:
            val = row.get(qcol, "").strip()
            if val:
                score = float(val)
                quiz_scores.append(score)
                earned_pts += (score / MAX_QUIZ) * QUIZ_WEIGHT_EACH
                available_pts += QUIZ_WEIGHT_EACH

        if quiz_scores:
            quiz_avg = sum(quiz_scores) / len(quiz_scores)
            quiz_pct = (quiz_avg / MAX_QUIZ) * 100
            print(f"  Quizzes ({len(quiz_scores)}/10): promedio {quiz_avg:.1f}/{MAX_QUIZ} ({quiz_pct:.0f}%)")
            for qcol in QUIZ_COLS:
                val = row.get(qcol, "").strip()
                if val:
                    print(f"    {qcol}: {val}/{MAX_QUIZ}")
        else:
            print(f"  Quizzes: sin notas aún")

        # --- Other assessments ---
        OTHER_ASSESSMENTS = [
            ("Tarea 1", 10), ("Tarea 2", 10), ("Examen Parcial", 20),
            ("Tarea 3", 10), ("Tarea 4", 10), ("Proyecto Final", 30),
        ]
        for assessment, weight in OTHER_ASSESSMENTS:
            val = row.get(assessment, "").strip()
            if val:
                score = float(val)
                max_score = ASSESSMENT_MAX[assessment]
                pct = (score / max_score) * 100
                earned_pts += (score / max_score) * weight
                available_pts += weight
                print(f"  {assessment} ({weight}%): {score}/{max_score} ({pct:.0f}%)")
            else:
                print(f"  {assessment} ({weight}%): —")

        # --- Current standing & projection ---
        print()
        if available_pts > 0:
            current_pct = (earned_pts / available_pts) * 100
            projected = current_pct  # if they maintain same level across all 100%
            print(f"  Rendimiento actual: {earned_pts:.1f}/{available_pts:.1f} pts evaluados ({current_pct:.0f}%)")
            print(f"  → Nota proyectada si mantiene el ritmo: {projected:.0f}/100")
        else:
            print(f"  Sin evaluaciones registradas aún.")

    # --- Class averages ---
    print("\n" + "=" * 70)
    print("PROMEDIOS DEL CURSO")
    print("-" * 70)

    all_current_pcts = []
    for row in rows:
        earned = 0.0
        avail = 0.0
        for qcol in QUIZ_COLS:
            val = row.get(qcol, "").strip()
            if val:
                earned += (float(val) / MAX_QUIZ) * QUIZ_WEIGHT_EACH
                avail += QUIZ_WEIGHT_EACH
        for assessment, weight in OTHER_ASSESSMENTS:
            val = row.get(assessment, "").strip()
            if val:
                earned += (float(val) / ASSESSMENT_MAX[assessment]) * weight
                avail += weight
        if avail > 0:
            all_current_pcts.append((earned / avail) * 100)

    if all_current_pcts:
        avg = sum(all_current_pcts) / len(all_current_pcts)
        best = max(all_current_pcts)
        worst = min(all_current_pcts)
        print(f"  Promedio del curso: {avg:.0f}%")
        print(f"  Mejor rendimiento: {best:.0f}%")
        print(f"  Menor rendimiento: {worst:.0f}%")

    print("\n" + "=" * 70)
    print("Ponderación: Quizzes 10% | Tareas 10% c/u | Parcial 20% | Proyecto 30%")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Gestión del Gradebook NLP UCB")
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # show
    subparsers.add_parser("show", help="Mostrar gradebook actual")

    # set
    p_set = subparsers.add_parser("set", help="Establecer una nota")
    p_set.add_argument("--student", required=True, help="Email parcial o nombre del estudiante")
    p_set.add_argument("--assessment", required=True, help="Nombre de la evaluación (ej: 'Quiz 2')")
    p_set.add_argument("--grade", required=True, type=float, help="Nota a asignar")

    # summary
    subparsers.add_parser("summary", help="Resumen ponderado de notas")

    args = parser.parse_args()

    if args.command == "show":
        cmd_show(args)
    elif args.command == "set":
        cmd_set(args)
    elif args.command == "summary":
        cmd_summary(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
