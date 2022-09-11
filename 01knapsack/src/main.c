#include <stdio.h>
#include <stdlib.h>

const int INPUT_COLUMN = 2;
const int INPUT_ROW_MAX = 65536;

int main(int argc, char *argv[]){
    FILE *file;

    int validation[INPUT_COLUMN][INPUT_ROW_MAX];
    int weight;
    int value;

    // IO
    int row_count;
    // file = fopen("../data/low-dimensional/f1_l-d_kp_10_269", "r");
    file = fopen(argv[1], "r");
    row_count = 0;
    while (!feof (file))
    {  
        fscanf (file, "%d %d", &weight, &value);    
        validation[row_count][0] = weight;
        validation[row_count][1] = value;
        // printf("%d %d", validation[row_count][0],validation[row_count][1]);
    }
    fclose (file);        



}