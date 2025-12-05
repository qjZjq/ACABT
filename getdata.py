import pandas as pd
import csv
import json
import re

def read(dataset):
    if dataset == "AIME25":
        with open("data/AIME25/test.jsonl", "r") as f:
            data = [json.loads(line.strip()) for line in f]
        return data, "Give a number as your answer"
    if dataset == "GSM8K":
        df = pd.read_parquet("data/GSM8K/main/train-00000-of-00001.parquet", engine = "pyarrow")
        data = [{
            "query": row["question"],
            "ans": int(row["answer"].split("####")[1])
        } for i, row in df.iterrows() if i <= 100]
        return data, "Give a number as your answer"
    if dataset == "ARC-Challenge":
        df = pd.read_parquet("data/ARCchallenge/data/test-00000-of-00001-a0c917350be4ccd9.parquet", engine = "pyarrow")
        data = [(row["question"], row["choices"], row["answerKey"]) for i, row in df.iterrows() if i <= 100]
        print(len(data))
        print(data[0])
        data = [{
            "query": (
                x[0]  + "\n" +
                "The options are:\n" +
                "\n".join([key + ". " + x[1]["text"][idx] for idx, key in enumerate(x[1]["label"])])        
            ),
            "ans": x[2],
        } for x in data]
        return data, "Give one capital letter of the label as your answer, with the format of \"[A/B/C...]\"."
    if dataset == "Game-of-24":
        with open("data/Gameof24/game24.csv", "r") as f:
            reader = csv.reader(f)
            data = [row for row in reader]
        data = [{
            "query": (
                "Let's play the game of 24.\n" + 
                "The 4 numbers are: " + d[1] + "\n" +
                "Find a way to manipulate with these numbers so that the end result is 24."
            ),
            "data": sorted(int(x) for x in re.findall(r"\d+", d[1])),
        } for d in data[1:101]]
        return data, "Give your solution in python executable form, such as \"8 * (2 + 4) / 2\"."

if __name__ == "__main__":
    df = read("Game-of-24")
    print(df.head())