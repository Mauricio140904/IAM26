#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <vector>

double poisson(int k, double mu) {
    return (std::pow(mu, k) * std::exp(-mu)) / std::tgamma(k + 1);
}

double prob(const std::vector<int>& data, double mu) {
    double likelihood = 1.0;

    for (int k : data) {
        likelihood *= poisson(k, mu);
    }

    return likelihood;
}

double logPoisson(int k, double mu) {
    if (mu == 0.0) {
        return (k == 0)
            ? 0.0
            : -std::numeric_limits<double>::infinity();
    }

    return k * std::log(mu) - mu - std::lgamma(k + 1.0);
}

double nll(const std::vector<int>& data, double mu) {
    double result = 0.0;

    for (int k : data) {
        result -= 2.0 * logPoisson(k, mu);
    }

    return result;
}

int main() {
std::ifstream input("sums.txt");

    std::vector<int> data;
    double sum = 0.0;
    int number;

    while (input >> number) {
        data.push_back(number);
        sum += number;
    }

    const double N = static_cast<double>(data.size());
    const double mean = sum / N;
    double squaredDeviationSum = 0.0;
    for (int k : data) {
        squaredDeviationSum += (k - mean) * (k - mean);
    }
    const double standardDeviation = std::sqrt(squaredDeviationSum / N);
    const double minimumNll = nll(data, mean);

    // Aufgabe a
    std::cout << std::setprecision(12);
    std::cout << "N = " << data.size() << '\n';
    std::cout << "Mean = " << mean << '\n';
    std::cout << "L(mean) = " << prob(data, mean) << '\n';
    

    std::ofstream likelihoodFile("likelihood.txt");
    std::ofstream nllFile("nll.txt");
    std::ofstream deltaFile("deltanll.txt");

    likelihoodFile << std::setprecision(12);
    nllFile << std::setprecision(12);
    deltaFile << std::setprecision(12);

    // Aufgaben b, c, d
    for (int i = 0; i <= 600; ++i) {
        double mu = i * 0.01;
        double value = nll(data, mu);

        likelihoodFile << mu << " " << prob(data, mu) << '\n';
        nllFile << mu << " " << value << '\n';
        deltaFile << mu << " " << value - minimumNll << '\n';
    }
    
    std::cout << "-2 log(prob(data, 1)) = " << -2.0 * std::log(prob(data, 1.0)) << '\n';
    std::cout << "nll(data, 1) = " << nll(data, 1.0) << '\n';

    double left = 0.0;
    double right = mean;
    //Aufgabe d
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
    
    std::cout << "Delta < 1 interval: " << lower << " to " << upper << '\n';
    std::cout << "Delta < 1 uncertainties: -" << mean - lower << ", +" << upper - mean << '\n';
    std::cout << "Standard error from sheet 2: " << standardDeviation / std::sqrt(N) << '\n';
    std::cout << "Poisson standard error: " << std::sqrt(mean / N) << '\n';

    // Aufgabe e
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

    likelihoodFile.close();
    nllFile.close();
    deltaFile.close();

}