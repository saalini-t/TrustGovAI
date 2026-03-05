from transformers import pipeline

nli_model = pipeline("text-classification", model="facebook/bart-large-mnli")


def verify_entailment(context, answer):

    result = nli_model(
        answer,
        candidate_labels=[context]
    )

    score = result["scores"][0]

    return score