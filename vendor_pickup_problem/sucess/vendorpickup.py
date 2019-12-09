#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np
from copy import deepcopy
from itertools import permutations
from clarkewright import *


# In[18]:


# 두 번째로 작은 값 출력 함수
def second_smallest(numbers):
    m1, m2 = 10000,10000
    for x in numbers:
        if x <= m1:
            m1, m2 = x, m1
        elif x < m2:
            m2 = x  
    return m2


# In[19]:


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


# In[20]:


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


# In[21]:


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
    return n_max,n_min# n(k) 계산 함수
def cal_nk(alp, P, n_max, n_min): #n_min이랑 n_max 위에서 받아온 전역변수로 된것같은데,, 이렇게 하면 나중에 문제 생길 수도 있음  
    #print(n_min) 
    #print(n_max)
    
    n = []  
    alpha = alp
    for k in range(len(P)):  
        n.append(n_min[k] + alp*(n_max[k]-n_min[k]))
        
    return n


# In[22]:


# n(k) 계산 함수
def cal_nk(alp, P, n_max, n_min): #n_min이랑 n_max 위에서 받아온 전역변수로 된것같은데,, 이렇게 하면 나중에 문제 생길 수도 있음  
    #print(n_min) 
    #print(n_max)
    
    n = []  
    alpha = alp
    for k in range(len(P)):  
        n.append(n_min[k] + alp*(n_max[k]-n_min[k]))
        
    return n


# In[23]:


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


# In[24]:

##2
# 가능한 모든 경로를 추출하는 함수 (방문 노드는 고정, 여러 개의 루트가 나왔을 때도 사용 가능)
def get_everycase(routes):
    everycase = []
    for i in range(len(routes)):
        a = routes[i][1:-1]
        b = list(permutations(a,len(a)))
        e, routes_cases,routes_everycase = [], [], []
        
        for j in range(len(b)):        
            e.append(list(b[j]))
            routes_cases.append([0] + e[j] + [0])
            
        if len(routes) == 1:
            routes_everycase = routes_cases
            return routes_everycase
            break
            
        if len(everycase) == 0:
            for k in range(len(routes_cases)):
                d = []
                d.append(routes_cases[k])
                everycase.append(d)
                
        elif len(routes) == 2: 
            for k in range(len(everycase)):
                for l in range(len(routes_cases)):
                    everycase[k].append(routes_cases[l])
                    d3 = deepcopy(everycase)
                    routes_everycase.append(d3[k])
                    everycase[k].pop()
        else:
            m = 2
            while(m < len(routes)):
                for k in range(len(everycase)):
                    for l in range(len(routes_cases)):
                        everycase[k].append(routes_cases[l])
                        d3 = deepcopy(everycase)
                        routes_everycase.append(d3[k])
                        everycase[k].pop()
                d4 = deepcopy(routes_everycase)
                everycase = d4 
                m += 1
                break
                
    return routes_everycase


# In[25]:

##4
#요일별 모든 exchange 경로(index값)과 half_mat_day를 받았을 때, 최적 경로와 비용 계산 
def calculate_bestcost(routes_everycase, half_mat_day):
    #route에 따른 cost 리턴하기?  
    
    #half matrix를 전체 matrix로 확장(인접하게)
    #각 노드들 간의 최단 거리 행렬 
    changed_half_mat = np.copy(half_mat_day)
    for i in range(len(changed_half_mat)):
        for j in range(len(changed_half_mat)):
            if changed_half_mat[i,j] == -1:
                changed_half_mat[i,j] = 0
    
    #print(changed_half_mat)
    
    total_mat = changed_half_mat + np.transpose(changed_half_mat) 
    #print(total_mat)
    #routes에 따라서 cost 계산
    total_cost = 0
    best_cost = 10000
    
    for route_idx, route in enumerate(routes_everycase):
        for i in range(len(route)-1):  
            total_cost += total_mat[route[i],route[i+1]]
        total_cost = round(total_cost,10)
       # print(f'{routes_everycase[route_idx]}일 때 비용 {total_cost}')
        if best_cost > total_cost :
            best_cost = total_cost
            best_route = routes_everycase[route_idx]
        total_cost = 0
  #  print(f' 최적 경로는 : {best_route}. 이 때의 비용은 : {best_cost}')     
    return best_cost, best_route


# In[10]:

##3
def to_half_mat_by_day(full_mat, day):    
    #요일별로 full matrix 잘라서 half_matrix 형태로 바꿔주기  
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


# In[27]:

##1
### function_ver 
#특정한 alpha값에 대해서 그때의 요일별 best schedule을 리턴해줌 
def calculate_total_week_cost(Mon, Tue, Wed, Thu, Fri, full_mat):
# 요일별로 CW 돌려서 반 최적의 routes 뽑아내야함 
# full matrix에서 step4에서 나온 요일별 스케줄 이용해서 자른 다음에 half_mat으로 바꿔서 넣어줘야 
# to_half_mat_by_day에서 출발노드인 0번 추가해주어야  

    schedules = [Mon, Tue, Wed, Thu, Fri] 
    names = ["Mon","Tue","Wed","Thu","Fri"]
    total_week_cost = 0
    local_optimal_schedule = []
    fake_optimal_schedule = []

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
                fake_optimal_schedule.append(routes)
                total_cost = calculate_cost(routes, half_mat_day)  
                total_week_cost += total_cost 
                break
            
    return total_week_cost, local_optimal_schedule, fake_optimal_schedule


# In[26]:

##5
def get_exchange(Mon, Tue, Wed, Thu, Fri, full_mat):
    
    cost = genuine = fake = 0
    cost, genuine, fake = calculate_total_week_cost(Mon, Tue, Wed, Thu, Fri, full_mat)
    new_day = []
    half_mat_days = []
    a = [Mon,Tue,Wed,Thu,Fri]
    c = ["Mon","Tue","Wed","Thu","Fri"]
    d = [1, 2, 3, 4, 5]
    exchange_opt_route = [1, 2, 3, 4, 5]
    exchange_opt_cost = 0
    
    for i in range(5):
        b = to_half_mat_by_day(full_mat, a[i])
        half_mat_days.append(b)
        new_day.append(0)
        new_day[i] = get_everycase(fake[i])
        #print(f'{c[i]}')
        d[i], exchange_opt_route[i] = calculate_bestcost(new_day[i],half_mat_days[i])
        exchange_opt_cost += d[i]
    print("월화수목금의 최적 경로의 Index:")
    print(exchange_opt_route)
    #print(f'그 때의 총 비용은 {exchange_opt_cost}')
    
    return exchange_opt_route, exchange_opt_cost 


# In[ ]:




