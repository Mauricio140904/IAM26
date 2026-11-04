#include <iostream>
#include <fstream>
#include <cmath>

int main() {
    std::ifstream inputFile("sums.txt");
    
    std::ofstream meanFile("means.txt");
    std::ofstream varianceFile("variances.txt");

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

        double variance_sum = 0.0;
        for (int i = 0; i < n; ++i) {
            variance_sum += std::pow(block[i] - mean, 2);
        }
        double variance = variance_sum / n;
        varianceFile << variance << "\n";
    }

    meanFile.close();
    varianceFile.close();

    std::ifstream meanInput("means.txt");
    std::ifstream varianceInput("variances.txt");

    double overall_mean = 0.0;
    for (int j = 0; j < total_runs; ++j) {
        double mean;
        meanInput >> mean;
        overall_mean += mean;
    }
    overall_mean /= total_runs;

    double overall_variance = 0.0;
    for (int j = 0; j < total_runs; ++j) {
        double variance;
        varianceInput >> variance;
        overall_variance += variance;
    }
    overall_variance /= total_runs;

    std::cout << "Overall mean of means: " << overall_mean << "\n";
    std::cout << "Overall mean of variances: " << overall_variance << "\n";

    double bessel_correction = (n > 1) ? (n / (n - 1.0)) : 1.0;
    double corrected_variance = overall_variance * bessel_correction;
    std::cout << "Corrected variance: " << corrected_variance << "\n";

    meanInput.clear();
    meanInput.seekg(0);

    double squared_deviation_sum = 0.0;
    for (int j = 0; j < total_runs; ++j) {
        double mean;
        meanInput >> mean;
        squared_deviation_sum += std::pow(mean - overall_mean, 2);
    }

    double standard_deviation_of_means = std::sqrt(squared_deviation_sum / (total_runs - 1));

    std::cout << "Standard Deviation of means: " << standard_deviation_of_means << "\n";

    inputFile.close();
    meanInput.close();
    varianceInput.close();
}
