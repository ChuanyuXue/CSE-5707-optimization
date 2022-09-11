#include <stdio.h>
#include <stdlib.h>

const int INPUT_COLUMN = 2;
const int INPUT_ROW_MAX = 1000;

int max(int a, int b)
{
    if (a >= b)
    {
        return a;
    }
    else
    {
        return b;
    }
}

int knapsack(const int W, int wt[], int val[], const int n)
{
    int K[n + 1][W + 1];
    // for (int i = 0; i < n + 1; i++)
    // {
    //     for (int w = 0; w < W + 1; w++)
    //     {
    //         K[n][w] = 0;
    //     }
    // }

    for (int i = 0; i < n + 1; i++)
    {
        for (int w = 0; w < W + 1; w++)
        {
            if (i == 0 || w == 0)
            {
                K[i][w] = 0;
            }
            else
            {
                if (wt[i - 1] <= w)
                {
                    K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);
                }
                else
                {
                    K[i][w] = K[i - 1][w];
                }
            }
        }
    }
    return K[n][W];
}

int main(int argc, char *argv[])
{
    FILE *file;

    int wt[INPUT_ROW_MAX];
    int val[INPUT_ROW_MAX];
    int weight;
    int value;
    int n;
    int capacity;
    int opt_est;

    // IO
    int row_count;
    file = fopen("/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/large_scale/knapPI_1_100_1000_1", "r");
    // file = fopen(argv[1], "r");
    row_count = 0;
    fscanf(file, "%d %d", &n, &capacity);
    while (!feof(file))
    {
        fscanf(file, "%d %d", &weight, &value);
        wt[row_count] = weight;
        val[row_count] = value;
        row_count++;
    }
    fclose(file);

    // for (int i = 0; i != 10; i++)
    // {
    //     printf("%d, ", wt[i]);
    // }

    printf("%d %d %d", capacity, n, row_count);
    opt_est = knapsack(capacity, wt, val, n);
    printf("\nOptvalue -> %d  ", opt_est);
    return 0;
}