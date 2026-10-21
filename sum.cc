#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

int main() {
    std::ifstream inputFile("data.txt");
    if (!inputFile) {
        std::cerr << "Error: Could not open 'data.txt'" << std::endl;
        return 1;
    }

    std::ofstream outputFile("sums.txt");
    if (!outputFile) {
        std::cerr << "Error: Could not create or open 'sums.txt'" << std::endl;
        inputFile.close();
        return 1;
    }

    std::string currentLine;
    int lineCount = 0;

    while (std::getline(inputFile, currentLine)) {
        lineCount++;
        std::stringstream ss(currentLine);
        double num1 = 0.0, num2 = 0.0;

        if (ss >> num1 >> num2) {
            double sum = num1 + num2;
            outputFile << "Line " << lineCount << " Sum: " << sum << std::endl;
        } else { continue; }
    }

    inputFile.close();
    outputFile.close();

    std::cout << "Successfully processed " << lineCount << " lines. Results saved to 'sums.txt'." << std::endl;

    return 0;
}