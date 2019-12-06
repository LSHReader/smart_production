import numpy as np

def initialize(N): # N = # of nodes   
    ###### 알고리즘 맨 처음 half matrix와 T matrix를 초기화함 (example에 따라서)  
    
    #initialize node lists
    nodelist = []
    for i in range(N):  
        nodelist += [i] 
    
    #initialize half matrix by networkx
    half_mat = np.array([[-1,10,12,15,7],[-1,-1,5,12,11],[-1,-1,-1,7,9],[-1,-1,-1,-1,10],[-1,-1,-1,-1,-1]]) 
    
    
    #initialize T matrix by number of nodes  
    t_mat = np.full((N,N),0)   
    for i in range(1,len(nodelist)):  
        t_mat[0,i] = 2  #step2, assign routes between start node zero and each other node 
    

    
    #initialize demand vector
    demand = np.array([0,7,2,5,3]) #각각 node 0,1,2,3,4를 방문 시 demand 
    
    return half_mat, t_mat, demand


def calculate_net_saving(half_mat, N):
    # Half matrix를 이용해서 Net saving 행렬 계산
    # Sij = C0i + C0j - Cij 
    # 예외처리 필수 
    
    net_saving_mat = np.full((N,N),-1)  
    
    for i in range(N):
        for j in range(i,N):
            if (half_mat[0,i] != -1 & half_mat[0,j] != -1 & half_mat[i,j] != -1):  
                net_saving_mat[i,j] = half_mat[0,i] + half_mat[0,j] - half_mat[i,j]  
            else:
                continue  
    
    return net_saving_mat    

def max_net_saving(half_mat, t_mat, net_saving_mat, demand, N,  Q):
    # constraint의 경우 3가지의 conditions와, unconstraint의 경우 2가지의 conditions를 만족하면서 net saving
    # 이 가장 큰 index 반환   
    
    # step5의 3가지 조건 (or 2가지 조건) 을 만족하는 (i,j) 쌍을 모두 받아와야함  
    # 받아온 (i,j) 중에서 net saving이 가장 큰 경우에 t_mat을 변형하고 반환하기
    
    # checking three conditions 
    
    cells = []

    for i in range(N):
        for j in range(N):
            t_temp = change_t_mat(t_mat, i, j)
            if (t_mat[0,i] > 0 & t_mat[0,j] > 0) & check_routes(t_mat, i, j) & check_capacity(t_temp, demand, N, Q):
                cells += [[i,j]] # push   
                
    #cells 중에서 net saving이 가장 큰 순서쌍 찾기
    max_i = -1
    max_j = -1 
    max_net_saving = -10 
    for idx in range(len(cells)):
        i = cells[idx][0]
        j = cells[idx][1] 
        if net_saving_mat[i,j] > max_net_saving:
            max_i = i
            max_j = j
            max_net_saving = net_saving_mat[i,j]
    
    # t_mat과 net_saving_mat을 변형
    net_saving_mat[max_i,max_j] = -1
    t_mat = change_t_mat(t_mat,max_i,max_j)
            
    return t_mat 

def change_t_mat(t_mat, i, j):
    t_mat[0,i] = t_mat[0,i] -1
    t_mat[0,j] = t_mat[0,j] -1
    t_mat[i,j] = t_mat[i,j] +1   
    
    return t_mat   

def check_routes(t_mat, i, j):
    #t_mat의 모든 routes를 받아와서, 각 route에 i랑 j가 동시에 포함되어 있는지 검사 
    available_flag = True #현재 존재하는 routes상에서 존재하지 않아서, 삽입 가능하다 
    
    routes = search_all_route(t_mat) 
    
    for route_idx, route in enumerate(routes):
        if (i in route) and (j in route):
            available_flag = False  
    
    return available_flag 

def search_all_route(t_mat):
    #해당 t_mat의 모든 routes를 담은 list를 리턴해주는 함수
    #ex) return [[0,1,0],[0,2,3,0],[0,4,0]]  
    
    routes = []
    #print(initial_route)
    
    for j in range(t_mat.shape[1]): #0부터 시작하는 route에 대해서(가장 바깥 탐색) 
        if t_mat[0,j] == 2:
            routes += [[0, j, 0]]   
            #print("all routes:{}".format(routes))
        elif t_mat[0,j] == 1:   
            if check_append_available(0, j, routes): #이미 이전 경로에 포함되어 있는 노드들인지 
                tmp_route = [[0, j]] 
                tmp_route = dfs(t_mat, j, tmp_route, routes)  
                #마지막 장소에서 0으로 가는 것이 탐색되지 않는 경우 예외처리 # [0,2,3] -> [0,2,3,0]  
                last_node = tmp_route[len(tmp_route)-1][len(tmp_route[len(tmp_route)-1])-1]
                if t_mat[0,last_node] == 1:
                    tmp_route[len(tmp_route)-1].append(0)
                
                routes += tmp_route 
        else: 
            continue
    
    return routes 

def dfs(t_mat, row_idx, tmp_route, routes):

    
    if row_idx == 0: #종료조건. 다시 출발 지점으로 돌아왔다면 탐색 끝 #지금의 t_mat으로는 이 조건 실행될 일 없음.. 마지막노드랑 0이랑 연결 안되어있음 
        print(tmp_route)
        return tmp_route
    
    else:
        for j in range(t_mat.shape[1]):
            if t_mat[row_idx, j] == 1 and check_append_available(row_idx, j, routes):
                print("execute")
                tmp_route[len(tmp_route)-1].append(j)
                print(tmp_route)
                tmp_route = dfs(t_mat, j, tmp_route, routes)   
                

        return tmp_route
    
def check_append_available(i, j, routes): #이미 경로속에 존재하는 노드들인지 검사
    flag = True
    for route_idx, route in enumerate(routes):
        if (i in route) and (j in route):
            flag = False
    
    return flag    

def check_capacity(t_mat, demand, N, Q):  
    #t_mat이 변경되었을 때 capacity 조건을 만족하는가?  
    
    flag = True #capacity 다 만족하고 삽입가능하다 -> True
    #receive routes list of all routes  
    routes = search_all_route(t_mat) 
    
    #check one above routes exceed capacity or not 
    for route_idx, route in enumerate(routes):
        #print(route)
        current_capacity = 0
        for i in range(len(route)):  
            #print(route[i])
            current_capacity += demand[route[i]]
        print(current_capacity)
        if current_capacity > Q:
            #print(current_capacity)
            flag = False
            return flag 
    
    return flag 