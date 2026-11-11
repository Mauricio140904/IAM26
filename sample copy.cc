#include <iostream>
#include <fstream>
#include <cmath>

int main() {
    std::ifstream inputFile("sums.txt");
    
    std::ofstream meanFile("means.txt");
    std::ofstream varianceFile("variances.txt");

    double SUM_MEAN = 0;
    double VAR_MEAN = 0;
    const int n = 9;          
    const int total_runs = 26; 
    double block[n];         

    for (int j = 0; j < total_runs; ++j) {
        double sum = 0.0;

        for (int i = 0; i < n; ++i) {
            inputFile >> block[i];
            sum += block[i];
        }

        double mean = sum / n;
        meanFile << mean << "\n";
        SUM_MEAN += mean;

        double variance_sum = 0.0;
        for (int i = 0; i < n; ++i) {
            variance_sum += std::pow(block[i] - mean, 2);
        }
        double variance = variance_sum / n;
        varianceFile << variance << "\n";
        VAR_MEAN += variance;
    }

    meanFile << SUM_MEAN << "\n";
    varianceFile << VAR_MEAN << "\n";
    
    inputFile.close();
    meanFile.close();
    varianceFile.close();
}
