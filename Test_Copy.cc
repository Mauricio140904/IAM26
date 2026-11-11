#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <vector>

double poisson(double mu, int k) {
    return std::pow(mu, k) * std::exp(-mu) / std::tgamma(k + 1);
}

int main() {
    std::ifstream input("sums.txt");
    if (!input) {
        std::cerr << "Could not open sums.txt\n";
        return 1;
    }

    std::vector<int> counts(11);
    long long N = 0;
    double sum = 0.0;
    double sum_squares = 0.0;
    int number;

    while (input >> number) {
        if (number < 0 || number > 10) {
            std::cerr << "Value outside the range 0–10: " << number << '\n';
            return 1;
        }

        counts.at(number) += 1;
        ++N;
        sum += number;
        sum_squares += number * number;
    }

    if (!input.eof()) {
        std::cerr << "Error reading sums.txt\n";
        return 1;
    }
    if (N == 0) {
        std::cerr << "sums.txt contains no values\n";
        return 1;
    }

    const double mean = sum / N;

    std::cout << std::setprecision(10);
    std::cout << "N: " << N << '\n';
    std::cout << "Mean: " << mean << '\n';

    // Sample variance, useful for part d).
    if (N > 1) {
        const double variance = (sum_squares - sum * sum / N) / (N - 1);
        std::cout << "Sample variance: " << variance << '\n';
    }

    std::ofstream hist("hist.txt");
    std::ofstream histpoi("histpoi.txt");
    if (!hist || !histpoi) {
        std::cerr << "Could not create output files\n";
        return 1;
    }

    histpoi << std::setprecision(12);
    for (unsigned int k = 0; k < counts.size(); ++k) {
        const double prediction = N * poisson(mean, static_cast<int>(k));

        std::cout << k << ":" << counts[k] << '\n';
        hist << k << ' ' << counts[k] << '\n';
        histpoi << k << ' ' << counts[k] << ' ' << prediction << '\n';
    }

    if (!hist || !histpoi) {
        std::cerr << "Error writing output files\n";
        return 1;
    }
}