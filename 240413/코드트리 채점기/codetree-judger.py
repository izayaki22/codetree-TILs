import sys
input = sys.stdin.readline
import heapq

q = int(input())
cmd, n, u = input().split()
n = int(n)
judgelist = [0] * (n + 1)  # 채점기 list
heap = []  # 채점대기큐 (p, t, domain/id)
waiting_url = {}  # {domain/id : 1}
doing = {}  # 채점진행 dict {domain : start}
finish = {}  # 채점완료 dict {domain : start + 3 * gap}
heapq.heappush(heap, (1, 0, u))
waiting_url[u] = 1

for _ in range(1, q):

    cmd_list = input().split()

    if(cmd_list[0] == '200'):
        t, p, u = cmd_list[1:]
        t, p = int(t), int(p)
        if(u not in waiting_url):
            heapq.heappush(heap, (p, t, u))
            waiting_url[u] = 1

    elif (cmd_list[0] == '300'):
    
        t = int(cmd_list[1]) # 채점 start 시간
        total = len(heap)

        for _ in range(total):
            if(len(heap) == 0):
                break

            np, nt, nu = heapq.heappop(heap)
            ndom, nid = nu.split('/')

            if(ndom not in doing):

                if(ndom in finish):
                    if(t >= finish[ndom]):
                        # 조건 만족
                        for i in range(1, n + 1):
                            if(judgelist[i] == 0):
                                judgelist[i] = ndom
                                doing[ndom] = t
                                del waiting_url[nu]
                                break
                        break
                    else:
                        heapq.heappush(heap, (np, nt, nu))
                else:
                    for i in range(1, n + 1):
                        if (judgelist[i] == 0):
                            judgelist[i] = ndom
                            doing[ndom] = t
                            del waiting_url[nu]
                            break
                    break

            else:
                heapq.heappush(heap,(np, nt, nu))

    elif (cmd_list[0] == '400'):

        t, jid = map(int, cmd_list[1:])
        dom = judgelist[jid]
        judgelist[jid] = 0

        start = doing[dom]
        finish[dom] = start + 3 * (t - start)
        del doing[dom]

    else:
        print(len(heap))