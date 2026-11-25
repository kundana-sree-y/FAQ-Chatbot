
import json
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "intents.json"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)


def load_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        intents = json.load(file)

    questions = []
    labels = []

    for intent in intents:

        for pattern in intent["patterns"]:

            questions.append(pattern)
            labels.append(intent["tag"])

    return questions, labels


def train_and_evaluate():

    print("\nLoading CampusAI dataset...")

    questions, labels = load_dataset()

    print(f"Total questions: {len(questions)}")
    print(f"Total intent categories: {len(set(labels))}")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        questions,
        labels,
        test_size=0.20,
        random_state=42,
        stratify=labels
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # Convert text into numerical features
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    X_train_vectors = vectorizer.fit_transform(X_train)
    X_test_vectors = vectorizer.transform(X_test)

    print("\nTF-IDF vectorization completed.")

    # Train the classifier
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train_vectors, y_train)

    print("Logistic Regression model trained.")

    # Evaluate on unseen test data
    predictions = model.predict(X_test_vectors)

    accuracy = accuracy_score(y_test, predictions)

    print("\n========== MODEL EVALUATION ==========")

    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    print("\nConfusion Matrix:")

    print(confusion_matrix(
        y_test,
        predictions,
        labels=model.classes_
    ))

    # Save trained model and vectorizer
    with open(MODEL_DIR / "campusai_model.pkl", "wb") as file:
        pickle.dump(model, file)

    with open(MODEL_DIR / "tfidf_vectorizer.pkl", "wb") as file:
        pickle.dump(vectorizer, file)

    print("\nModel saved successfully!")
    print("Saved inside the models folder.")

    print("\nCampusAI training completed.")


if __name__ == "__main__":
    train_and_evaluate()
