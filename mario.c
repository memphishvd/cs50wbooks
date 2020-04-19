// Week 1 Problem Set: Program builds a pyramid of a user specified height
#include <cs50.h>
#include <stdio.h>

int main(void)

{
   
   
    int h;

    do 
        {
             h = get_int("Please Input The Required Pyramid Height:");
        }
    while (h<1 || h>8);
    
   for (int i=0; i<=h; i++)
        
        {   

            for (int j=h-i; j>0; j--) 
        
                 {
                        printf(" ");

                 }

            for (int j=0; j<i; j++) 
                  
                 {
                        printf("#");
                 }
            
            printf("\n");

        }
        
}

