#include <stdio.h>
int arr[10][10] = { {4, 1, 3, 5, 7}, {5, 2, 4, 6, 8,13}, {4, -1, 9, 10,100},{3, 300,400,500}} ;

int b[100],size = 0;
void merge(int a[10][10], int end, int b[],int j1)
{
    int temp[50];    //array used for merging
    int i,j,k, j2=a[end][0];
    i=0;    //beginning of the first list
    j=1;
        j1 -=1;//beginning of the second list
    k=0;
    
    while(i<=j1 && j<=j2)    //while elements in both lists
    {
        if(b[i]<a[end][j])
        {
            temp[k++]=b[i++];
            printf("temp= %d b=%d, %d\n", temp[k-1], b[i-1],i-1);
        }
        else
        {
            temp[k++]=a[end][j++];
            printf("%d temp=\n", temp[k-1]);
        }
    }
    printf("%d %d\n", j,j2);
    
    while(i<=j1)    //copy remaining elements of the first list
        temp[k++]=b[i++];
        
    while(j<=j2)    //copy remaining elements of the second list
    {
        //printf("I am here %d\n", a[end][j++]);
        temp[k++]=a[end][j++];
        printf("I am here %d\n", temp[k-1]);
    }
    j = j1 + j2;
    for(i=0;i<=j;i++)
    {        
        b[i]=temp[i];
        printf("%d ", b[i]);
    }
    size = j1+j2+1;
    printf("size: %d (%d + %d)\n", size, j1,j2);
    printf("\n");
}
int main(int argc, char const *argv[])
{
    int i;
    for(i=1;i<=arr[0][0];i++){
        b[i-1] = arr[0][i];
    }
    size += arr[0][0];
    for(i=1;i<4;i++){
        int temp[100];
        merge(arr, i, b, size);
        //size += arr[i][0] - 1;
    }
    for (i = 0; i < 16; ++i)
    {
        printf("%d\n", b[i]);
    }
}