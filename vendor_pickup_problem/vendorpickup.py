import numpy as np
from copy import deepcopy
from clarkewright import *

######## step 1
### notebook에서 그냥 구현 
    
######## step 2

# 두 번째로 작은 값 출력 함수
def second_smallest(numbers):
    m1, m2 = 10000,10000
    for x in numbers:
        if x <= m1:
            m1, m2 = x, m1
        elif x < m2:
            m2 = x  
    return m2


# 세 번째로 작은 값 출력 함수
def third_smallest(numbers):
    m1, m2, m3 = 10000,10000, 10000 
    for x in numbers:
        if x <= m1:
            m1, m2, m3 = x, m1, m2
        elif x < m2:
            m2, m3 = x, m2
        elif x < m3:
            m3 = x
    return m3

#dt_min값 / dt_max 계산 함수_second_smallest / third_smallest 함수 사용
def cal_dtmin_dtmax(n, full_mat):
    
    
    full_mat2 = np.copy(full_mat[1:,1:])
    full_mat3 = np.copy(full_mat[1:,:])

    dt_min, dt_max, dtmin1, dtmin2, dtmin, dtmax = [],[],[],[],[],[]  
    
    for k in range(n-1):
        dtmin.append(10000)
        dtmin[k] = second_smallest(full_mat2[k]) + third_smallest(full_mat2[k])        
        dt_min.append(dtmin[k])
        
    for i in range(n-1):
        dtmax.append(0)
        dtmax[i] += full_mat3[i][0] * 2
        if dtmax[i] < dtmin[i]:
            dtmax[i] = dtmin[i]
        dt_max.append(dtmax[i])
    
    return dt_min, dt_max

#n_min, n_max 계산 함수
def cal_nmax_nmin(D, C, Cr, Cp, VVC, P, dt_min, dt_max):
    n_max,n_min = [], []
    for k in range(len(P)):  
        sum1 = 0
        sum2 = 0
        for i in P[k]:  
            sum1 += D[i-1]*C[i-1]
            sum2 += Cp[i-1]
        a = (Cr*sum1)/(2*(sum2+VVC*dt_min[k]))
        b = (Cr*sum1)/(2*(sum2+VVC*dt_max[k]))
        n_max.append(round(a**0.5,2))
        n_min.append(round(b**0.5,2))
    return n_max,n_min


############ step 3   

# n(k) 계산 함수
def cal_nk(alp, P, n_max, n_min): #n_min이랑 n_max 위에서 받아온 전역변수로 된것같은데,, 이렇게 하면 나중에 문제 생길 수도 있음  
    #print(n_min) 
    #print(n_max)
    
    n = []  
    alpha = alp
    for k in range(len(P)):  
        n.append(n_min[k] + alp*(n_max[k]-n_min[k]))
        
    return n


############ step 4  

#STEP4 n(k)값에 따른 요일 분배

def create_schedule(alp, P, n_max, n_min):
    nk = cal_nk(alp, P, n_max, n_min)    
    
    Mon, Tue, Wed, Thu, Fri = [],[],[],[],[]
    for k in range(len(nk)):
        nk[k] = round(nk[k],0)
        if nk[k] >= 5:
            Mon.append(k+1)
            Tue.append(k+1)
            Wed.append(k+1)
            Thu.append(k+1)
            Fri.append(k+1)
        elif nk[k] == 4:
            Mon.append(k+1)
            Tue.append(k+1)
            Thu.append(k+1)
            Fri.append(k+1)
        elif nk[k] == 3:
            Mon.append(k+1)
            Wed.append(k+1)
            Fri.append(k+1)
        elif nk[k] == 2:
            Tue.append(k+1)
            Thu.append(k+1)
        elif nk[k] == 1:
            Wed.append(k+1)
            
    return nk, Mon, Tue, Wed, Thu, Fri

############### step 5 

def to_half_mat_by_day(full_mat, day):    
    #요일별로 full matrix 잘라서 half_matrix 형태로 바꿔주기  
    #day는 각 요일에 방문해야 하는 vendor number을 나타낸 1차원 벡터형태 리스트 
    # ex) half_mat = np.array([[-1,10,12,15,7],[-1,-1,5,12,11],[-1,-1,-1,7,9],[-1,-1,-1,-1,10],[-1,-1,-1,-1,-1]])
    
   
    #cut by indices
    indices = deepcopy(day) 
    indices.insert(0,0)
    indices = np.array(indices)   
    #print(indices)  
    tmp_mat = np.copy(full_mat[indices]) #cut row  
    tmp_mat = np.copy(tmp_mat[:,indices]) #cut column
    
    #change to half matrix 
    half_mat = np.triu(tmp_mat)
    #print(half_mat)     
    for i in range(len(half_mat)):
        for j in range(len(half_mat)):
            if half_mat[i,j] == 0: #tmp_mat의 upper diagonal이 모두 0이 아닐 경우에만 이게 맞는 코딩임  
                half_mat[i,j] = -1
    #print(half_mat)

    
    return half_mat


### function_ver 

def calculate_total_week_cost(Mon, Tue, Wed, Thu, Fri, full_mat):   
# 요일별로 CW 돌려서 반 최적의 routes 뽑아내야함 
# full matrix에서 step4에서 나온 요일별 스케줄 이용해서 자른 다음에 half_mat으로 바꿔서 넣어줘야 
# to_half_mat_by_day에서 출발노드인 0번 추가해주어야  

    schedules = [Mon, Tue, Wed, Thu, Fri] 
    names = ["Mon","Tue","Wed","Thu","Fri"]
    total_week_cost = 0
    local_optimal_schedule = []

    for day_idx, day in enumerate(schedules):

        half_mat_day = to_half_mat_by_day(full_mat, day)  #from vendorpickup.py 
        #print("{}'s must visit vendor from zero:{}".format(names[day_idx], day))  #list not changed! (by using deepcopy)   
        _, t_mat, demand, is_constraint = initialize(len(half_mat_day), False) #from clarkewright.py    
        net_saving_mat = calculate_net_saving(half_mat_day, len(half_mat_day)) #from clarkewright.py     
        
        while(True):
            t_mat, adjacency, net_saving_mat, cells= max_net_saving(half_mat_day, t_mat, net_saving_mat, demand, is_constraint,  12345)
            routes = search_all_route(adjacency) 
            if len(cells) == 0 or len(routes) == 1:  
                routes = search_all_route(adjacency) 
                #실제 vendor number에 맞게 조정 
                tmp_day = deepcopy(day)
                tmp_day.insert(0,0) 
                real_routes = deepcopy(routes) 
                for route_idx, route in enumerate(routes):
                    for i in range(len(route)):
                        real_routes[route_idx][i] = tmp_day[route[i]]
                
                local_optimal_schedule.append(real_routes)
                total_cost = calculate_cost(routes, half_mat_day)  
                total_week_cost += total_cost 
                break
            
    return total_week_cost, local_optimal_schedule

