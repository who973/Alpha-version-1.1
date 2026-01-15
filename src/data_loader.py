import os
import csv
from collections import Counter


LABEL_MAPPING = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}


def load_csv(path: str) -> list:
    """
    Загружает CSV с колонками: text,label,id
    Возвращает сырые данные без фильтрации.
    """
    data = []

    with open(path, mode="r", encoding="utf-8-sig", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        required_columns = {"text", "label", "id"}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                f"CSV должен содержать колонки {required_columns}, найдено: {reader.fieldnames}"
            )

        for row in reader:
            data.append({
                "id": row["id"].strip(),
                "text": row["text"].strip(),
                "label": row["label"].strip().lower()
            })

    return data


def load_data(path: str, min_text_len: int = 5) -> list:
    """
    Полная загрузка + валидация + маппинг меток.
    Возвращает список словарей:
    {id, text, label}
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл {path} не найден")

    if not path.lower().endswith(".csv"):
        raise ValueError("Поддерживается только формат CSV")

    raw_data = load_csv(path)

    validated_data = []
    dropped = 0

    for row in raw_data:
        text = row["text"]
        label_str = row["label"]

        if not text or len(text) < min_text_len:
            dropped += 1
            continue

        if label_str not in LABEL_MAPPING:
            dropped += 1
            continue

        validated_data.append({
            "id": row["id"],
            "text": text,
            "label": LABEL_MAPPING[label_str]
        })

    label_stats = Counter(x["label"] for x in validated_data)

    print(
        f"Загружено: {len(raw_data)}, "
        f"принято: {len(validated_data)}, "
        f"отброшено: {dropped}"
    )
    print(f"Распределение классов (0=neg,1=neu,2=pos): {dict(label_stats)}")

    return validated_data

