# Instrumentation and Analysis Methods – Exercise Sheet 4

**Handout:** 11th Nov 2026 **Due:** 25th Nov 2026

## Exercise 1: Maximum likelihood method (8 points)

We estimate the parameter $\mu$ of the Poisson distribution for the sample from sheet 3 with the [maximum likelihood method](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation) and test with a [likelihood ratio](https://en.wikipedia.org/wiki/Likelihood-ratio_test) whether the Poisson distribution describes the data. First update your fork with *Sync fork* and run `git pull` to get the new files and checks. Please name your program **likelihood.cc**.

a) (2 points) Read the $N = 234$ values $k_i$ from **sums.txt** into a `std::vector<int> data`, appending each value with `data.push_back(number)`. Write a function

   ``` cpp
   double prob(const std::vector<int>& data, double mu)
   ```

   that returns the likelihood $\mathcal{L}(\mu) = \prod_{i=1}^{N} P(k_i,\mu)$, i.e. the probability to observe the sample, reusing `poisson` from sheet 3. The `const &` passes the vector by reference without copying it and prevents the function from changing it. Loop over the values with

   ``` cpp
   for(int k : data) {
     ...
   }
   ```

   Print $\mathcal{L}(\bar n)$ for the sample mean $\bar n = 3.11538$. It should be $7.76841\cdot 10^{-195}$.

b) (1 point) Write $\mu$ and $\mathcal{L}(\mu)$ for $0 \le \mu \le 6$ with a step size of 0.1 or smaller into **likelihood.txt**, one pair per line. Plot it, and zoom into $2.5 < \mu < 3.8$, with

   ``` bash
   python3 plot_likelihood.py likelihood.txt
   python3 plot_likelihood.py likelihood.txt 2.5 3.8
   ```

   or in ROOT (`root -l`) with `TGraph g("likelihood.txt"); g.Draw("AL")` (`A`: axes, `L`: line).\
   Where is the maximum and what does it mean?

c) (2 points) Write $\mu$ and $-2\ln \mathcal{L}(\mu)$ into **nll.txt**, first using `log` from **cmath** on the result of `prob`. What happens for $\mu \le 1$, and why?\
   Avoid the problem with $\ln \prod_i P(k_i,\mu) = \sum_i \ln P(k_i,\mu)$: write a function

   ``` cpp
   double nll(const std::vector<int>& data, double mu)
   ```

   that computes $-2\ln \mathcal{L}(\mu)$ as a sum, and use it for **nll.txt**. Only $\mu = 0$ may give an infinite value now. This is why fits minimise $-2\ln\mathcal{L}$ instead of maximising $\mathcal{L}$. Plot the file as in b).

d) (2 points) Write $\mu$ and $\Delta(\mu) = -2\ln \mathcal{L}(\mu) + 2\ln \mathcal{L}(\bar n)$ into **deltanll.txt** and plot it. Read off the minimum $\hat\mu$, the maximum likelihood estimate, and compare it with $\bar n$. Its uncertainty is given by the interval with $\Delta(\mu) < 1$; use a finer scan around $\hat\mu$ to determine it precisely. Compare the uncertainty with $\sigma/\sqrt{N}$, using the standard deviation $\sigma$ from sheet 2, and with $\sqrt{\hat\mu/N}$, expected for a Poisson distribution. Submit your answers on Moodle.

e) (1 point) The value of $\mathcal{L}(\hat\mu)$ alone says little about the quality of the description, since it gets smaller with every additional value. We therefore compare it with the best possible description, the *saturated model*, which gives every value its own parameter $\mu_i = k_i$:

   $$\Lambda = \frac{\prod_{i=1}^{N} P(k_i,\hat\mu)}{\prod_{i=1}^{N} P(k_i,k_i)} \qquad (\text{with } P(0,0) = 1).$$

   Print $-2\ln \Lambda$. For large expected counts, $-2\ln\Lambda$ follows a [$\chi^2$ distribution](https://en.wikipedia.org/wiki/Chi-square_distribution) with $n_\textrm{dof} = N - 1 = 233$ degrees of freedom, mean $n_\textrm{dof}$ and, approximately, standard deviation $\sqrt{2n_\textrm{dof}}$. Print the deviation $z = (-2\ln \Lambda - n_\textrm{dof})/\sqrt{2n_\textrm{dof}}$.\
   Here, however, each $k_i$ is a single small count, so the $\chi^2$ distribution is only a rough approximation: a simulation of many Poisson samples with $N = 234$ and $\mu = 3.1$ gives a mean of about 254 and a standard deviation of about 24 for $-2\ln\Lambda$. Does the Poisson distribution describe the data? Why does the $\chi^2$ approximation require large counts? Submit your answers on Moodle.

Upload your program and the output files to GitHub:

``` bash
git add likelihood.cc likelihood.txt nll.txt deltanll.txt
git commit -m"sheet 4"
git push
```

The automatic check on GitHub also creates plots from your **likelihood.txt**, **nll.txt** and **deltanll.txt**: open the *Actions* tab of your fork, select the latest run and download **sheet-4-plots** at the bottom of the page.
