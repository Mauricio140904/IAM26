#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>

double poisson(int k, double mu) {
    return (std::pow(mu, k) * std::exp(-mu)) / std::tgamma(k + 1);
}

int main() {
    std::ifstream inputFile("sums.txt");

    std::vector<int> counts(11);

    int number;
    int N = 0;
    double sum = 0.0;
    while (inputFile >> number) {
        counts.at(number) += 1;
        sum += number;
        ++N;
    }

    double mu = sum / N;

    std::cout << "N: " << N << '\n';
    std::cout << "Mean: " << mu << '\n';

    std::ofstream histFile("hist.txt");
    std::ofstream histPoiFile("histpoi.txt");

    for (unsigned int k = 0; k < counts.size(); ++k) {
        std::cout << k << " " << counts[k] << std::endl;
        histFile << k << " " << counts[k] << '\n';
        histPoiFile << k << " " << counts[k] << " " << N * poisson(static_cast<int>(k), mu) << '\n';
    }    

    inputFile.close();
    histFile.close();
    histPoiFile.close();

    return 0;
}