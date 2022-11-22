#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

const long INPUT_ROW_MAX = 1000000;

int max(int a, int b) { return (a > b) ? a : b; }

// int max(int a, int b) {
//   if (a >= b) {
//     return a;
//   } else {
//     return b;
//   }
// }

int knapsack(const int W, int wt[], int val[], const int n)
{
    int i, w;
    // Stack memory is not free
    // int K[n + 1][W + 1];

    int **K = (int **)malloc((n + 1) * sizeof(int *));
    for (i = 0; i < n + 1; i++)
    {
        K[i] = (int *)malloc((W + 1) * sizeof(int));
    }

    // for (i = 0; i < n; i++)
    // {
    //     printf("%d %d\n", wt[i], val[i]);
    // }

    // Build table K[][] in bottom up manner
    for (i = 0; i <= n; i++)
    {
        for (w = 0; w <= W; w++)
        {
            if (i == 0 || w == 0)
                K[i][w] = 0;
            else if (wt[i - 1] <= w)
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);
            else
                K[i][w] = K[i - 1][w];
        }
    }

    w = W;
    int res = K[n][W];
    int *output;
    output = (int *)malloc(n * sizeof(int));
    for (i = 0; i < n; i++)
    {
        output[i] = 0;
    }
    for (i = n; i != 0; i--)
    {
        if (res <= 0)
        {
            break;
        }
        if (res == K[i - 1][w])
        {
            continue;
        }
        else
        {
            output[i - 1] = 1;
            res = res - val[i - 1];
            w = w - wt[i - 1];
        }
    }
    for (i = 0; i < n; i++)
    {
        printf("%d ", output[i]);
    }
    printf("\n");
    return K[n][W];
}

// int knapsack(const int W, int wt[], int val[], const int n) {
//   int i;
//   int w;
//   int K[n + 1][W + 1];
//   //   for (int i = 0; i < n + 1; i++) {
//   //     for (int w = 0; w < W + 1; w++) {
//   //       K[n][w] = 0;
//   //     }
//   //   }

//   printf("%d %d\n\n\n", W, n);
//   for (i = 0; i < n + 1; i++) {
//     for (w = 0; w < W + 1; w++) {
//       if (i == 0 || w == 0) {
//         K[i][w] = 0;
//       } else if (wt[i - 1] <= w) {
//         K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);
//       } else {
//         K[i][w] = K[i - 1][w];
//       }
//     }
//   }
//   return K[n][W];
// }

int main(int argc, char *argv[])
{
    struct timeval stop, start;
    gettimeofday(&start, NULL);
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
    // file = fopen("/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/"
    //              "large_scale/knapPI_1_100_1000_1",
    //              "r");
    file = fopen("/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/"
                 "low-dimensional/f1_l-d_kp_10_269",
                 //  "low-dimensional/f2_l-d_kp_20_878",
                 "r");

    // file = fopen("/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/customized_dataset/big_big_dataset", "r");

    // file = fopen(argv[1], "r");

    row_count = 0;

    fscanf(file, "%d", &n);

    while (row_count < n)
    {
        fscanf(file, "%d %d", &weight, &value);
        wt[row_count] = value;
        val[row_count] = weight;
        row_count++;
    }

    fscanf(file, "%d", &capacity);
    fclose(file);
    opt_est = knapsack(capacity, wt, val, n);
    gettimeofday(&stop, NULL);
    printf("\nOptvalue -> %d, Time -> %ld,%06d", opt_est, (stop.tv_sec - start.tv_sec), stop.tv_usec - start.tv_usec);
    return 0;
}