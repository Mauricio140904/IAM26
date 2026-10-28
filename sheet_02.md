# Instrumentation and Analysis Methods – Exercise Sheet 2

**Handout:** 28th Oct 2026 **Due:** 11th Nov 2026

## Exercise 1: Samples (3 points)

Compute the mean, the variance and the standard deviation of the sums that you have written to the file **sums.txt** on sheet 1. Use your fork of the IAM26 repository as for the last sheet. First update your fork with *Sync fork* on its GitHub page and run `git pull` in your working copy to get the new files and checks for this sheet. Please name your program **sample.cc**.

a) (1 point) Read in the $N=234$ numbers $a_i$ from the file **sums.txt** and compute the mean $\bar a$ using $\bar a = \langle a \rangle = \frac{1}{N}\sum_{i=1}^N a_i$. Instead of hard-coding $N$, read until the end of the file and count the numbers:

   ``` cpp
   double a;
   int n = 0;
   while (fin >> a) {
     sum += a;
     ++n;
   }
   ```

   Print out the result in the terminal.

b) (1 point) In your program, open the file a second time and again read in the $N$ numbers $a_i$. Use these to compute the variance of the sample with $V = \langle(a - \langle a\rangle)^2 \rangle = \frac{1}{N}\sum_{i=1}^N (a_i-\bar a)^2$. Print out the result in the terminal.

c) (1 point) Compute the standard deviation $\sigma = \sqrt{V}$ with the `sqrt` function from the `cmath` package:

   ``` cpp
   #include <cmath>
   ```

   Print out the result in the terminal.

Remark: With $V = \langle a^2 \rangle - \langle a \rangle^2$ you could compute the variance while reading the file only once. Why might the two-pass version still be preferred? Submit a short answer on Moodle.

## Exercise 2: Small samples (6 points)

a) (3 points) Extend your program from exercise 1 such that it computes the means and the variances $V_j = \frac{1}{n}\sum_{i=1}^{n} (a_i-\bar a_j)^2$ for each $n=9$ consecutive numbers in **sums.txt**. Write the 26 results in two new files, **means.txt** and **variances.txt** respectively. Work on a copy named **sample2.cc** of **sample.cc**. To create the copy in the terminal window type:

   ``` bash
   cp sample.cc sample2.cc
   ```

   Hint: Use two `std::ifstream` objects for the file **sums.txt** to first compute the mean and then read in the same nine numbers from the second object to compute the variance.

b) (2 points) Compute the mean of the 26 means and the mean of the 26 variances and compare them to $\bar a$ and $V$ from exercise 1. By which factor do the variances differ? Repeat the computation with Bessel's correction, $s_j^2 = \frac{1}{n-1}\sum_{i=1}^{n} (a_i-\bar a_j)^2$, and explain the result. Submit your numbers and your explanation on Moodle.

c) (1 point) Compute the standard deviation of the 26 means and compare it to $\sigma/\sqrt{9}$ with $\sigma$ from exercise 1. What does this tell you about the uncertainty of a mean? Submit your answer on Moodle.

Upload your programs and the output files to GitHub:

``` bash
git add means.txt variances.txt
git commit -m"sheet 2" sample.cc sample2.cc means.txt variances.txt
git push
```
