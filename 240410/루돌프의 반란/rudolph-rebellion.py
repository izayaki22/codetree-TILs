import sys
input = sys.stdin.readline
import copy

def ru_move(rux, ruy, santa_pos):
    distance = [] # (거리, 산타 -x좌표, 산타 -y좌표) 오름차순

    for pos in santa_pos:
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
    dxy = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    cur_dis = (v[0] - rux) ** 2 + (v[1] - ruy) ** 2
    case = []

    for i in range(4):
        dis = (v[0] + dxy[i][0] - rux) ** 2 + (v[1] + dxy[i][1] - ruy) ** 2
        if(cur_dis > dis):
            min_x, min_y = v[0] + dxy[i][0], v[1] + dxy[i][1]
            dx, dy =  dxy[i][0], dxy[i][1]
            case.append([dis, min_x, min_y, dx, dy])

    case = sorted(case, key = lambda x:x[0])

    for i in range(len(case)):
        d, min_x, min_y, dx, dy = case[i]
        if([min_x, min_y] not in santa_pos.values() and 0 <= min_x < n and 0 <= min_y < n):
            santa_pos[key] = [min_x, min_y]
            return True, min_x, min_y, dx, dy

    return False, 0
def crash(who, time, rux, ruy, dis_x, dis_y, power, santa_pos):

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
                interaction(nsx, nsy, k, dis_x, dis_y)
            else:
                santa_pos[k] = [nsx, nsy]
        else:
            del santa_pos[k]

    else:
        paused_santa[who] = time
        score_update(who, power)
        dis_x, dis_y = -dis_x, -dis_y
        nsx, nsy = rux + (dis_x * power), ruy + (dis_y * power)  # san_power만큼 밀려난 산타의 새 position

        if (0 <= nsx < n and 0 <= nsy < n):

            if ([nsx, nsy] in santa_pos.values()):
                interaction(nsx, nsy, who, dis_x, dis_y)
            else:
                santa_pos[who] = [nsx, nsy]
        else:
            del santa_pos[who]

def interaction(nsx, nsy, k, dis_x, dis_y):
    global santa_pos

    new_pos = {} # 산타 번호 : 새 좌표
    new_pos[k] = [nsx, nsy]
    # nsx, nsy : 겹치는 산타의 좌표. (나중에 좌표 업데이트 필요)
    # k : 날라온 산타의 번호
    # dis_x, dis_y : 산타가 날라온 방향

    for key, val in santa_pos.items():
        if([nsx, nsy] == val):
            if(0 <= nsx + dis_x < n and 0 <= nsy + dis_y < n):
                new_pos[key] = [nsx + dis_x, nsy + dis_y]

            nsx += dis_x
            nsy += dis_y
        elif(key != k):
            new_pos[key] = val

    #santa_pos를 업데이트 하는 방법
    santa_pos = copy.deepcopy(new_pos)


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
            print(score_board[num], end = ' ')
        exit()

    paused_temp = {}
    for num, ti in paused_santa.items():
        if(ti + 2 != time):
            paused_temp[num] = ti

    paused_santa = copy.deepcopy(paused_temp)

    rux, ruy, dis_x, dis_y = ru_move(rux, ruy, santa_pos.values())
    if([rux, ruy] in santa_pos.values()):
        crash("R", time, rux, ruy, dis_x, dis_y, ru_power, santa_pos)

    for key in list(sorted(santa_pos.keys()))[:]:  # 모든 산타가 움직인다.
        if (key not in paused_santa):
            bool_li = santa_move(key, santa_pos[key])
            if(bool_li[0]):
                nsx, nsy, dx, dy = bool_li[1:]
                if(nsx == rux and nsy == ruy):
                    crash(key, time, rux, ruy, dx, dy, san_power, santa_pos)

    for key in santa_pos.keys():
        score_update(key, 1)

for num in sorted(list(score_board.keys())):
    print(score_board[num], end = ' ')