
import numpy as np
import sys 

# no of rows are equal to the number of columns. 
n = int(input("Enter the number of rows in a matrix")) 
mat = [[0 for x in range (n)] for y in range(n)] 
for i in range (n): 
    for j in range(n): 
     mat[i][j]=int(input()) 


    
#assign initial job list
row_job = np.arange(n) + 1 #+1 for real job number
col_job = np.arange(n) + 1 #+1 for real job number 

#substract row_min from mat 
pat = np.array(mat)  


# stack으로 assign job 하기
stack = np.zeros((n*2)) 

def stack_push_jobs(top, element): 
    if top == -1:#empty stack
        stack[top+1] = element #[rowjob,coljob]
        return top + 1
    if stack[top] != element: # 현재 top # 이미 있는 거랑 중복이 아니면 
        stack[top+1] = element  
        return top + 1
    else:  
        return top 


## 여기서부터 n번 for문 돌리면 됨 
new_n = n 
Cmax = 0
top = -1


for al_iter in range(n):
    
    
    row_min = np.amin(pat, axis = 1)
    
    for i in range(new_n):
        pat[i] = pat[i] - row_min[i] 

    #substract col_min from mat
    col_min = np.amin(pat, axis = 0)
    pat = pat - col_min  

    #calculate value of Cmax 
    for i in range(new_n):
        Cmax += row_min[i] + col_min[i] #row_min과 col_min의 모든 element값을 빼면 cmax가 나온다 
    print("Cmax: ", Cmax)
    
    #regret matrix 

    regret_mat = np.zeros((new_n,new_n))
    row_regret_min = 0
    col_regret_min = 0

    for i in range(new_n):  
        for j in range(new_n):   
            if(pat[i,j] == 0):  
                row_regret_min = 30000000
                col_regret_min = 30000000 
                for k in range(new_n): #i빼고 colum min 구하기 
                    if((k != i) & (pat[k,j] < col_regret_min)):
                        col_regret_min = pat[k,j]
                        #print(col_regret_min)
                    if((k != j) & (pat[i,k] < row_regret_min)):
                        row_regret_min = pat[i,k]
                        #print(row_regret_min)
                regret_mat[i,j] = row_regret_min + col_regret_min
                    
    #max regret의 index를 추출하기  
    idx = np.unravel_index(np.argmax(regret_mat, axis=None), regret_mat.shape)   
    

    # reduced job number
    assigned_row_job = row_job[idx[0]] 
    assigned_col_job = col_job[idx[1]] 
    print("assigned_row_job: ", assigned_row_job)
    print("assigned_col_job: ", assigned_col_job)
    #stack push
    top = stack_push_jobs(top, assigned_row_job)  
    top = stack_push_jobs(top, assigned_col_job)  
    
   
    # return value to infinity of inverse assigned job  
    idx1 = np.where(row_job == assigned_col_job) #top 
    idx2 = np.where(col_job == assigned_row_job) #top -1 
    print("idx1: ", idx1)
    print("idx2: ", idx2)  
    
    #연결되지 않는 경우 예외처리 
    tmp1 = np.array(idx1)
    tmp2 = np.array(idx2)
    print(tmp1.shape)
    print(tmp2.shape)
    if tmp1.shape == (1,0):
        idx1 = np.where(row_job == stack[top-1])
        idx2 = np.where(col_job == stack[top-2])
    #예제에서는 이 경우만 해당될듯
    if tmp2.shape == (1,0):
        idx2 = np.where(col_job == stack[top-2])
    print("idx1: ", idx1)
    print("idx2: ", idx2) 
    
    pat[idx1,idx2] = 30000000
    
    
    print(row_job)
    print(col_job)
    
    # reduce jobs   
    row_job = np.delete(row_job, idx[0]) 
    col_job = np.delete(col_job, idx[1])  
    
    # reduce matrix 
    pat = np.delete(pat, idx[0], 0)
    pat = np.delete(pat, idx[1], 1)
    pat #reduced matrix  
    print(pat)  
    new_n = new_n - 1  
    
    
    