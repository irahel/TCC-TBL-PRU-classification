 def evaluate(self, gold):
        """
        Score the accuracy of the tagger against the gold standard.
        Strip the tags from the gold standard text, retag it using
        the tagger, then compute the accuracy score.

        :type gold: list(list(tuple(str, str)))
        :param gold: The list of tagged sentences to score the tagger on.
        :rtype: float
        """

        tagged_sents = self.tag_sents(untag(sent) for sent in gold)
        gold_tokens = list(chain(*gold))
        test_tokens = list(chain(*tagged_sents))
        return accuracy(gold_tokens, test_tokens)
    
 def tag_sents(self, sentences):
        """
        Apply ``self.tag()`` to each element of *sentences*.  I.e.:

            return [self.tag(sent) for sent in sentences]
        """
        return [self.tag(sent) for sent in sentences]    
