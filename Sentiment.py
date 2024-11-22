class Sentiment:
    def __init__(self) -> None:
        """
        Initializes the Hugging Face sentiment model
        """
        from transformers import pipeline, logging

        logging.set_verbosity_error()

        self.pipeline = pipeline("text-classification", model="ProsusAI/finbert")
        # https://huggingface.co/ProsusAI/finbert?text=Is+AMD+Stock+A+Buy+As+Chipmaker+Gains+Market+Share+...%5CnInvestor%27s+Business+Daily%5Cnhttps%3A%2F%2Fwww.investors.com+%E2%80%BA+news+%E2%80%BA+technology+%E2%80%BA+amd-...&library=transformers

    def get_sentiment(self, sentence: list[str]) -> dict:
        """
        Given strings, returns an array of sentiment scores from -1 to 1
        """
        sentiments = []

        results = self.pipeline(sentence, padding=True, truncation=True)
        for result in results:
            label, score = result.values()
            print(label, score)
            
            if label == "neutral":
                sentiments.append(float(score) - 0.5)
            else:
                score = float(-1.0 * score) if label == "negative" else float(score)
                sentiments.append(score)

        return sentiments


if __name__ == "__main__":
    s = Sentiment()
    res = s.get_sentiment("eat a bag of dicks")

    print(res)
