import logging
from functools import cache

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from core.constants import TOXICITY_THRESHOLD

logger = logging.getLogger(__name__)
MODEL_NAME = 'cointegrated/rubert-tiny-toxicity'


@cache
def _load_model():
    """Загрузить токенизатор и модель один раз на процесс.

    При ошибке загрузки (нет интернета, нет кеша) возвращает (None, None).
    Модель не загружается при импорте — только при первом вызове is_toxic.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        model.eval()
        return tokenizer, model
    except Exception as exc:
        logger.warning(
            'ML-модель недоступна (%s). Комментарии проходят без модерации.',
            exc,
        )
        return None, None


def get_toxicity_score(text: str) -> float:
    """Вернуть оценку токсичности от 0 до 1."""
    tokenizer, model = _load_model()
    if model is None:
        return 0.0
    inputs = tokenizer(
        text,
        return_tensors='pt',
        truncation=True,
        padding=True,
    )
    with torch.inference_mode():
        logits = model(**inputs).logits
        proba = torch.sigmoid(logits).cpu().numpy()[0]
    return float(1 - proba[0] * (1 - proba[-1]))


def is_toxic(text: str) -> bool:
    """Определить, достигла ли оценка заданного порога."""
    return get_toxicity_score(text) >= TOXICITY_THRESHOLD
