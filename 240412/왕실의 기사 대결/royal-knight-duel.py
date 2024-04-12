import sys
input = sys.stdin.readline
from collections import deque

l, n, q = map(int, input().split())
chess = [[-1] * (l + 2) for _ in range(l + 2)]
omg = {} # 함정의 좌표
knights = [0] * (n + 1) # 기사의 (h, w) 값
heart = [0] * (n + 1) # 기사의 체력 k 값
lived_knights = {} # 생존한 기사의 번호 : 받은 대미지


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

    for j in range(r, r + h):
        for ci in range(c, c + w):
            chess[j][ci] = i


# 위, 오, 아, 왼
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def find_knights(num): # num에 해당하는 기사의 왼쪽 위의 좌표 찾기
    global chess
    for i in range(len(chess)):
        for j in range(len(chess[0])):
            if (chess[i][j] == num):
                return i, j

def bfs(x, y, num, dir):

    que = deque()
    if(dir in [0, 2]):
        no_dir = 2 - dir
    else:
        no_dir = 4 - dir

    visited = [[0] * (len(chess[0])) for _ in range(len(chess))]

    if(dir == 0):
        x += (knights[num][0] - 1)
    elif(dir == 3):
        y += (knights[num][1] - 1)

    que.append((x, y))
    visited[x][y] = 1

    while(que):
        x, y = que.popleft()

        for i in range(4):

            if(i == no_dir):
                continue
            else:

                nx = x + dx[i]
                ny = y + dy[i]

                if(i == dir):
                    if(not (1 <= nx <= l and 1 <= ny <= l) or chess[nx][ny] == -1):
                        return False, 0

                if(1 <= nx <= l and 1 <= ny <= l and not visited[nx][ny] and 1 <= chess[nx][ny] <= n):
                    que.append((nx, ny))
                    visited[nx][ny] = 1

    return True, visited

for _ in range(q):
    num, dir = map(int, input().split())

    if(num in lived_knights): # 명령을 받은 기사가 살아있음
        x, y = find_knights(num)
        bol, vis = bfs(x, y, num, dir)
        if(bol): # 움직일 수 있다.
            temp = [[0] * (l) for _ in range(l)]

            for i in range(1, l + 1):
                for j in range(1, l + 1):

                    if(vis[i][j] == 1):
                        temp[i + dx[dir] - 1][j + dy[dir] - 1] = chess[i][j]
                    else:
                        if(chess[i][j] == -1):
                            temp[i - 1][j - 1] = -1
                        elif(1 <= chess[i][j] <= n):
                            temp[i - 1][j - 1] = chess[i][j]

            for i in range(1, l + 1):
                for j in range(1, l + 1):
                    if(1 <= temp[i - 1][j - 1] <= n):
                        kni = temp[i - 1][j - 1]
                        if(kni != num and (i, j) in omg):
                            heart[kni] -= 1
                            lived_knights[kni] = lived_knights[kni] + 1
                            if(heart[kni] <= 0):
                                del lived_knights[kni]
                                continue
                    chess[i][j] = temp[i - 1][j - 1]

ans = 0
for kni, damage in lived_knights.items():
    ans += damage


print(ans)