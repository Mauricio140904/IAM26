#include <iostream>
#include <fstream>
#include <string>
#include <sstream> 

int main() {
    std::ifstream inputFile("data.txt");

    std::ofstream outputFile("sums.txt");

    std::string currentLine;
    int lineCount = 0;

    while (std::getline(inputFile, currentLine)) {
        lineCount++;
        std::stringstream ss(currentLine);
        double num1 = 0.0, num2 = 0.0;

        if (ss >> num1 >> num2) {
            double sum = num1 + num2;
            outputFile << sum << std::endl;
        } else { continue; }
    }

    inputFile.close();
    outputFile.close();

    std::cout << "Successfully processed " << lineCount << " lines. Results saved to 'sums.txt'." << std::endl;

    return 0;
}