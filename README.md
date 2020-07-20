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
