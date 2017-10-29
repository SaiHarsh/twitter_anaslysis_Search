#include <mpi.h>
#include <stdio.h>

int a[1000]; //= {11,2,3,4,5,6,7,8,9,10,-1};
int processer_size,input_size;
int b[1000],size = 0;
void sort(int array[],int n){
    int c,d,swap,index =0;
    /*for(c = start; c<end;c++)
    {
        array[index] = a[c];
        printf("%d ", array[index]);
        index += 1;   
    }*/

    //printf(" rank %d and n= %d\n", rank, n);
    for (c = 0 ; c < ( n - 1 ); c++)
    {
        for (d = 0 ; d < n - c - 1; d++)
        {
            if (array[d] > array[d+1]) /* For decreasing order use < */
            {
                swap       = array[d];
                array[d]   = array[d+1];
                array[d+1] = swap;
            }
        }
    }
    //printf("Try to send by rank %d\n",rank);
    MPI_Send(array, n, MPI_INT, 0, 0, MPI_COMM_WORLD);
    //printf("Send completed %d,\n",rank);
    MPI_Barrier(MPI_COMM_WORLD);
}
//int partial_array[12][12], partial_array_index = 0;
void merge(int row, int column, int a[row][column], int end, int b[],int j1)
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
        }
        else
        {
            temp[k++]=a[end][j++];
        }
    }
    
    while(i<=j1)    //copy remaining elements of the first list
        temp[k++]=b[i++];
        
    while(j<=j2)    //copy remaining elements of the second list
    {
        ////printf("I am here %d\n", a[end][j++]);
        temp[k++]=a[end][j++];
        //printf("I am here %d\n", temp[k-1]);
    }
    j = j1 + j2;
    for(i=0;i<=j;i++)
    {        
        b[i]=temp[i];
        //printf("%d ", b[i]);
    }
    size = j1+j2+1;
    //printf("size: %d (%d + %d)\n", size, j1,j2);
    //printf("\n");
}

int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);

    // Get the number of processes
    MPI_Comm_size(MPI_COMM_WORLD, &processer_size);

    // Get the rank of the process
    int processer_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &processer_rank);


    
    if (processer_rank == 0) {
    	int i=1,j;
        
        scanf("%d", &input_size);
        for (i = 0; i < input_size; ++i)
        {
        	scanf("%d",&a[i]);
        	//printf("%d\n", a[i]);
        }
        
        int chunk = input_size /(processer_size-1);
        printf("chunk: %d\n", chunk);
        
        processer_size -=1;
		
		i=1;

        int number = 0;
        while(i < processer_size){
        		//MPI_Send(&number, 1, MPI_INT, i, 0, MPI_COMM_WORLD);
                
                //MPI_Send(&number, 1, MPI_INT, i, 0, MPI_COMM_WORLD);
                int temp[chunk+1], temp_index=0;
                printf("[");
                for(j=number;j<(number+chunk);j++){
                	temp[temp_index++] = a[j];
                	printf("%d ", temp[temp_index-1]);
                }
                printf("]\n");
                number += chunk;
                MPI_Send(temp, chunk, MPI_INT, i, 0, MPI_COMM_WORLD);
                
            i+=1;
        }
        int temp_index = 0,temp[input_size];
        printf("[");
        for(j=number;j<input_size;j++){
            temp[temp_index++] = a[j];
            printf("%d ", temp[temp_index-1]);
        }
        printf("] %d \n",temp_index);
        MPI_Send(temp, temp_index, MPI_INT, processer_size, 0, MPI_COMM_WORLD);
        //MPI_Send(&number, 1, MPI_INT, processer_size, 0, MPI_COMM_WORLD);
        //MPI_Send(&input_size, 1, MPI_INT, processer_size, 0, MPI_COMM_WORLD);
        MPI_Barrier(MPI_COMM_WORLD); // sync all threads
        printf("First Call\n");
        printf("\n");

        i = 0;
        //int b[input_size], b_index = 0;
        int partial_array[processer_size+1][input_size], partial_array_index = 0;
        
        // collecting data from all slaves
        while(i < processer_size){
            partial_array_index = 0;
            MPI_Status status;
            int numbers[input_size], number;
            MPI_Recv(numbers, input_size, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD,
                         &status);
             printf("[");
            
            MPI_Get_count(&status, MPI_INT, &number);
            
            partial_array[i][partial_array_index] = number;
            partial_array_index += 1;

            number -=1;

            for(j=0;j<number;j++){
                printf("%d ", numbers[j]);
                //b[b_index] = numbers[j];
                partial_array[i][partial_array_index] = numbers[j];
                partial_array_index += 1; 
            	//b_index += 1;
            }
                printf("%d", numbers[number]);
                partial_array[i][partial_array_index] = numbers[number];
                partial_array_index += 1; 
                //b[b_index] = numbers[number];
                //b_index += 1;
            printf("​] is​ ​ received​ ​ from​ ​ Slave %d\n", status.MPI_SOURCE);
            i++;
        }
        MPI_Barrier(MPI_COMM_WORLD);
        printf("second Call\n");
        printf("Job completed\n");
        printf("---------------------------------\n");
        for(i=0;i<processer_size;i++){
            for(j=0;j<=partial_array[i][0];j++){
            	printf("%d ", partial_array[i][j]);
            }
            printf("\n");
        }

        for(i=1;i<=partial_array[0][0];i++){
	        b[i-1] = partial_array[0][i];
	    }
	    size += partial_array[0][0];
	    for(i=1;i<=processer_size;i++){
	        merge(processer_size+1, input_size,partial_array, i, b, size);
	        //size += arr[i][0] - 1;
	    }
	    printf("---------------------------------------------------\n");
	    for (i = 0; i < (input_size-1); ++i)
	    {
	        printf("%d ", b[i]);
	    }
	    printf("%d\n", b[input_size-1]);
    }
    else {
    	MPI_Status status;
        int start, end;
        int i = 0;
        
        int len;
        int partial_array[100];

        MPI_Recv(partial_array, 100, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);

        MPI_Get_count(&status, MPI_INT, &len);

        printf("Len: %d\n", len);
        
        printf("Process %d received number [", processer_rank);
        for (i = 0; i < len; ++i)
        {
        	printf("%d ", partial_array[i]);
        }
        printf("] from process 0 \n");
        MPI_Barrier(MPI_COMM_WORLD);
        sort(partial_array, len);
    }
    // Finalize the MPI environment.
    MPI_Finalize();
}