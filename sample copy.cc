#include <iostream>
#include <fstream>
#include <cmath>

int main() {
    // Open the input file containing the numbers
    std::ifstream inputFile("sums.txt");
    
    // Open the output files for writing the results
    std::ofstream meanFile("means.txt");
    std::ofstream varianceFile("variances.txt");

    // Check if files opened successfully
    if (!inputFile.is_open() || !meanFile.is_open() || !varianceFile.is_open()) {
        std::cerr << "Error opening one or more files." << std::endl;
        return 1;
    }

    const int n = 9;          // Numbers per group
    const int total_runs = 26; // Total groups to process
    double block[n];          // C++ array to store the 9 consecutive numbers

    for (int j = 0; j < total_runs; ++j) {
        double sum = 0.0;

        // 1. Read 9 numbers into the array and calculate the sum
        for (int i = 0; i < n; ++i) {
            if (!(inputFile >> block[i])) {
                std::cerr << "Error: Unexpected end of file or bad data at block " << j + 1 << std::endl;
                return 1;
            }
            sum += block[i];
        }

        // 2. Compute the mean for the current group
        double mean = sum / n;
        meanFile << mean << "\n";

        // 3. Compute the variance using the values stored in the array
        double variance_sum = 0.0;
        for (int i = 0; i < n; ++i) {
            variance_sum += std::pow(block[i] - mean, 2);
        }
        double variance = variance_sum / n;
        varianceFile << variance << "\n";
    }

    // Close all open file streams
    inputFile.close();
    meanFile.close();
    varianceFile.close();

    std::cout << "Successfully processed 26 groups. Results written to 'means.txt' and 'variances.txt'." << std::endl;
    return 0;
}