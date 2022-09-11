#include <stdio.h>
#include <stdlib.h>

const int INPUT_COLUMN = 2;
const int INPUT_ROW_MAX = 65536;

void swap_f(float *a, float *b)
{
  float t = *a;
  *a = *b;
  *b = t;
}

void swap_i(int *a, int *b)
{
  int t = *a;
  *a = *b;
  *b = t;
}

int partition(int index[], float arr[], int low, int high)
{
  int pivot = arr[high];
  int i = (low - 1);

  for (int j = low; j <= high - 1; j++)
  {
    if (arr[j] <= pivot)
    {
      i++;
      swap_f(&arr[i], &arr[j]);
      swap_i(&index[i], &index[j]);
    }
  }
  swap_f(&arr[i + 1], &arr[high]);
  swap_i(&index[i + 1], &index[high]);
  return (i + 1);
}

void quick_sort(int index[], float arr[], int low, int high)
{
  if (low < high)
  {
    int pi = partition(index, arr, low, high);
    quick_sort(index, arr, low, pi - 1);
    quick_sort(index, arr, pi + 1, high);
  }
}

int optimize(int validation[INPUT_ROW_MAX][INPUT_COLUMN], const int n)
{
  int result[n];
  int index[n];
  float rate[n];

  for (int i = 0; i < n; ++i)
  {
    index[i] = i;
    rate[i] = (float)validation[i][1] / (float)validation[i][0];
    printf("\nbefore %d %f", index[i], rate[i]);
  }

  quick_sort(index, rate, 0, n - 1);

  for (int i = 0; i < n; ++i)
  {
    printf("\nafter %d %f", index[i], rate[i]);
  }
}

int main(int argc, char *argv[])
{
  FILE *file;

  int validation[INPUT_ROW_MAX][INPUT_COLUMN];
  int weight;
  int value;
  int opt_est;

  // IO
  int row_count;
  file = fopen("../data/low-dimensional/f1_l-d_kp_10_269", "r");
  // file = fopen(argv[1], "r");
  row_count = 0;
  while (!feof(file))
  {
    fscanf(file, "%d %d", &weight, &value);
    validation[row_count][0] = weight;
    validation[row_count][1] = value;
    printf("%d %d", validation[row_count][0], validation[row_count][1]);
    row_count++;
  }
  fclose(file);
  opt_est = optimize(validation, row_count);
  return 0;
}