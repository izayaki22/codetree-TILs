import sys
input = sys.stdin.readline
from collections import deque

l, n, q = map(int, input().split())
chess = [[-1] * (l + 2) for _ in range(l + 2)]
omg = {} # 함정의 좌표
knights = [0] * (n + 1) # 기사의 (h, w) 값
heart = [0] * (n + 1) # 기사의 체력 k 값
lived_knights = {} # 생존한 기사의 번호 : 받은 대미지
pos = [0] * (n + 1) # 기사의 위치 좌표 (r, c) 값


for i in range(l):
    li = list(map(int, input().split()))
    for j in range(l):

        if(li[j] == 1): # 함정
            omg[(i + 1, j + 1)] = 1
        if(li[j] != 2): # 빈칸
            chess[i + 1][j + 1] = 0

for i in range(1, n + 1):
    r, c, h, w, k = map(int, input().split())
    knights[i] = (h, w)
    heart[i] = k
    lived_knights[i] = 0
    pos[i] = (r, c)

    for j in range(r, r + h):
        for ci in range(c, c + w):
            chess[j][ci] = i


# 위, 오, 아, 왼
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def bfs(idx, dir):

    que = deque()
    visited = [False] * (n + 1)
    que.append(idx)
    visited[idx] = True

    while(que):
        x = que.popleft()
        r, c = pos[x]
        nr, nc = r + dx[dir], c + dy[dir]
        h, w = knights[x]

        if(nr < 1 or l < nr + h - 1 or nc < 1 or l < nc + w - 1):
            return False, 0

        for i in range(nr, nr + h):
            for j in range(nc, nc + w):
                if(chess[i][j] == -1):
                    return False, 0

        for i in range(1, n + 1):
            if(i == x):
                continue
            else:
                ix, iy = pos[i]
                ih, iw = knights[i]
                if ix > nr + h - 1 or nr > ix + ih - 1:
                    continue
                if iy > nc + w - 1 or nc > iy + iw - 1:
                    continue
                if visited[i] == False:
                    que.append(i)
                    visited[i] = True


    return True, visited

for _ in range(q):
    num, dir = map(int, input().split())
    if(num in lived_knights): # 명령을 받은 기사가 살아있음
        x, y = pos[num]
        bol, vis = bfs(num, dir)
        h, w = knights[num]

        if(bol): # 움직일 수 있다
            for i in range(1, n + 1):
                if(vis[i]):
                    ix, iy = pos[i]
                    ih, iw = knights[i]
                    pos[i] = (ix + dx[dir], iy + dy[dir])
                    if(i == num):
                        continue
                    for ri in range(ix, ix + ih):
                        for ci in range(iy, iy + iw):
                            if((ri + dx[dir], ci + dy[dir]) in omg and i in lived_knights):
                                heart[i] -= 1
                                lived_knights[i] = lived_knights[i] + 1
                                if (heart[i] <= 0):
                                    del lived_knights[i]
                                    break

ans = 0
for kni, damage in lived_knights.items():
    ans += damage


print(ans)