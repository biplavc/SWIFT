#include<stdlib.h>
#include<stdio.h>
#include<conio.h>

// int test_cfun_(int *arg)
// #FUNCTION INTEGER TEST_CFUN
#define MAX 100 

FILE *fp;

// char a[100];
float d;

float retcod;
float b;
char cmdbuf[80];

int testv_(double *time,int *x)
{

float i;
FILE *fp;
char a[100];
//double d;
// double i;
//double z = x;


fp = fopen("test.txt", "w");
fprintf(fp, "%d",*x);
fclose(fp);




d= system("C:\\Users\\rahul\\OneDrive\\Desktop\\FORTRAN\\dist\\random_num.exe");
fp = fopen("result.txt", "r");
fscanf(fp, "%s", a);

sscanf(a, "%f", &i);
fclose(fp);
//printf("%f",i);


return (i);
}


//int main()
//{
//float p;
// double *a=0.1, *b=.1, *c;
// printf("b");
//p=testv_(0.1,0.1);
//printf("%f",p);
//}

