# markov-chain-autocomplete

A Python snippet for autocompleting phrases by applying Marckov Chain Rule. It is a Supervised model. Needs training data in order to function.


## Training
Update data/queryCleanData.json with your own data. The keys in this json represent the phrases and values represents the number of times those phrases have occured.

```json
{
        "i have taken loan":1,
        "i have taken mutual fund":2,
        "i want to buy tofee":1,
        "i want to purchase a box of candies":2
}
```
Once ready with data. Run the following command on your terminal to train on the given dataset

```sh
python train.py
```

### Running

In order to run the app, provide thequery phrase name as the first argument. As followed

```sh
python run.py "i have"
```
Once this is run, it should show following output

```sh
{'query': 'i have', 'prediction': [{'phrase': 'taken loan', 'logProbability': -0.40546510810816444}, {'phrase': 'taken mutual fund', 'logProbability': -1.0986122886681098}], 'phraseLogProbability': -0.6931471805599453}
```

The query contains the request query.
In prediction, it shows the list of possible next phrases with their respective log probability.
phraseLongProbability is the log probability of the current requested phrase.
