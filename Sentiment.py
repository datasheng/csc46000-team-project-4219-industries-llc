class Sentiment:
    def __init__(self) -> None:
        """
        Initializes the Hugging Face sentiment model
        """
        from transformers import pipeline, logging

        logging.set_verbosity_error()

        self.pipeline = pipeline("sentiment-analysis")

    def get_sentiment(self, sentence: list[str]) -> dict:
        """
        Given strings, returns an array of sentiment scores from -1 to 1
        """
        sentiments = []

        results = self.pipeline(sentence)

        for result in results:
            label, score = result.values()
            score = -1 * score if label == "NEGATIVE" else score
            sentiments.append(score)
        
        return sentiments


if __name__ == "__main__":
    s = Sentiment()
    res = s.get_sentiment("eat a bag of dicks")

    print(res)
