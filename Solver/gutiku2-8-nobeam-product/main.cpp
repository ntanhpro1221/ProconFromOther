#include "solver.hpp"
#include "../include/header/kyougi_app.h"

#include <iostream>
#include <string>
#include <fstream>
#include <cstdlib>
#include <iomanip>

string input_path;
string output_path;

class Solver_Interface {
public:
    Solver_Interface(float left_ratio, std::unique_ptr<ISolver> solver) :
        solver_(std::move(solver))
        {
            solver_->init(left_ratio);
        }

    void start() {
        receive_problem(); //受信ループ 問題を受信したら終了

        solver_->solve();//解答 解き終わったら終了

        save_answer(solver_->get_answer());
    }

    void receive_problem() {
        std::string problem;
        std::ifstream f(input_path);
        string tmp;
        while (f >> tmp)
            problem += tmp;
        f.close();
        solver_->set_problem(problem);
    }

    static void save_answer(const std::string& answer){
        std::ofstream out_stream(output_path);
        out_stream << answer;
        out_stream.close();
    };

    std::unique_ptr<ISolver> solver_;
};

int main(int argc, char *argv[]){
    input_path = argv[1];
    output_path = argv[2];
    float left_ratio = atof(argv[3]);

    std::ostringstream oss;
    oss << std::fixed << std::setprecision(2) << "start solve " << left_ratio << '\n';
    std::cout << oss.str();
    auto start = std::chrono::high_resolution_clock::now();

    Solver_Interface receiver(left_ratio, std::move(std::make_unique<Solver>()));
    receiver.start(); 

    auto end = std::chrono::high_resolution_clock::now(); 
    std::chrono::duration<double> elapsed = end - start;
    oss = std::ostringstream();
    oss << std::fixed << std::setprecision(2) << "finish solve " << left_ratio << " in " << elapsed.count() << " seconds | " << 
        receiver.solver_->get_step() << " steps" << '\n';
    std::cout << oss.str();
    
    return 0;
}