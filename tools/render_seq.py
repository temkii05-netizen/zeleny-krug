import sys, math
sys.path.insert(0, 'src')
from mascot3d import *
# поворот 360
N = 36
for i in range(N):
    a = 2 * math.pi * i / N
    render(480, 480, Pose(yaw=a, bounce=0.06 * abs(math.sin(a * 2)))).save(f'mascot/turn/{i:03d}.png')
# прыжок + взмах (для ролика), прозрачный фон
M = 24
for i in range(M):
    ph = i / M
    b = 0.35 * max(0, math.sin(2 * math.pi * ph))
    sq = 1 - 0.08 * max(0, -math.sin(2 * math.pi * ph))
    w = 0.5 + 0.5 * math.sin(4 * math.pi * ph)
    render(560, 560, Pose(yaw=-0.3, bounce=b, squash=sq, wave=w, blink=1.0 if i in (17, 18) else 0), transparent=True).save(f'mascot/wave/{i:03d}.png')
print('done')
