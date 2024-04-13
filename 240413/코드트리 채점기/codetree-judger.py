import sys
import heapq

q = int(input())
cmd, n, u = input().split()
n = int(n)

judgelist = [0] * (n + 1)  # 채점기 list
heap = []  # 채점대기큐 (p, t, domain/id)
waiting_url = {}  # {domain/id : 1}
doing = {}  # 채점진행 dict {domain : start}
finish = {}  # 채점완료 dict {domain : start + 3 * gap}
domain_heap = {} # domain별 우선순위큐
nothingjudge = [i for i in range(1, n + 1)]
heapq.heapify(nothingjudge)

ans = 1
heapq.heappush(heap, (1, 0, u))
waiting_url[u] = 1
do, id = u.split('/')
domain_heap[do] = heap

for _ in range(1, q):
    cmd_list = input().split()

    if(cmd_list[0] == '200'):
        t, p, u = cmd_list[1:]
        t, p = int(t), int(p)
        do, id = u.split('/')
        if(u not in waiting_url):
            if(do in domain_heap):
                heapq.heappush(domain_heap[do], (p, t, u))
            else:
                heap = []
                heapq.heappush(heap, (p, t, u))
                domain_heap[do] = heap
            waiting_url[u] = 1
            ans += 1

    elif (cmd_list[0] == '300'):
        t = int(cmd_list[1]) # 채점 start 시간
        temp = []
        if(len(nothingjudge) > 0):

            for do, hea in domain_heap.items():
                if(do in doing):
                    continue
                if(do in finish and t < finish[do]):
                    continue
                if(len(hea) > 0):
                    temp.append(hea)

            if(len(temp) > 0):
                temp = sorted(temp, key=lambda x: (x[0][0], x[0][1]))
                np, nt, nu = temp[0][0]
                ndom, nid = nu.split('/')

                i = heapq.heappop(nothingjudge)
                judgelist[i] = ndom
                doing[ndom] = t
                del waiting_url[nu]
                ans -= 1
                heapq.heappop(domain_heap[ndom])

    elif (cmd_list[0] == '400'):

        t, jid = map(int, cmd_list[1:])
        dom = judgelist[jid]
        if(dom in doing):
            judgelist[jid] = 0
            heapq.heappush(nothingjudge, jid)
            start = doing[dom]
            finish[dom] = start + 3 * (t - start)
            del doing[dom]

    else:
        print(ans)