# Instrumentation and Analysis Methods – Exercise Sheet 3

**Handout:** 4th Nov 2026 **Due:** 18th Nov 2026

## Exercise 1: Poisson distribution (8 points)

Compare the frequencies of the numbers in **sums.txt** with the predictions of the Poisson distribution. First update your fork with *Sync fork* on its GitHub page and run `git pull` in your working copy to get the new files and checks for this sheet. Please name your program **poisson.cc**.

a) (2 points) Count with a `std::vector<int>` how often the values $k$ - with $k$ ranging from 0 to 10 - appear in the file. Include the necessary include file with

   ``` cpp
   #include <vector>
   ```

   Create a `std::vector` object with eleven entries: `std::vector<int> counts(11);`\
   As on sheet 2, read all values $n_i$ from **sums.txt** until the end of the file, count them to get $N$, and compute their mean $\bar n$ in the same loop. Increment the corresponding entry in the vector for each value:

   ``` cpp
   counts.at(number) += 1;
   ```

   Unlike `counts[number]`, `counts.at(number)` checks that `number` is a valid index and stops the program with an error otherwise, instead of silently writing to memory outside the vector.\
   Print $N$, $\bar n$ and all entries of `counts` to the terminal

   ``` cpp
   for(unsigned int k = 0 ; k < counts.size() ; ++k)  {
     std::cout << k << ":" << counts[k] << std::endl;
   }
   ```

b) (2 points) Write out a file **hist.txt** with the result of a) in the format:

   ```
   0 12
   1 23
   2 53
   ...
   ```

   Visualize the contents of the file as a histogram. The easiest way is a *GitHub Codespace*: on the GitHub page of your fork click *Code*, *Codespaces*, *Create codespace on main*. This opens VS Code in your browser with g++, ROOT and Python with Matplotlib already installed, so you can also compile and run your programs there. Alternatively, install ROOT (macOS: `brew install root`, Windows: in WSL2) or Python with Matplotlib on your laptop.

   - with Python\
     Run the script provided in the repository

     ``` bash
     python3 plot_poisson.py hist.txt
     ```

     and open the created file **hist.png**. Have a look at the script: it uses **numpy.loadtxt** and **Matplotlib**.

   - with ROOT\
     Start ROOT in the terminal with `root -l` and then type:

     ``` cpp
     //create histogram with 11 bins from -0.5 to 10.5
     TH1D hist("hist","; N", 11, -0.5,10.5);
     //create TTree object and fill with file contents
     TTree t;
     t.ReadFile("hist.txt","N/I:counts/I");
     //fill histogram with entries in tree
     t.Draw("N >>hist","counts","HIST")
     ```

c) (2 points) Write a function `double poisson(double mu, int k)` that computes the Poisson probability $P(k,\mu) = \frac{\mu^ke^{-\mu}}{k!}$.\
   For the exponential function you can use `double exp(double x)` from **cmath** and the function `double pow(double x, double k)` for the $x^k$. The factorial can be computed via the gamma function $k! = \Gamma(k+1)$ with `double tgamma(double x)` from **cmath**.\
   Write a new file **histpoi.txt** that contains a third column with the expectation from the Poisson distribution $N \cdot P(k, \mu)$. Use the mean $\bar n$ from a) as value of the $\mu$ parameter. It should agree with the mean from sheet 2.\
   Compare the data with the prediction with `python3 plot_poisson.py histpoi.txt` or with ROOT:

   ``` cpp
   //create histogram with 11 bins from -0.5 to 10.5
   TH1D hist("hist","; N", 11, -0.5,10.5);
   //create TTree object and fill with file contents
   TTree t;
   t.ReadFile("histpoi.txt","N/I:counts/I:prediction/D");
   //fill histogram with entries in tree
   t.Draw("N >>hist","counts","HIST")
   t.Draw("N","prediction","HISTSAME")
   ```

d) (2 points) Discuss your result and submit your answers on Moodle:

   - The numbers in **sums.txt** are sums of the two numbers in each line of **data.txt**. Under which condition is such a sum again Poisson distributed?
   - For a Poisson distribution, mean and variance are equal. Compare the mean and the variance $V$ from sheet 2. Do you consider the difference significant?
   - The number of entries in each bin fluctuates around the prediction $N P(k,\mu)$ with a standard deviation of about $\sqrt{N P(k,\mu)}$. Are the differences between data and prediction compatible with these fluctuations?

Upload your program and the output files to GitHub:

``` bash
git add hist.txt histpoi.txt
git commit -m"sheet 3" poisson.cc hist.txt histpoi.txt
git push
```

The automatic check on GitHub also creates the plot from your **histpoi.txt**: open the *Actions* tab of your fork, select the latest run and download **sheet-3-plot** at the bottom of the page.

So far, we have simply used the mean as value for $\mu$. On the next sheet, we will determine $\mu$ and its uncertainty properly with a likelihood fit.
