import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer
from data.load import load_all

def train():
    data = load_all()
    labels = [item.label for item in data]

    train_data, test_data = train_test_split(
        data, test_size=0.2, random_state=42, stratify=labels
    )

    train_prompts = [item.prompt for item in train_data]
    train_labels = [item.label for item in train_data]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    train_embeddings = model.encode(train_prompts)

    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(train_embeddings, train_labels)

    joblib.dump(classifier, "detectors/classifier_model.joblib")
    print("Model trained and saved.")

    return test_data  ##return this so we can evaluate right after training, in the same run

if __name__ == "__main__":
    train()