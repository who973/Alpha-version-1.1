from collections import Counter
from typing import List, Dict


LABEL_MAP = {
    0: "negative",
    1: "neutral",
    2: "positive"
}
def build_report(predictions: List[int], data: List[Dict]) -> Dict:
    if len(predictions) != len(data):
        raise ValueError("Что то не то")

    labels = [LABEL_MAP[p] for p in predictions]
    counter = Counter(labels)

    total = sum(counter.values())
    reputation_index = (
        counter.get("positive", 0) - counter.get("negative", 0)
    ) / total if total > 0 else 0

    report = {
        "total_messages": total,
        "distribution": dict(counter),
        "reputation_index": round(reputation_index, 3)
    }

    return report


def print_report(report: Dict):
    print("\nОтчет\n")
    print(f"Всего сообщений: {report['total_messages']}")
    print("Распределение тональности:")

    for label, count in report["distribution"].items():
        print(f"{label}: {count}")

    print(f"Индекс репутации: {report['reputation_index']}")
