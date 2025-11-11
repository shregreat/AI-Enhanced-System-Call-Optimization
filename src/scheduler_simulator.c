/* src/scheduler_simulator.c
   Simple simulator that emits system call lines to stdout (can be redirected to file).
   Compile: gcc scheduler_simulator.c -o scheduler_simulator
   Run: ./scheduler_simulator > data/sample_logs_from_c.csv
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

const char *syscalls[] = {"read","write","open","close","fork","exec","wait","exit","stat","getpid","kill","sleep"};
int num_syscalls = 12;

int main(int argc, char *argv[]) {
    int entries = 100;
    if (argc > 1) entries = atoi(argv[1]);

    srand(time(NULL));
    printf("PID,SysCall,ExecTime(ms),Timestamp\n");
    for (int i = 0; i < entries; ++i) {
        int pid = 1000 + rand() % 9000;
        const char *call = syscalls[rand() % num_syscalls];
        double ex = ((double)(rand() % 2000)) / 100.0 + 0.5; // 0.5ms to ~20.5ms
        time_t now = time(NULL);
        char tbuf[64];
        struct tm *tm_info = localtime(&now);
        strftime(tbuf, sizeof(tbuf), "%Y-%m-%d %H:%M:%S", tm_info);
        printf("%d,%s,%.3f,%s\n", pid, call, ex, tbuf);
        usleep(10000); // sleep 10ms
    }
    return 0;
}
