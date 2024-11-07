class Sentiment:
    def __init__(self) -> None:
        """
        Initializes the Hugging Face sentiment model
        """
        from transformers import pipeline, logging

        logging.set_verbosity_error()

        from transformers import pipeline
        self.pipeline = pipeline("sentiment-analysis")

    def get_sentiment(self, sentence: str) -> dict:
        """
        Given a string, returns a dictionary with 'label' and 'score'
        representing sentiment polarity and confidence
        """
        res = self.pipeline(sentence)
        return res


if __name__ == "__main__":
    s = Sentiment()
    res = s.get_sentiment("eat a bag of dicks")

    print(res)
