#include<stdlib.h>
#include<stdio.h>
// #include<conio.h>

// int test_cfun_(int *arg)
// #FUNCTION INTEGER TEST_CFUN
#define MAX 100 

// FILE *fp;

// char a[100];
float d;

int num_devices = 3; // new

float retcod;
float b;
char cmdbuf[80];

int testv_(double *times, double *x) // new - time and x are arrays of dimension - num_devices*1
{

    float i;
    FILE *fp;
    char a[100];
    //double d;
    // double i;
    //double z = x;


    fp = fopen("test.txt", "w");
    for (int i=0; i<num_devices; i++)
    {
        fprintf(fp, "%d", int(*(times+i)));
        fprintf(fp, "\n");
    }
    for (int i=0; i<num_devices; i++)
    {
        fprintf(fp, "%d", int(*(x+i)));
        fprintf(fp, "\n");
    }
    
    fclose(fp);




    // d= system("C:\\Users\\rahul\\OneDrive\\Desktop\\FORTRAN\\dist\\random_num.exe");
    // d= system("/home/biplav/SWIFT/main.exe");
    FILE *fileStream;
    char fileText [100];

    fileStream = fopen ("result.txt", "r"); 
    fgets (fileText, 100, fileStream);
    printf("%s", fileText);
    fclose(fileStream);
}


int main()
{
float p;
// double *a=0.1, *b=.1, *c;
// printf("b");
double foo [3] = {2, 2, 1};
double foo1 [3] = { 0, 0, 0};

// p=testv_(0.1,0.1);
p=testv_(foo,foo1);
// printf("%f",p);
}

