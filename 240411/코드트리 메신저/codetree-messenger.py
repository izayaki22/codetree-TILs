import sys
input = sys.stdin.readline
from collections import deque

def bfs(i):
    global child
    global athrz
    global state

    que = deque()
    cnt = 0
    for j in range(len(child[i])):
        if(state[child[i][j]]):
            que.append((child[i][j], 1))

    while(que):
        ch, dpth = que.popleft()
        if(dpth <= athrz[ch]):
            cnt += 1

        for j in range(len(child[ch])):
            if(state[child[ch][j]]):
                que.append((child[ch][j], dpth + 1))

    return cnt


n, q = map(int, input().split())

l = list(map(int, input().split()))
parents = l[1 : n + 1]
athrz = [0] + l[n + 1 :]
state = [True] * (n + 1)

child = [[] for _ in range(n + 1)]
for i in range(n):
    child[parents[i]].append(i + 1)

for _ in range(q - 1):
    cmd = list(map(int, input().split()))

    if(cmd[0] == 200):  # 상태 변경하기
        state[cmd[1]] = False if(state[cmd[1]]) else True
    elif(cmd[0] == 300): # 권한 변경하기
        athrz[cmd[1]] = cmd[2]
    elif(cmd[0] == 400): # 부모 변경하기
        n1, n2 = cmd[1], cmd[2]
        p1 = parents[n1 - 1]  # n1의 부모 노드
        p2 = parents[n2 - 1]  # n2의 부모 노드

        child[p1].remove(n1)
        child[p1].append(n2)

        child[p2].remove(n2)
        child[p2].append(n1)

        parents[n1 - 1] = p2
        parents[n2 - 1] = p1
    else:
        print(bfs(cmd[1])) # cmd[1]의 정보 출력하기