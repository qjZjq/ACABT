from openai import OpenAI

client = OpenAI(
    api_key = "sk-89d43b4e34fa487a92311a78c8a393ab",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    # base_url = "https://api.chatanywhere.tech/v1",
    # api_key = "sk-RDAwatfI7Vb9M5RSvKHPuq7g73KiFk6gVyQlOYJAK6eRF9Zz",
)
def api(msgs):
    if isinstance(msgs, str):
        msgs = [{"role": "user", "content": msgs}]
    res = client.chat.completions.create(
        # model = "gpt-4",
        model = "qwen3-max",
        messages = msgs,
        max_tokens = 2000,
    )
    return res.choices[0].message.content


from baselines.run import baselines
from AnsTree.main_loop import run
from getdata import read

import re
import json

data, ans_format = read("AIME25")

if True:
    CoTs = []
    cnt = 0
    for x in data:
        res, info = baselines(api, "reflexion", x["problem"], ans_format, iter = 10)
        CoTs.append(info)
        try:
            ans = int(res)
            if ans != x["answer"]:
                print("WA:", res, "ANS:", x["answer"])
            else:
                print("CORRECT")
                cnt += 1
        except:
            print("WA:", res, "ANS:", x["answer"])
    print(cnt)
    
    with open("reflexion_log.json", "w") as f:
        json.dump(CoTs, f)
else:
    cnt = 0
    for x in data:
        res, info = run(api, x["query"], iter = 4, answer_format = ans_format)
        options = re.findall(r"\[[A-Z]\]", res)
        if options:
            if options[0][1] == x["ans"]:
                print("CORRECT")
            else:
                print("WA:", res, "ANS:", x["ans"])
        else:
            print("WA:", res, "ANS:", x["ans"])
    print(cnt)