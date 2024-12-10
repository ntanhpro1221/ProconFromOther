# swagger doc: https://proconvn.duckdns.org/docs

import requests
import json
import sys

def VNU():
    url = "https://proconvn.duckdns.org"
    token = sys.argv[1]
    question_id = int(sys.argv[2])
    output_path = sys.argv[3]
    headers = {"Authorization": token}

    if len(sys.argv) != 0 and sys.argv[0].isdigit():
        question_id = int(sys.argv[0])

    # request steps from file
    print("Getting steps from", output_path)
    with open(output_path, "r") as file:
        steps = json.loads(file.read())

    # send your answer to server
    print("Submiting answer to server")
    payload = {"question_id": question_id, "answer_data": steps}
    res = requests.post(f"{url}/answer", json=payload, headers=headers).json()

    #  get your answer id
    answer_id = res["id"]

    # get your answer and score from server
    answer = requests.get(f"{url}/answer/{answer_id}", headers=headers).json()
    score_data = json.loads(answer["score_data"])
    print("final score:", score_data["final_score"])

def LOCAL():
    url = sys.argv[1]
    token = sys.argv[2]
    output_path = sys.argv[3]
    headers = {
        "Content-Type": "application/json",
        "Procon-Token": token
    }

    # load answer
    print(f"Get answer from {output_path}")
    with open(output_path, 'r') as file:
        answer = json.loads(file.read())

    # request question from server
    print(f"Submiting answer")
    result = requests.post(f"{url}/answer", headers=headers, json=answer)

    print(result)

def JUDGE():
    url = sys.argv[1]
    token = sys.argv[2]
    output_path = sys.argv[3]
    input_path = sys.argv[4]
    print("\nJUDGING...")

    # load question
    print(f"Get question from {input_path}")
    with open(input_path, 'r') as file:
        question = json.loads(file.read())

    # load answer
    print(f"Get answer from {output_path}")
    with open(output_path, 'r') as file:
        answer = json.loads(file.read())
    
    factor = 0.3

    print(f"==> Number of step: {answer['n']}")
    print(f"==> Point: {question["board"]["width"] * question["board"]["height"] - factor * answer["n"]}")

JUDGE()