# Instrumentation and Analysis Methods – Exercise Sheet 1

**Handout:** 21st Oct 2026 **Due:** 4th Nov 2026

## Exercise 1: Let’s start (3 points)

We will try to use freely available online tools for these exercises where possible. The exercises are provided in the GitHub repository <https://github.com/stadie/IAM26>.\
Open the link and click *Fork* (top right) to create your own copy of the repository, owned by your GitHub account. In your fork, open the *Actions* tab and click *I understand my workflows, go ahead and enable them*, so that your solutions are checked automatically after each push. Your fork is public. When new exercises are added, update your fork with *Sync fork* on its GitHub page. Post the URL of your fork on Moodle so that we can look at your solutions.\
With <https://replit.com/> you can get an integrated development environment (IDE) in your browser. Log in with your GitHub account and import your fork. If you want to work locally, clone your fork:

``` bash
git clone https://github.com/<your-username>/IAM26.git
```

Type the following program code into the file **hello.cc**:

``` cpp
#include<iostream>
    
int main() {
  std::cout << "Hello World!" << std::endl;
}
```

Compile and execute the program in the terminal window on the (lower) right:

``` bash
g++ hello.cc -o hello
./hello
```

Before your first commit, tell git your name and the e-mail address of your GitHub account (only once per computer):

``` bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

If the program works you can update the files on GitHub with your changes:

``` bash
git commit -m"first attempt" hello.cc
git push
```

You will be asked for your GitHub account name and your [personal access token, which you have to create on GitHub beforehand](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). In <https://replit.com/> you can also use the *Version control* tab on the left side of the screen.

## Exercise 2: Input and Output (7 points)

<u>From the lecture:</u>\
Input and output (terminal):

``` cpp
int number;
std::cin >> number;
std::cout << number << std::endl;
```

Output (file):

``` cpp
#include <fstream>
...
std::ofstream fout("output.txt");
fout << number << std::endl;
fout.close();
```

Input (file):

``` cpp
#include <fstream>
...
std::ifstream fin("input.txt");
int number;
fin >> number;
fin.close();
```

Dump contents of file in terminal:

``` bash
cat input.txt
```

<u>Exercise:</u>\
Write a program **sum.cc**, that reads number pairs from the file **data.txt** and writes the sum of each pair to a new file. Please develop the solution following these steps and test your program after each step:

- Dump the file and understand its structure

- Open the file **data.txt** in C++, read the first two numbers and write them to the terminal. Close the file at the end.

- Loop over the input and output commands 234 times to read and print all number pairs

- Print the sum of the two numbers for each pair

- Open an output file **sums.txt** and write the sums to the file instead of the terminal

- Add the output file to the local repository and upload it to GitHub:

  ``` bash
  git add sums.txt
  git commit -m"exercise 2" sums.txt sum.cc
  git push
  ```
