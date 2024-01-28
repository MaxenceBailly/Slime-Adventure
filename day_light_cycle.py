import time

def day_night_cycle(cycle_duration=(24,0,0), t1=0):
    t2 = time.time()
    real_duration = 86400
    elapsed_time = t2 - t1
    target_duration = cycle_duration[0] * 3600 + cycle_duration[1] * 60 + cycle_duration[2]
    scaled_elapsed_time = (real_duration//target_duration)*elapsed_time

    return ((int(scaled_elapsed_time)//3600)%24, (int(scaled_elapsed_time)//60)%60, int(scaled_elapsed_time)%60)

if __name__ == '__main__':
    t1 = time.time()
    while True:
        print(day_night_cycle((0,0,1), t1), end='\r')
