import sys
input = sys.stdin.readline
import copy

def ru_move(rux, ruy):
    global santa_pos

    distance = [] # (거리, 산타 -x좌표, 산타 -y좌표) 오름차순

    for pos in santa_pos.values():
        sx, sy = pos[0], pos[1]
        dis = (rux - sx) ** 2 + (ruy - sy) ** 2
        distance.append((dis, -sx, -sy))

    distance = sorted(distance, key = lambda x: (x[0], x[1], x[2]))
    ans = distance[0]

    dis_x, dis_y = 0, 0
    if(rux > -ans[1]):
        rux -= 1
        dis_x = -1
    elif(rux < -ans[1]):
        rux += 1
        dis_x = 1

    if (ruy > -ans[2]):
        ruy -= 1
        dis_y = -1

    elif (ruy < -ans[2]):
        ruy += 1
        dis_y = 1

    return rux, ruy, dis_x, dis_y

def santa_move(key, v):
    global santa_pos

    dxy = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    cur_dis = (v[0] - rux) ** 2 + (v[1] - ruy) ** 2
    case = []

    for i in range(4):
        dis = (v[0] + dxy[i][0] - rux) ** 2 + (v[1] + dxy[i][1] - ruy) ** 2
        if(cur_dis > dis):
            min_x, min_y = v[0] + dxy[i][0], v[1] + dxy[i][1]
            dx, dy = dxy[i][0], dxy[i][1]
            case.append([dis, min_x, min_y, dx, dy])

    case = sorted(case, key = lambda x:x[0])

    for i in range(len(case)):
        d, min_x, min_y, dx, dy = case[i]
        if([min_x, min_y] not in santa_pos.values() and 0 <= min_x < n and 0 <= min_y < n):
            santa_pos[key] = [min_x, min_y]
            return True, min_x, min_y, dx, dy

    return False, 0
def crash(who, time, rux, ruy, dis_x, dis_y, power):
    global santa_pos
    # print("루돌프 위치는 ", rux, ruy, dis_x, dis_y)

    if(who == 'R'): # 루돌프가 움직여서 충돌한 경우

        for k, v in santa_pos.items():
            if(rux == v[0] and ruy == v[1]):
                # print("충돌한 산타는 ", k,"번 산타")
                # print("산타의 좌표는 ", v[0], v[1])
                paused_santa[k] = time
                break

        score_update(k, power)
        nsx, nsy = v[0] + (dis_x * power), v[1] + (dis_y * power) # ru_power만큼 밀려난 산타의 새 position
       # print("새 산타의 위치는 ", nsx, nsy)

        if(0 <= nsx < n and 0 <= nsy < n):

            if([nsx, nsy] in santa_pos.values()):
                interaction(v[0], v[1], nsx, nsy, dis_x, dis_y)
            else:
                santa_pos[k] = [nsx, nsy]
        else:
            del santa_pos[k]

    else:
        paused_santa[who] = time
        score_update(who, power)
        dis_x, dis_y = -dis_x, -dis_y
        new_sx, new_sy = rux + (dis_x * power), ruy + (dis_y * power)  # san_power만큼 밀려난 산타의 새 position

        if (0 <= new_sx < n and 0 <= new_sy < n):
            if ([new_sx, new_sy] in santa_pos.values()):
                interaction(rux, ruy, new_sx, new_sy, dis_x, dis_y)
            else:
                santa_pos[who] = [new_sx, new_sy]
        else:
            del santa_pos[who]

def interaction(psx, psy, nsx, nsy, dis_x, dis_y):
    global santa_pos

    new_pos = {} # 이전 좌표 : 새 좌표
    new_pos[(psx, psy)] = [nsx, nsy]
    new_santa_pos = {}

    previous_pos = list(santa_pos.values())

    new_x, new_y = nsx, nsy
    while([new_x, new_y] in previous_pos):
        new_pos[(new_x, new_y)] = [new_x + dis_x, new_y + dis_y]
        new_x += dis_x
        new_y += dis_y

    for key, val in santa_pos.items():

        if(tuple(val) in new_pos):
            if(0 <= val[0] < n and 0 <= val[1] < n):
                new_santa_pos[key] = new_pos[tuple(val)]
        else:
            new_santa_pos[key] = val

    #santa_pos를 업데이트 하는 방법
    santa_pos = copy.deepcopy(new_santa_pos)

def score_update(key, value):

    score_board[key] = score_board[key] + value

    return


n, m, p, ru_power, san_power = map(int, input().split())
rux, ruy = map(int, input().split())
rux -= 1
ruy -= 1 # (0, 0) 기준 좌표 맞춰주기

score_board = {} # 전체 산타 번호: 점수
santa_pos = {} # {산타 번호: 위치 좌표}
# santa_pos.values()가 살아남은 산타의 위치 좌표 list
paused_santa = {} # 기절한 산타의 번호  1 ~ P : 기절한 시간

for _ in range(p):
    pi, sr, sc = map(int, input().split())
    score_board[pi] = 0
    santa_pos[pi] = [sr - 1, sc - 1]

for time in range(m):

    if(len(santa_pos) == 0):
        for num in sorted(list(score_board.keys())):
            print(score_board[num], end=' ')
        exit()

    paused_temp = {}
    for num, ti in paused_santa.items():
        if(ti + 2 != time):
            paused_temp[num] = ti

    paused_santa = copy.deepcopy(paused_temp)

    rux, ruy, dis_x, dis_y = ru_move(rux, ruy)
    if([rux, ruy] in santa_pos.values()):
        crash("R", time, rux, ruy, dis_x, dis_y, ru_power)

    for key in list(sorted(santa_pos.keys()))[:]:  # 모든 산타가 움직인다.
        if (key not in paused_santa and key in santa_pos.keys()):
            bool_li = santa_move(key, santa_pos[key])
            if(bool_li[0]):
                nsx, nsy, dx, dy = bool_li[1:]
                if(nsx == rux and nsy == ruy):
                    crash(key, time, rux, ruy, dx, dy, san_power)

    for key in santa_pos.keys():
        score_update(key, 1)

for num in sorted(list(score_board.keys())):
    print(score_board[num], end = ' ')