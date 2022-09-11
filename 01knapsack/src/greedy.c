#include "greedy.h"
#include <stdio.h>

void swap_f(float *a, float *b) {
  float t = *a;
  *a = *b;
  *b = t;
}

void swap_i(int *a, int *b) {
  int t = *a;
  *a = *b;
  *b = t;
}

int partition(int index[], float arr[], int low, int high) {
  int pivot = arr[high];
  int i = (low - 1);

  for (int j = low; j <= high - 1; j++) {
    if (arr[j] < pivot) {
      i++;
      swap_f(&arr[i], &arr[j]);
      swap_i(&index[i], &index[j]);
    }
  }
  swap_f(&arr[i + 1], &arr[high]);
  swap_i(&index[i + 1], &index[high]);
  return (i + 1);
}

void quick_sort(int index[], float arr[], int low, int high) {
  if (low < high) {
    int pi = partition(index, arr, low, high);
    quick_sort(index, arr, low, pi - 1);
    quick_sort(index, arr, pi + 1, high);
  }
}

int optimize(int **validation, const int n) {
  int result[n];
  int index[n];
  float rate[n];

  for (int i = 0; i < n; i++) {
    rate[i] = validation[i][1] / validation[i][0];
    printf("before %f", rate[i]);
  }

  quick_sort(index, rate, 0, n);
  for (int i = 0; i < n; i++) {
    printf("after %f", rate[i]);
  }
}