# markov-chain-autocomplete

A Python snippet for autocompleting phrases by applying Marckov Chain Rule. It is a Supervised model. Needs training data in order to function.


## Training
Update data/queryCleanData.json with your own data. The first order key represents the group/project name.

Inside every project, the keys represent the phrases and values represents the number of times those phrases have occured.

```json
{
    "financeProject":{
        "i have taken loan":1,
        "i have taken mutual fund":2
    },
    "retailProject":{
        "i want to buy tofee":1,
        "i want to purchase a box of candies":2
    }
}
```
Once ready with data. Run the following command on your terminal to train on the given dataset

```sh
python train.py
```

### Running

In order to run the app, provide the project/group name as the first argument and query as the send. As followed

```sh
python run.py projectDemo "i have"
```
