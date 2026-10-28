#include <iostream>
#include <fstream>

int main() {
    std::ifstream inputFile("sums.txt");

    double a;
    double sum = 0;
    int n = 0;
    while (inputFile >> a) {
        sum += a;
        ++n;
    }

    std::cout << "Sum: " << sum << ", Count: " << n << std::endl;
    double mean = sum / n;
    std::cout << "Mean: " << mean << std::endl;

    std::ifstream inputFile2("sums.txt");
    double deviationSum = 0;
    while (inputFile2 >> a) {
        double deviation = a - mean;
        deviationSum += deviation * deviation;
    }
    double variance = deviationSum / n;
    std::cout << "Variance: " << variance << std::endl;
    double standardDeviation = std::sqrt(variance);
    std::cout << "Standard Deviation: " << standardDeviation << std::endl;
    
    inputFile.close();
    inputFile2.close();
}
