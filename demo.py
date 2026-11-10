
from pathlib import Path

from config import DOCUMENTS_DIR


NO_ANSWER = (
    "לא נמצא מידע במסמכי ועד הבית "
    "שמאפשר לענות על השאלה."
)


def answer_demo(question: str):
    """
    Demonstration mode.

    Uses predefined answers and checks whether the
    relevant information exists in the sample files.

    This is NOT an actual RAG or vector search.
    """

    question = question.strip()

    if not question:
        return "יש להקליד שאלה.", []

    rules = [
        {
            "keywords": ["כמה", "ועד", "תשלום", "דמי"],
            "document": "payments.txt",
            "required_text": '250 ש"ח',
            "answer": 'דמי ועד הבית הם 250 ש"ח לחודש.',
        },
        {
            "keywords": ["מתי", "לשלם", "תשלום"],
            "document": "payments.txt",
            "required_text": "עד ה-10",
            "answer": "יש לשלם את דמי ועד הבית עד ה-10 בכל חודש.",
        },
        {
            "keywords": ["ניקיון", "מנקים", "מנוקה"],
            "document": "maintenance.txt",
            "required_text": "ראשון ורביעי",
            "answer": "חדר המדרגות מנוקה בימי ראשון ורביעי.",
        },
        {
            "keywords": ["מעלית", "תקלה"],
            "document": "maintenance.txt",
            "required_text": "לנציג ועד הבית",
            "answer": "במקרה של תקלה במעלית יש לדווח לנציג ועד הבית.",
        },
        {
            "keywords": ["שקט", "רעש"],
            "document": "rules.txt",
            "required_text": "14:00",
            "answer": (
                "שעות השקט הן 14:00–16:00 "
                "ו-23:00–07:00."
            ),
        },
    ]

    for rule in rules:
        path = DOCUMENTS_DIR / rule["document"]

        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8")

        if rule["required_text"] not in content:
            continue

        if any(word in question for word in rule["keywords"]):
            return rule["answer"], [rule["document"]]

    return NO_ANSWER, []
