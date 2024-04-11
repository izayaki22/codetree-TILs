import sys
input = sys.stdin.readline
from collections import deque

def change_state(i):
    global state
    state[i] = False if(state[i]) else True

def chage_athrz(i, power):
    global athrz
    athrz[i] = power

def chage_parent(n1, n2):
    global child
    global parents

    p1 = parents[n1 - 1] # n1의 부모 노드
    p2 = parents[n2 - 1] # n2의 부모 노드

    # temp1 = copy.deepcopy(child[p1])
    # temp1.remove(n1)
    # temp1.append(n2)
    # child[p1] = temp1

    child[p1].remove(n1)
    child[p1].append(n2)

    # temp2 = copy.deepcopy(child[p2])
    # temp2.remove(n2)
    # temp2.append(n1)
    # child[p2] = temp2

    child[p2].remove(n2)
    child[p2].append(n1)

    parents[n1 - 1] = p2
    parents[n2 - 1] = p1


def bfs(i):
    #global visited
    global child
    global athrz
    global state

    que = deque()
    cnt = 0
    #visited[i] = True
    for j in range(len(child[i])):
        que.append((child[i][j], 1))
        #visited[child[i][j]] = True

    while(que):
        ch, dpth = que.popleft()
        if(state[ch]):
            if(dpth <= athrz[ch]):
                cnt += 1

            for j in range(len(child[ch])):
                #if(not visited[child[ch][j]]):
                que.append((child[ch][j], dpth + 1))
                #visited[child[ch][j]] = True

    return cnt

n, q = map(int, input().split())

l = list(map(int, input().split()))
parents = l[1 : n + 1]
athrz = [0] + l[n + 1 :]
state = [True] * (n + 1)
#visited = [False] * (n + 1)

child = [[] for _ in range(n + 1)]
for i in range(n):
    child[parents[i]].append(i + 1)

for _ in range(q - 1):
    cmd = list(map(int, input().split()))

    if(cmd[0] == 200):
        change_state(cmd[1]) # 상태 변경하기
    elif(cmd[0] == 300):
        chage_athrz(cmd[1], cmd[2]) # 권한 변경하기
    elif(cmd[0] == 400):
        chage_parent(cmd[1], cmd[2]) # 부모 변경하기
    else:
        print(bfs(cmd[1])) # cmd[1]의 정보 출력하기
        #visited = [False] * (n + 1)