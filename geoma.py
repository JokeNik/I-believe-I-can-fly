import numpy
from numpy import ndarray
import math

EPS = 1e-9

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

def sort(a, n):
    for i in range(n):
        for j in range(n - 1):
            if a[j].x > a[j + 1].x:
                t = a[j]
                a[j] = a[j + 1]
                a[j + 1] = t
            if a[j].x == a[j + 1].x and a[j].y > a[j + 1].y:
                t = a[j]
                a[j] = a[j + 1]
                a[j + 1] = t
    return a

def cw(a, b, c):
    return a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y) < 0

def ccw(a, b, c):
    return a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y) > 0


def Convex_hull(a, n):
    a = sort(a, n)
    p1 = a[0]
    p2 = a[n - 1]
    up = []
    down = []
    su = 1
    sd = 1
    up.append(p1)
    down.append(p1)
    for i in range(1, n):
        if (i == n - 1 or cw(p1, a[i], p2)):
            while (su >= 2 and cw(up[su - 2], up[su - 1], a[i]) == 0):
                up.pop()
                su = su - 1
            up.append(a[i])
            su = su + 1
        if (i == n - 1 or ccw(p1, a[i], p2)):
            while (sd >= 2 and ccw(down[sd - 2], down[sd - 1], a[i]) == 0):
                down.pop()
                sd = sd - 1
            down.append(a[i])
            sd = sd + 1
    a.clear()
    sz = 0
    for i in range(su):
        a.append(up[i])
        sz = sz + 1
    for i in range(sd - 2, 0, -1):
        a.append(down[i])
        sz = sz + 1
    return a, sz

def dist(a, b):
    return math.sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y))

def findmax(a, n):
    id = 0
    mx = 0
    for i in range(n - 1):
        d = dist(a[i], a[i + 1])
        if d > mx:
            mx = d
            id = i

    d = dist(a[n - 1], a[0])
    if d > mx:
        return a[n - 1], a[0]
    else:
        return a[id], a[id + 1]

def makeline(p, q):
    a = p.y - q.y
    b = q.x - p.x
    c = -a * p.x - b * p.y
    return a, b, c

def det(a, b, c, d):
    return a * d - b * c

def parallel(m, n):
    return abs(det(m.a, m.b, n.a, n.b)) < EPS

def intersect(m, n):
    zn = det(m.a, m.b, n.a, n.b)
    res = Point(0, 0)
    res.x = - det (m.c, m.b, n.c, n.b) / zn
    res.y = - det (m.a, m.c, n.a, n.c) / zn
    return res

def check(ar, n, a, b, c):
    l = Line(a, b, c)
    ar.append(ar[0])
    n = n + 1
    ans = []
    sz = 0
    for i in range(n - 1):
        a1, b1, c1 = makeline(ar[i], ar[i + 1])
        l1 = Line(a1, b1, c1)
        if (parallel(l, l1) == 0):
            pt = intersect(l, l1)
            if pt.x >= min(ar[i].x, ar[i + 1].x) and pt.x <= max(ar[i].x, ar[i + 1].x):
                if pt.y > min(ar[i].y, ar[i + 1].y) and pt.y <= max(ar[i].y, ar[i + 1].y):
                    ans.append(pt)
                    sz = sz + 1
    return ans, sz

def cs(ax, ay, bx, by):
    return (ax * bx + ay * by) / (math.sqrt(ax * ax + ay * ay) * math.sqrt(bx * bx + by * by))

def makevector(p, q):
    x = q.x - p.x
    y = q.y - p.y
    return x, y

def solve(a, n, d):
    a, n = Convex_hull(a, n)
    pt1, pt2 = findmax(a, n)
    aa, b, c = makeline(pt1, pt2)

    k = math.sqrt(aa * aa + b * b) * d;

    fl = 1
    j = 0
    ans = []
    ans.append(pt1)
    ans.append(pt2)
    sa = 2
    while (fl == 1):
        j = j - 1
        ass, sz1 = check(a, n, aa, b, c + j * k)
        if sz1 == 1:
            ans.append(ass[0])
            sa = sa + 1
            continue
        if sz1 == 0:
            break
        ax, ay = makevector(ans[sa - 1], ans[sa - 2])
        bx, by = makevector(ans[sa - 1], ass[0])
        cx, cy = makevector(ans[sa - 1], ass[1])
        cos1 = cs(ax, ay, bx, by);
        cos2 = cs(ax, ay, cx, cy);
        if (cos1 > cos2):
            ans.append(ass[1])
            ans.append(ass[0])
        else:
            ans.append(ass[0])
            ans.append(ass[1])
        sa = sa + 2


    fl = 1
    j = 0
    while (fl == 1):
        j = j + 1
        ass, sz1 = check(a, n, aa, b, c + j * k)
        if sz1 == 1:
            ans.append(ass[0])
            sa = sa + 1
            continue
        if sz1 == 0:
            break
        ax, ay = makevector(ans[sa - 1], ans[sa - 2])
        bx, by = makevector(ans[sa - 1], ass[0])
        cx, cy = makevector(ans[sa - 1], ass[1])
        cos1 = cs(ax, ay, bx, by);
        cos2 = cs(ax, ay, cx, cy);
        t1 = cos1
        t2 = cos2
        if (cos1 > cos2):
            ans.append(ass[1])
            ans.append(ass[0])
        else:
            ans.append(ass[0])
            ans.append(ass[1])
        sa = sa + 2

    for i in range(sa):
        print(ans[i].x, ans[i].y, sep = ' ')




n = int(input())
d = int(input())
a = []
for i in range(n):
    x = float(input())
    y = float(input())
    t = Point(x, y)
    a.append(t)

solve(a, n, d)
