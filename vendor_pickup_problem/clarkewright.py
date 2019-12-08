import numpy as np  



'''
initialize half_mat, t_mat, demand, is_constraint

calculate_net_saving: need only one time when initialize  
'''
def initialize(N, is_constraint): # N = # of nodes   
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
    
    #initialize constraint type
    is_const = is_constraint #True -> constraint problem, False -> unconstraint problem  
    
    return half_mat, t_mat, demand, is_const 

def calculate_net_saving(half_mat, N):
    # Half matrix를 이용해서 Net saving 행렬 계산
    # Sij = C0i + C0j - Cij 
    # 예외처리 필수 
    
    net_saving_mat = np.full((N,N),-1)   
    net_saving_mat = np.array(net_saving_mat, dtype = "float64")
    
    
    for i in range(N):
        for j in range(i,N): 
            if ((half_mat[0,i] != -1) and (half_mat[0,j] != -1) and (half_mat[i,j] != -1)):  
                net_saving_mat[i,j] = half_mat[0,i] + half_mat[0,j] - half_mat[i,j]  
            else:
                continue  
    
    return net_saving_mat    

'''
1. max_net saving is main algorithm function on step 5  

'''

def max_net_saving(half_mat, t_mat, net_saving_mat, demand, is_constraint,  Q):
    # constraint의 경우 3가지의 conditions와, unconstraint의 경우 2가지의 conditions를 만족하면서 net saving
    # 이 가장 큰 index 반환   
    
    # step5의 3가지 조건 (or 2가지 조건) 을 만족하는 (i,j) 쌍을 모두 받아와야함  
    # 받아온 (i,j) 중에서 net saving이 가장 큰 경우에 t_mat을 변형하고 반환하기
    
    # dfs 탐색을 위해 change t_mat to all adjacency matrix 
    # 아래처럼 해야 포인터 참조 안함 -> np.copy()  
    #indices = (t_mat != 0)
    #print(is_constraint)
    adjacency = make_adjacency_mat(t_mat) 
    # checking three conditions 
    cells = []

    if is_constraint == True:
        for i in range(len(t_mat)):
            for j in range(len(t_mat)):  
                t_temp = change_t_mat(t_mat, i, j)
                tmp_adjacency = make_adjacency_mat(t_temp)
                if (t_mat[0,i] > 0 and t_mat[0,j] > 0) and check_routes(adjacency, i, j) and check_capacity(tmp_adjacency, demand, Q):  
                    cells += [[i,j]] # push 
    else:
        for i in range(len(t_mat)):
            for j in range(len(t_mat)):  
                t_temp = change_t_mat(t_mat, i, j)
                tmp_adjacency = make_adjacency_mat(t_temp)
                if (t_mat[0,i] > 0 and t_mat[0,j] > 0) and check_routes(adjacency, i, j):  
                    cells += [[i,j]] # push 
    
 
    #cells 중에서 net saving이 가장 큰 순서쌍 찾기
    max_i = -1  
    max_j = -1   
    max_net_saving = -10000
    
    for idx in range(len(cells)):
        i = cells[idx][0]
        j = cells[idx][1] 
        if net_saving_mat[i,j] > max_net_saving:
            max_i = i
            max_j = j
            max_net_saving = net_saving_mat[i,j]
    
    # t_mat과 net_saving_mat을 변형
    #print("max_i: {}".format(max_i))
    #print("max_j: {}".format(max_j))
    net_saving_mat[max_i,max_j] = -1 
    t_mat = change_t_mat(t_mat,max_i,max_j)
    adjacency = make_adjacency_mat(t_mat)
    
    
    return t_mat, adjacency, net_saving_mat, cells

####################################
def make_adjacency_mat(t_mat): 
    
    adjacency = np.copy(t_mat) 
    adjacency_t = np.transpose(adjacency)
    adjacency = adjacency + adjacency_t
    
    return adjacency

def change_t_mat(t_mat, i, j): 
    #initialize 
    tmp_t_mat = np.copy(t_mat)  
    
    #change
    tmp_t_mat[0,i] -= 1
    tmp_t_mat[0,j] -= 1
    tmp_t_mat[i,j] += 1 
    #print("t_mat:{}".format(t_mat))
    #print("tmp_t_mat:{}".format(tmp_t_mat))
    
    return tmp_t_mat   
####################################



####################################
def check_routes(adjacency, i, j):
    #t_mat의 모든 routes를 받아와서, 각 route에 i랑 j가 동시에 포함되어 있는지 검사 
    available_flag = True #현재 존재하는 routes상에서 존재하지 않아서, 삽입 가능하다 
    
    routes = search_all_route(adjacency) 
    
    for route_idx, route in enumerate(routes):    
        if (i in route) and (j in route):  
            available_flag = False  
    
    return available_flag 

def search_all_route(adjacency):  
    #해당 t_mat의 모든 routes를 담은 list를 리턴해주는 함수
    #ex) return [[0,1,0],[0,2,3,0],[0,4,0]]  
    
    routes = []
    visited = np.zeros(len(adjacency)) ############새로도입 -> route구할 때만 0번 노드 방문기록 초기화 

    #일부 dfs에서 아이디어 차용  
    for j in range(1,len(adjacency)): #0빼고 탐색 
        #재탐색을 위한 초기화
        stack = [] 
        stack.append(0) 
        visited[0] = 0 #0에 대해서만 초기화 
        route = []
        
        while(stack):
            cur_node = stack.pop()  
            visited[cur_node] = 1  
            route += [cur_node]
            #print(route)  
            for col in range(1,len(adjacency)):
                if(adjacency[cur_node, col] != 0) and (visited[col] == 0): #인접했고, 아직 방문한 노드 아닐 때 
                    stack.append(col)  
                    break #이부분 매우 중요
                    
        if route != [0] and adjacency[route[len(route)-1], 0] != 0: # [0]으로 된 route는 route가 아니므로 빼주기, 마지막으로 탐색된 노드랑 출발노드인 0이랑 이어져 있는지 
            route += [0]
            routes += [route]
        
    #print(routes)
    return routes   


def check_capacity(adjacency, demand, Q):  
    #t_mat이 변경되었을 때 capacity 조건을 만족하는가?  
    
    flag = True #capacity 다 만족하고 삽입가능하다 -> True
    #receive routes list of all routes  
    routes = search_all_route(adjacency)   
    
    #check one above routes exceed capacity or not 
    for route_idx, route in enumerate(routes):
        #print(route)
        current_capacity = 0
        for i in range(len(route)):  
            #print(route[i])
            current_capacity += demand[route[i]]
        #print(current_capacity)
        if current_capacity > Q:
            #print(current_capacity) 
            flag = False
            return flag 
    
    return flag 

###############################################

def calculate_cost(routes, half_mat):
    #route에 따른 cost 리턴하기?  
    
    #half matrix를 전체 matrix로 확장(인접하게)
    #각 노드들 간의 최단 거리 행렬 
    changed_half_mat = np.copy(half_mat)
    for i in range(len(changed_half_mat)):
        for j in range(len(changed_half_mat)):
            if changed_half_mat[i,j] == -1:
                changed_half_mat[i,j] = 0
    
    #print(changed_half_mat)
    
    total_mat = changed_half_mat + np.transpose(changed_half_mat) 
    #print(total_mat)
    #routes에 따라서 cost 계산
    total_cost = 0
    
    for route_idx, route in enumerate(routes):
        for i in range(len(route)-1):  
            total_cost += total_mat[route[i],route[i+1]] 
    
    return total_cost 

###############################################