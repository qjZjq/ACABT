assert __name__ == "__main__"

from expand import gen_adversary, refine


from openai import  OpenAI
client = OpenAI(
    api_key = "sk-89d43b4e34fa487a92311a78c8a393ab",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",     # qwen
    # base_url = "https://api.chatanywhere.tech/v1",
    # api_key = "sk-RDAwatfI7Vb9M5RSvKHPuq7g73KiFk6gVyQlOYJAK6eRF9Zz",    # GPT 4
    # base_url = "https://api.deepseek.com",
    # api_key = "sk-da6caca47a634462b9cb894ad5d17667",                    # Deepseek V3.2
)
def api(msgs):
    if isinstance(msgs, str):
        msgs = [{"role": "user", "content": msgs}]
    res = client.chat.completions.create(
        model = "qwen3-max",
        # model = "gpt-4",
        # model = "deepseek-v3",
        # model = "deepseek-chat",
        messages = msgs
    )
    return res.choices[0].message.content

query = "Let ${\triangle ABC}$ be a right triangle with $\angle A = 90^\circ$ and $BC = 38.$ There exist points $K$ and $L$ inside the triangle such\[AK = AL = BK = CL = KL = 14.\]The area of the quadrilateral $BKLC$ can be expressed as $n\sqrt3$ for some positive integer $n.$ Find $n.$"

thinking = api(query + "\nLet's think step by step.")

ans0 = api([
    {"role": "user", "content": query + "\nLet's think step by step."},
    {"role": "assistant", "content": thinking},
    {"role": "user", "content": "Summarize your answer into a short solution:"},
])

exit(0)
adv = gen_adversary(api, query, ans0)
ans1 = refine(api, query, ans0, adv, num = 1)[0]

print("ANS0:")
print("(Thinking)", thinking)
print("(answer)", ans0)
print("#"*100)
print("ADVERSARY:")
print(adv)
print("#"*100)
print("REFINE:")
print(ans1)
print("#"*100)

eval = api(f"""For the question:
{query}

The original answer is:
{ans0}

It has the following shortcoming:
{adv}

A new version of the answer is:
{ans1}

Does the answer solve the shortcoming and get improved from the previous answer? Give \"Yes\" or \"No\" and then the reason:""")
print(eval)