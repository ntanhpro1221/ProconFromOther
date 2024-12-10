import subprocess
import json
import requests
import os

# THAM SỐ SERVER
url = "https://proconvn.duckdns.org"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjcsIm5hbWUiOiJIQVVJIiwiaXNfYWRtaW4iOmZhbHNlLCJpYXQiOjE3MzM4MzgxNDUsImV4cCI6MTczNDAxMDk0NX0.UOkUHLyWW5LaL-7O99MtmUNeyeqifKHlt-H6dnU5T6Q"
question_id = "67"

# CHẠY NHƯ THẾ NÀO
just_submit = False 
file_to_submit = ""
get_new_question = True

# TÙY CHỈNH SOLVE
start = 66
end = 66
step = 1
div = 10

# ĐỊA CHỈ FILE
input_path = "input.json"
output_path = "Output"
solver_path = "Solver/build/solver_2_8.exe"


def get_input():
    headers = {"Authorization": token}

    # request question from server
    print(f"Requesting question {question_id}")
    question = json.loads(requests.get(f"{url}/question/{question_id}", headers=headers).json()["question_data"])

    # write to file
    print("Writing to", input_path)
    with open(input_path, "w") as file:
        json.dump(question, file, indent=4, ensure_ascii=False)

    print("Done get question!")

def submit(output_path):
    headers = {"Authorization": token}

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

def submit_best_answer():
    best_step = 1000000000
    best_file = ""
    for filename in os.listdir(output_path):
        with open(output_path + "/" + filename, 'r') as file:
            data = json.load(file)
            if data['n'] < best_step:
                best_step = data['n']
                best_file = filename
    
    if input("Bạn có muốn submit lần chạy tốt nhất với " + str(best_step) + " bước của " + best_file + " không (Y/N): ").lower() == "y":
        submit(output_path + "/" + best_file)

def run_solution():
    # Chạy tất cả các solver
    processes = []
    for i in range(start, end + 1, step):
        left_ratio = i / div
        process = subprocess.Popen([
            solver_path, 
            input_path, 
            output_path + "/" + str(left_ratio) + ".json", 
            str(left_ratio)])
        processes.append(process)

    # Đợi tất cả các chương trình hoàn thành
    for process in processes:
        process.wait()

    print("Done all solve")

if just_submit: 
    # Submit luôn
    submit(output_path + "/" + file_to_submit + ".json")
else:
    # Lấy câu hỏi từ input_pathe
    if get_new_question: get_input()

    # Chạy solution với nhiều config
    run_solution()

    # Submit câu trả lời tốt nhất
    submit_best_answer()

# In chữ màu vàng
print("\033[33mLưu ý: các file trả lời trong folder output không tự động xóa!\033[0m")


