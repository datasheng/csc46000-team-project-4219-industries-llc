class Sentiment:
    def __init__(self) -> None:
        """
        inits hugginface sentiment model
        """
        from transformers import pipeline

        model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        self.sentiment_task = pipeline(
            "sentiment-analysis", model=model_path, tokenizer=model_path
        )

        pass

    def get_sentiment(self, sentence: str) -> int:
        """
        given a string, returns an integer on the range of 1-10
        with 1 being extremely negative
        10 being extremely positive
        """
        res = self.sentiment_task("i fucking hate you, but i love you")
        print(res)
        pass


if __name__ == "__main__":
    s = Sentiment()
    s.get_sentiment()
