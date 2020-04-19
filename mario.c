// Week 1 Problem Set: Program builds a pyramid of a user specified height
#include <cs50.h>
#include <stdio.h>

int main(void)

{
   
   
    int h;
// A loop to ensure the user inputs a positive integer between 1 and 8
    do 
        {
             h = get_int("Please Input The Required Pyramid Height:");
        }
    while (h<1 || h>8);
// First For Loop for rows    
   for (int i=1; i<=h; i++)
        
        {   
// Nested Loop-1 for printing empty spaces
            for (int j=h-i; j>0; j--) 
        
                 {
                        printf(" ");

                 }
// Nested Loop-2 for printing #
            for (int j=0; j<i; j++) 
                  
                 {
                        printf("#");
                 }
            
            printf("\n");

        }
        
}

