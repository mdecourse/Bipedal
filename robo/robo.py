import inspect
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


def three_linked_chain(state, t):
    q1 = state[0]
    q1d = state[1]
    q2 = state[2]
    q2d = state[3]
    q3 = state[4]
    q3d = state[5]

    H = np.zeros((3,3))
    H[0,0] = ms*a1**2 + mt*(ls+a2)**2 + (mh+ms+mt)*l**2
    H[0,1] = -(mt*b2+ms*lt) * l * cos(q2-q1)
    H[0,2] = -ms*b1*l * cos(q3-q1)
    H[1,0] = H[0,1]
    H[1,1] = mt*b2**2 + ms*lt**2
    H[1,2] = ms*lt*b1 * cos(q3-q2)
    H[2,0] = H[0,2]
    H[2,1] = H[1,2]
    H[2,2] = ms*b1**2

    B = np.zeros((3,3))
    h122 = -(mt*b2+ms*lt) * l * sin(q1-q2)
    h133 = -ms*b1*l * sin(q1-q3)
    h211 = -h122
    h233 = ms*lt*b1 * sin(q3-q2)
    h311 = -h133
    h322 = -h233
    B[0,0] = 0
    B[0,1] = h122 * q2d
    B[0,2] = h133 * q3d
    B[1,0] = h211 * q1d
    B[1,1] = 0
    B[1,2] = h233 * q3d
    B[2,0] = h311 * q1d
    B[2,1] = h322 * q2d
    B[2,2] = 0

    G = np.zeros(3)
    G[0] = -(ms*a1 + mt*(ls+a2) + (mh+ms+mt)*l) * g*sin(q1)
    G[1] = (mt*b2 + ms*lt) * g*sin(q2)
    G[2] = ms*b1*g * sin(q3)

    qd = [q1d,q2d,q3d]
    rhs = -np.dot(B,qd) - G
    try:
        sol = np.linalg.solve(H,rhs)
    except:
        print(H)
    xd = np.zeros_like(state)
    xd[0] = q1d
    xd[1] = sol[0]
    xd[2] = q2d
    xd[3] = sol[1]
    xd[4] = q3d
    xd[5] = sol[2]

    return xd



def two_linked_chain(state, t):
    q1 = state[0]
    q1d = state[1]
    q2 = state[2]
    q2d = state[3]

    H = np.zeros((2,2))
    H[0,0] = ms*a1**2 + mt*(ls+a2)**2 + (mh+ms+mt)*l**2
    H[0,1] = -(mt*b2 + ms*(lt+b1))*l *cos(q2-q1)
    H[1,0] = H[0,1]
    H[1,1] = mt*b2**2 + ms*(lt+b1)**2

    h = -(mt*b2 + ms*(lt+b1))*l * sin(q1-q2)
    B = np.zeros((2,2))
    B[0,0] = 0
    B[0,1] = h*q2d
    B[1,0] = 0
    B[1,1] = -h*q1d

    G = np.zeros(2)
    G[0] = -(ms*a1 + mt*(ls+a2) + (mh+mt+ms)*l) *g*sin(q1)
    G[1] = (mt*b2 + ms*(lt+b1)) * g*sin(q2)

    qd = [q1d,q2d]
    rhs = -np.dot(B,qd) - G
    sol = np.linalg.solve(H,rhs)

    xd = np.zeros_like(state)
    xd[0] = q1d
    xd[1] = sol[0]
    xd[2] = q2d
    xd[3] = sol[1]
    xd[4] = q2d
    xd[5] = sol[1]

    return xd


def knee_strike(state):
    q1 = state[0]
    q2 = state[2]
    q3 = state[4]

    alpha = cos(q1-q2)
    beta = cos(q1-q3)
    gamma = cos(q2-q3)

    Q_r = np.zeros((2,3))
    Q_r[0,0] = -(ms*lt+mt*b2)*l*cos(alpha) - ms*b1*l*cos(beta) + (mt+ms+mh)*l**2 + ms*a1**2 + mt*(ls+a2)**2
    Q_r[0,1] = -(ms*lt+mt*b2)*l*cos(alpha) + ms*b1*lt*cos(gamma) + mt*b2**2 + ms*lt**2
    Q_r[0,2] = -ms*b1*l*cos(beta) + ms*b1*lt*cos(gamma) + ms*b1**2
    Q_r[1,0] = -(ms*lt+mt*b2)*l*cos(alpha) - ms*b1*l*cos(beta)
    Q_r[1,1] = ms*b1*lt*cos(gamma) + ms*lt**2 + mt*b2**2
    Q_r[1,2] = ms*b1*lt*cos(gamma) + ms*b1**2

    Q_l = np.zeros((2,2))
    Q_l[1,1] = ms*(lt+b1)**2 + mt*b2**2
    Q_l[1,0] = -(ms*(b1+lt) + mt*b2) * l*cos(alpha)
    Q_l[0,1] = Q_l[1,0] + ms*(lt+b1)**2 + mt*b2**2
    Q_l[0,0] = Q_l[1,0] + mt*(ls+a2)**2 + (mh+mt+ms)*l**2 + ms*a1**2

    q_r = [state[1],state[3],state[5]]
    rhs = np.dot(Q_r,q_r)
    sol = np.linalg.solve(Q_l,rhs)

    xd = np.zeros_like(state)
    xd[0] = state[0]
    xd[1] = sol[0]
    xd[2] = state[2]
    xd[3] = sol[1]
    xd[4] = state[4]
    xd[5] = sol[1]  # q3d = q2d, thigh and shank binded

    return xd

def heel_strike(state):
    q1 = state[0]
    q2 = state[2]

    alpha = cos(q1-q2)

    Q_r = np.zeros((2,2))
    Q_r[1,1] = 0
    Q_r[1,0] = -ms*a1*(lt+b1) + mt*b2*(ls+a2)
    Q_r[0,1] = Q_r[1,0]
    Q_r[0,0] = Q_r[0,1] + (mh*l + 2*mt*(a2+ls) + ms*a1) * l*cos(alpha)

    Q_l = np.zeros((2,2))
    Q_l[1,1] = ms*(lt+b1)**2 + mt*b2**2
    Q_l[1,0] = -(ms*(b1+lt) + mt*b2) * l*cos(alpha)
    Q_l[0,1] = Q_l[1,0] + ms*(b1+lt)**2 + mt*b2**2
    Q_l[0,0] = Q_l[1,0] + (ms+mt+mh)*l**2 + ms*a1**2 + mt*(a2+ls)**2

    q_r = [state[1],state[3]]
    rhs = np.dot(Q_r,q_r)
    sol = np.linalg.solve(Q_l,rhs)

    xd = np.zeros_like(state)
    xd[0] = state[0]
    xd[2] = state[2]
    xd[4] = state[2]
    xd[1] = sol[0]
    xd[3] = sol[1]
    xd[5] = sol[1]

    return xd


def step_cycle(state,pos_sf,_time):
    print('start state: ', state)

    ttcosd = []
    cnt = 0
    num_time = 2
    dt = _time / num_time
    chain_num=3 # starts with three-chain state
    success = 1
    while True:
        try:
            # print('cnt: ',cnt)
            t = np.arange(0.0, _time, dt)
            if cnt==0:
                try:
                    tmp = integrate.odeint(three_linked_chain, state, t)
                    state = np.insert(tmp[1:len(tmp)+1],[0],state,axis=0)
                except:
                    print(state)
                    print(lineno())
                    sys.exit("wrong in this step!")
                # print('three linked chain, time: %s <<<' % (cnt*_time))
                # print(np.degrees([state[-1,0],state[-1,2],state[-1,4]]))
                cnt += 1
                continue
            # knee strike
            if  ((state[-num_time:,2])>(state[-num_time:,0])).any()\
            and (chain_num==3) and (np.min(np.abs(state[-num_time:,2]-state[-num_time:,4]))<np.radians(1)):
                tmp = knee_strike(state[-1])
                state = np.insert(state, [len(state)], tmp, axis=0)
                chain_num = 2
                print('===============================================knee strike, time: %s' % (cnt*_time))
                print(state[-1])
                continue
            # heel strike
            if (chain_num==2) and (dist<0.005): # in degree
                tmp = heel_strike(state[-1])
                state = np.insert(state, [len(state)], tmp, axis=0)
                chain_num = 3
                print('===============================================heel strike, time: %s' % (cnt*_time))
                print(state[-1])
                print('end state: ',state[-1,:])
                break
            # three linked chain
            if (chain_num==3):
                try:
                    tmp = integrate.odeint(three_linked_chain, state[-1], t)
                    state = np.insert(tmp[1:len(tmp)+1],[0],state,axis=0)
                    # print('three linked chain, time: %s <<<' % (cnt*_time))
                    # print(state[-1])
                    chain_num = 3
                    cnt += 1
                except:
                    print(state)
                    print(lineno())
                    sys.exit("wrong in this step!")
            # two linked chain
            if (chain_num==2):
                try:
                    tmp = integrate.odeint(two_linked_chain, state[-1], t)
                    state = np.insert(tmp[1:len(tmp)+1],[0],state,axis=0)
                    # print('two linked chain, time: %s <<<' % (cnt*_time))
                    # print(state[-1])
                    chain_num = 2
                    cnt += 1
                except:
                    print(state)
                    print(lineno())
                    sys.exit("wrong in this step!")
        except:
            print("this is not a good step!")
            success = 0
            break

        q1 = tmp[:,0]
        q2 = tmp[:,2]
        q3 = tmp[:,4]
        x_h_tmp = -l*sin(q1)
        y_h_tmp = l*cos(q1)
        x_nsk_tmp = x_h_tmp + lt*sin(q2)
        y_nsk_tmp = y_h_tmp - lt*cos(q2)
        x_nsf_tmp = x_nsk_tmp + ls*sin(q3)
        y_nsf_tmp = y_nsk_tmp - ls*cos(q3)

        dist = 1000
        for i in range(len(x_nsf_tmp)):
            v1 = [x_nsf_tmp[i], y_nsf_tmp[i]]
            v2 = [sin((_gamma)), cos((_gamma))]
            ab = np.dot(v1, v2)
            dist = min(dist,ab)
        # print('dist: ',dist)
        # print('chain_num: ',chain_num)

        if dist <-0.1 or cnt > 6 / _time:  # usually it takes less than three seconds for a step
            print("this is not a good step!")
            success = 0
            break

    q1 = state[:,0]
    q2 = state[:,2]
    q3 = state[:,4]
    x_h = pos_sf[0] - l*sin(q1)
    y_h = pos_sf[1] + l*cos(q1)
    x_nsk = x_h + lt*sin(q2)
    y_nsk = y_h - lt*cos(q2)
    x_nsf = x_nsk + ls*sin(q3)
    y_nsf = y_nsk - ls*cos(q3)

    return x_h,y_h,x_nsk,y_nsk,x_nsf,y_nsf,state, success

def init():
    for line in lines:
        line.set_data([],[])
    time_text.set_text('')
    return tuple(lines) + (time_text,)


import sys
def animate(i):
    try:
        x_bipedal = [x_sf[i], x_sk[i], x_h[i], x_nsk[i], x_nsf[i]]
        y_bipedal = [y_sf[i], y_sk[i], y_h[i], y_nsk[i], y_nsf[i]]
        # k=0
        # x_bipedal = [x_sf[i], x_sk[i], x_h[k], x_nsk[k], x_nsf[k]]
        # y_bipedal = [y_sf[i], y_sk[i], y_h[k], y_nsk[k], y_nsf[k]]
    except:
        sys.exit("wrong in animation!")
    x_slop = [x_slop_up,x_slop_low,-2]
    y_slop = [y_slop_up,y_slop_low,y_slop_low]

    xlist = [x_bipedal, x_slop]
    ylist = [y_bipedal, y_slop]

    for lnum,line in enumerate(lines):
        line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately.

    time_text.set_text('time = %.3fs' % (i*dt))

    return tuple(lines) + (time_text,)


def show_walking():

    # following code are for animation

    # slop
    global x_slop_low,x_slop_up,y_slop_low,y_slop_up
    x_slop_low = 2 * cos((_gamma))
    x_slop_up = -x_slop_low
    y_slop_low = -2 * sin((_gamma))
    y_slop_up = -y_slop_low

    print('start animation...')

    fig = plt.figure()
    ax1 = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
    ax1.grid(True)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    global lines, time_text
    lines = []
    lobj = ax1.plot([], [], 'o-', lw=2, color="black")[0]
    lines.append(lobj)
    lobj = ax1.plot([], [], lw=2, color="red")[0]
    lines.append(lobj)

    time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)

    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(x_h)),
                                  interval=1000 * dt, blit=True, init_func=init)
    plt.show()
    # ani.save('PDW.mp4', fps=15)



def animate_orbit(i):
    try:
        orbit_q1 = orbit[0:i,0]
        orbit_q1d = orbit[0:i,1]
        orbit_q2 = orbit[0:i,2]
        orbit_q2d = orbit[0:i,3]
        orbit_q3 = orbit[0:i,4]
        orbit_q3d = orbit[0:i,5]

        xlist = [orbit_q1,orbit_q2,orbit_q3]
        ylist = [orbit_q1d,orbit_q2d,orbit_q3d]

        for lnum,line in enumerate(lines):
            line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately.

        time_text.set_text('time = %.3fs' % (i*dt))
    except:
        sys.exit("wrong in animating orbit!")

    return tuple(lines) + (time_text,)

def show_orbit():
    fig = plt.figure()
    ymin = min( [min(orbit[:,1]),min(orbit[:,3]),min(orbit[:,5])] )
    ymax = max( [max(orbit[:,1]),max(orbit[:,3]),max(orbit[:,5])] )
    xmin = min( [min(orbit[:,0]),min(orbit[:,2]),min(orbit[:,4])] )
    xmax = max( [max(orbit[:,0]),max(orbit[:,2]),max(orbit[:,4])] )
    ax1 = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
    ax1.grid(True)
    plt.xlabel('angle')
    plt.ylabel('angular velocity')

    global lines, time_text
    lines = []
    lobj = ax1.plot([], [], lw=2, color="black")[0]
    lines.append(lobj)
    lobj = ax1.plot([], [], lw=2, color="red")[0]
    lines.append(lobj)
    lobj = ax1.plot([], [], lw=2, color="blue")[0]
    lines.append(lobj)

    time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)

    ani = animation.FuncAnimation(fig, animate_orbit, np.arange(1, len(orbit)),
                                  interval=10000 * dt, blit=True, init_func=init)
    plt.show()


def robo(show_ani):
    # Passive Dynamic Walking for bipedal robot
    # % reset


    # parameters of leg structure
    paras = np.loadtxt('parameters.txt', delimiter='  ')
    try:
        last = paras[-1,:]
    except:
        last = paras
    q1 = last[0]
    q2 = last[1]
    q3 = last[2]
    c_mh = 0.47
    c_mt = 0.47
    c_ms = 0.06
    c_a1 = last[3]
    c_b1 = last[4]
    c_a2 = last[5]
    c_b2 = last[6]

    global mh,mt,ms,a1,b1,a2,b2,lt,ls,l
    M = 1# total weight
    L = 1 # total lenth
    mh = M * c_mh   #mass of hip
    mt = M * c_mt  # mass of thigh
    ms = M * c_ms # mass of shank
    a1 = L * c_a1
    b1 = L * c_b1
    a2 = L * c_a2
    b2 = L * c_b2
    lt = a2 + b2  # length of thigh
    ls = a1 + b1  # length of shank
    l = lt + ls

    global g,dt
    g = 9.8  # acceleration due to gravity, in m/s^2
    dt = 0.001 # time step of simulation
    step_idx = 1
    step_tt = 1
    if show_ani:
        step_tt = 10

    # slop of terran
    global _gamma
    # _gamma = np.radians(9)
    _gamma = 0.0504


    # state = [q1, q1d, q2, q2d, q3, q3d]
    # state = [0.1877, -1.1014, -0.2884, -0.0399, -0.2884, -0.0399]
    state = [q1, -1.1014, q2, -0.0399, q3, -0.0399]
    pos_sf = [0,0]

    # f = open('out.txt', 'w')
    # output = np.degrees(state).tolist()
    # f.write(str(output))
    # f.write('\n')

    global x_sf,y_sf,x_h,y_h,x_nsk,y_nsk,x_nsf,y_nsf
    global x_sk, y_sk

    # start walking....
    x_h, y_h, x_nsk, y_nsk, x_nsf, y_nsf,state, success = step_cycle(state, pos_sf, dt)
    step_time = len(x_h)
    x_sf = np.zeros_like(x_h)
    y_sf = np.zeros_like(x_h)


    if success==0:
        output = [[10000, -10000]]
        np.savetxt('out.txt',output, delimiter='  ')
        if show_ani:
            x_sk = x_h * (c_a1 + c_b1) + x_sf * (c_a2 + c_b2)
            y_sk = y_h * (c_a1 + c_b1) + y_sf * (c_a2 + c_b2)
            s = (c_a1 + c_b1) + (c_a2 + c_b2)
            x_sk /= s
            y_sk /= s
            show_walking()
        return

    # update initial condition
    q1 = (state[-1, 2] + state[-1, 4]) / 2
    q1d = (state[-1, 3] + state[-1, 5]) / 2
    q2 = state[-1, 0]
    q2d = state[-1, 1]
    q3 = state[-1, 0]
    q3d = state[-1, 1]
    state[-1] = [q1, state[0,1], q2, state[0,3], q3, state[0,5]]   ##############################ATTENTION HERE!
    ini_state = state[-1]
    # update location
    pos_sf = [x_nsf[-1], y_nsf[-1]]
    # ini_state_deg = [(kk)*180/np.pi for kk in ini_state]
    diff = ini_state - state[0] # difference in starting state of two step cycle
    stability = np.linalg.norm(diff) **2 * 1000
    v1 = [cos(_gamma),-sin(_gamma)]
    v2 = [x_nsf[-1],y_nsf[-1]]
    disp = np.dot(v1,v2)
    if disp<0:
        speed = 1000 * disp
    else:
        speed = disp
    output = [[stability, speed]]
    np.savetxt('out.txt',output, delimiter='  ')
    # f.write(str(output))
    # f.write('\n')

    # more steps...
    while step_idx<step_tt:
        # start another step
        x_h_new, y_h_new, x_nsk_new, y_nsk_new, x_nsf_new, y_nsf_new, state_new, success = step_cycle(ini_state, pos_sf, dt)
        x_sf_new = np.ones_like(x_h_new) * pos_sf[0]
        y_sf_new = np.ones_like(x_h_new) * pos_sf[1]
        # add trajectory of new step
        x_sf = np.insert(x_sf,[len(x_sf)],x_sf_new,axis=0)
        y_sf = np.insert(y_sf,[len(y_sf)],y_sf_new,axis=0)
        x_h = np.insert(x_h,[len(x_h)],x_h_new,axis=0)
        y_h = np.insert(y_h,[len(y_h)],y_h_new,axis=0)
        x_nsk = np.insert(x_nsk,[len(x_nsk)],x_nsk_new,axis=0)
        y_nsk = np.insert(y_nsk,[len(y_nsk)],y_nsk_new,axis=0)
        x_nsf = np.insert(x_nsf,[len(x_nsf)],x_nsf_new,axis=0)
        y_nsf = np.insert(y_nsf,[len(y_nsf)],y_nsf_new,axis=0)
        y_nsf = np.insert(y_nsf,[len(y_nsf)],y_nsf_new,axis=0)
        state = np.insert(state,[len(state)],state_new,axis=0)
        # update initial condition
        q1 = (state[-1, 2] + state[-1, 4]) / 2
        q1d = (state[-1, 3] + state[-1, 5]) / 2
        q2 = state[-1, 0]
        q2d = state[-1, 1]
        q3 = state[-1, 0]
        q3d = state[-1, 1]
        state[-1] = [q1, state[0, 1], q2, state[0, 3], q3, state[0, 5]]  ##############################ATTENTION HERE!
        ini_state = state[-1]
        # update location
        pos_sf = [x_nsf[-1],y_nsf[-1]]

        step_idx += 1
    # f.close()

    if show_ani:
        # plot hybrid trajectory in state space
        pq1 = []
        pq1d = []
        pq2 = []
        pq2d = []
        pq3 = []
        pq3d = []
        global orbit, orbit_q1, orbit_q2, orbit_q3, orbit_q1d, orbit_q2d, orbit_q3d
        orbit_q1 = []
        orbit_q2 = []
        orbit_q3 = []
        orbit_q1d = []
        orbit_q2d = []
        orbit_q3d = []
        orbit = state
        show_orbit()
        for f in orbit:
            pq1 += [f[0]]
            pq1d += [f[1]]
            pq2 += [f[2]]
            pq2d += [f[3]]
            pq3 += [f[4]]
            pq3d += [f[5]]
        plt.plot(pq1, pq1d)
        plt.plot(pq2, pq2d)
        plt.plot(pq3, pq3d)
        plt.show()
        # animation
        x_sk = x_h * (c_a1 + c_b1) + x_sf * (c_a2 + c_b2)
        y_sk = y_h * (c_a1 + c_b1) + y_sf * (c_a2 + c_b2)
        s =  (c_a1 + c_b1) +  (c_a2 + c_b2)
        x_sk /= s
        y_sk /= s
        show_walking()


from numpy import sin, cos
import numpy as np
import scipy.integrate as integrate
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

robo(1)

