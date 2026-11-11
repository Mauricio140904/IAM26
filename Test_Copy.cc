#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <vector>

// Poisson probability P(k, mu).
double poisson(double mu, int k) {
    if (mu == 0.0) {
        return (k == 0) ? 1.0 : 0.0;
    }

    return std::pow(mu, k) * std::exp(-mu) / std::tgamma(k + 1.0);
}

// Likelihood, calculated as a product.
double prob(const std::vector<int>& data, double mu) {
    double likelihood = 1.0;

    for (int k : data) {
        likelihood *= poisson(mu, k);
    }

    return likelihood;
}

// Logarithm of P(k, mu), calculated without forming P first.
double logPoisson(double mu, int k) {
    if (mu == 0.0) {
        return (k == 0)
            ? 0.0
            : -std::numeric_limits<double>::infinity();
    }

    return k * std::log(mu) - mu - std::lgamma(k + 1.0);
}

// Returns -2 ln L(mu).
double nll(const std::vector<int>& data, double mu) {
    double result = 0.0;

    for (int k : data) {
        result -= 2.0 * logPoisson(mu, k);
    }

    return result;
}

int main() {
    std::ifstream input("sums.txt");
    if (!input) {
        std::cerr << "Could not open sums.txt\n";
        return 1;
    }

    std::vector<int> data;
    double sum = 0.0;
    int number;

    while (input >> number) {
        if (number < 0) {
            std::cerr << "Poisson observations must be nonnegative\n";
            return 1;
        }
        data.push_back(number);
        sum += number;
    }

    if (!input.eof() || data.empty()) {
        std::cerr << "Error reading sums.txt or file is empty\n";
        return 1;
    }

    const double N = static_cast<double>(data.size());
    const double mean = sum / N;

    // The given sample has a positive mean.
    if (mean <= 0.0 || data.size() < 2) {
        std::cerr << "This program expects at least two values "
                     "and a positive mean\n";
        return 1;
    }

    const double minimumNll = nll(data, mean);

    std::cout << std::setprecision(12);
    std::cout << "N = " << data.size() << '\n';
    std::cout << "Mean = " << mean << '\n';
    std::cout << "L(3.11538) = " << prob(data, 3.11538) << '\n';
    std::cout << "L(mean) = " << prob(data, mean) << '\n';

    // Illustrate the underflow problem in part c).
    std::cout << "-2 log(prob(data, 1)) = "
              << -2.0 * std::log(prob(data, 1.0)) << '\n';
    std::cout << "nll(data, 1) = " << nll(data, 1.0) << '\n';

    std::ofstream likelihoodFile("likelihood.txt");
    std::ofstream nllFile("nll.txt");
    std::ofstream deltaFile("deltanll.txt");

    if (!likelihoodFile || !nllFile || !deltaFile) {
        std::cerr << "Could not create output files\n";
        return 1;
    }

    likelihoodFile << std::setprecision(12);
    nllFile << std::setprecision(12);
    deltaFile << std::setprecision(12);

    // Scan from 0 to 6 in steps of 0.01.
    for (int i = 0; i <= 600; ++i) {
        double mu = i * 0.01;
        double value = nll(data, mu);

        likelihoodFile << mu << " " << prob(data, mu) << '\n';
        nllFile << mu << " " << value << '\n';
        deltaFile << mu << " " << value - minimumNll << '\n';
    }

    // Find the two Delta = 1 crossings by bisection.
    double left = 0.0;
    double right = mean;

    for (int i = 0; i < 80; ++i) {
        double middle = (left + right) / 2.0;
        if (nll(data, middle) - minimumNll > 1.0) {
            left = middle;
        } else {
            right = middle;
        }
    }
    double lower = (left + right) / 2.0;

    left = mean;
    right = mean + 1.0;
    while (nll(data, right) - minimumNll < 1.0) {
        right = mean + 2.0 * (right - mean);
    }

    for (int i = 0; i < 80; ++i) {
        double middle = (left + right) / 2.0;
        if (nll(data, middle) - minimumNll < 1.0) {
            left = middle;
        } else {
            right = middle;
        }
    }
    double upper = (left + right) / 2.0;

    std::cout << "Delta < 1 interval: " << lower
              << " to " << upper << '\n';
    std::cout << "Poisson standard error: "
              << std::sqrt(mean / N) << '\n';

    // Saturated model: each observation has its own mu_i = k_i.
    double saturatedNll = 0.0;
    for (int k : data) {
        saturatedNll -= 2.0 * logPoisson(static_cast<double>(k), k);
    }

    double deviance = minimumNll - saturatedNll;
    double ndof = N - 1.0;
    double z = (deviance - ndof) / std::sqrt(2.0 * ndof);

    std::cout << "-2 ln Lambda = " << deviance << '\n';
    std::cout << "ndof = " << ndof << '\n';
    std::cout << "chi-square approximation z = " << z << '\n';
    std::cout << "Simulation-based standardized deviation = "
              << (deviance - 254.0) / 24.0 << '\n';

    if (!likelihoodFile || !nllFile || !deltaFile) {
        std::cerr << "Error writing output files\n";
        return 1;
    }
}