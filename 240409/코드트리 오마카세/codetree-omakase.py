import sys
input = sys.stdin.readline

# 시계 방향으로 돈다. (1초에 한 칸씩)
# 1. 시간 t에 초밥 회전 -> 위치 x 앞에 있는 벨트 위에 name 부착한 회전초밥.
# 이때 같은 위치에 여러 개의 초밥 가능

# 2. 시간 t에 초밥 회전 -> name이 위치 x 의자에 앉음
# x로 오는 초밥 중에 자신의 이름이 적혀 있는 초밥 n개를 먹음 (시간 소요X)

# 3. 시간 t에 초밥 회전 -> 손님이 초밥 먹음 -> 사진 촬영 (남아있는 사람 수, 초밥 수)

class Query:

    def __init__(self, id, t, x, name, n):

        self.id = id
        self.t = t
        self.x = x
        self.name = name
        self.n = n

# 사고방식
# 1. 전부 시뮬레이션 하는건 시간 복잡도가 너무 크다. -> 시간 복잡도가 너무 큰 경우, 공간 복잡도를 이용한다. 많은 list나 자료구조에 data를 저장한다.
# 2. 어차피 모든 초밥은, 모든 사람에 의해 먹힌다. 모든 사람도 전부 먹고 결국에 떠나게 된다.
# 3. 초밥을 회전시키지 말고, 사람이 들어온 시간과 떠나는 시간을 직접 계산해서 저장한다.
# 4. 쿼리를 추가하자. (이 생각은 어케 함?) -> 초밥이 사라지는 쿼리, 사람이 나가는 쿼리 이렇게 두 개 추가
# 5. 시간 t 별로 query를 오름차순으로 정렬해서, 변수를 사용해서 따로 사람의 수와 초밥의 수를 저장한 다음 300을 만났을 때 print를 한다.
# 6. 최종 시간 복잡도는 O(NlogN)이다.


queries = []  # queries 저장
p_queries = {}  # 사람 : 초밥 query
names = set()  # 사람 이름
entry_time = {}  # 사람 : 입장 시간
position = {}  # 사람 : 위치 x
exit_time = {}  # 사람 : 퇴장 시간

l, q = map(int, input().split())

for _ in range(q):
    cmd = input().split()
    id = int(cmd[0])
    t = int(cmd[1])
    x, name, n = -1, '', -1

    if(id == 100):
        x = int(cmd[2])
        name = cmd[3]
        queries.append(Query(id, t, x, name, n))

        if(name not in p_queries):
            p_queries[name] = [Query(id, t, x, name, n)]
        else:
            p_queries[name].append(Query(id, t, x, name, n))

    elif(id == 200):
        x = int(cmd[2])
        name = cmd[3]
        n = int(cmd[4])
        queries.append(Query(id, t, x, name, n))
        names.add(name)
        position[name] = x
        entry_time[name] = t
        exit_time[name] = -1

    elif(id == 300):
        queries.append(Query(id, t, x, name, n))

for name in names: # 각 사람이 떠날 시간을 구하기

    for pq in p_queries[name]: # 해당 사람 이름에 대한 초밥 쿼리
        # 사람이 초밥 보다 먼저 온 경우
        if(entry_time[name] < pq.t):
            # entry_time[name] : 사람이 도착한 시간
            # pq.t : 초밥이 도착한 시간

            add_time = (position[name] - pq.x + l) % l
            leave_time = pq.t + add_time

        else: # 초밥이 사람보다 먼저 온 경우

            # 사람이 들어온 시간일 때의 초밥의 위치를 먼저 구해야함
            chobab_pos = (entry_time[name] - pq.t + pq.x) % l
            add_time = (position[name] - chobab_pos + l) % l # 위치 차이를 계산해서 떠나는 시간 구하기
            leave_time = entry_time[name] + add_time

        queries.append(Query(150, leave_time, pq.x, name, -1)) # 초밥이 하나 없어지는 쿼리

        exit_time[name] = max(exit_time[name], leave_time) # 사람이 떠나는 시간은 초밥이 떠나는 시간 중 제일 나중 시간

    queries.append(Query(250, exit_time[name], position[name], name, 0)) # 사람이 떠나는 쿼리

queries = sorted(queries, key = lambda x: (x.t, x.id))
chobab_cnt = people_cnt = 0

for q in queries:

    if(q.id == 100):
        chobab_cnt += 1
    elif(q.id == 150):
        chobab_cnt -= 1
    elif(q.id == 200):
        people_cnt += 1
    elif(q.id == 250):
        people_cnt -= 1
    elif(q.id == 300):
        print(people_cnt, chobab_cnt)