// UVa 11729 - Commando War
// Problem description: https://onlinejudge.org/external/117/11729.pdf

/*
This is a classic greedy algorithm problem. 
The idea is to first brief the soldiers for taks that take longest.
The optimal strategy is to sort the tasks in descending order of their briefing times,
and then assign the tasks to the soldiers in that order.

Why is this optimal?
If we have two jobs X and Y, say Jx > Jy (J denoting time needed to complete the task), and we assign X to a soldier before Y,
Then if we assign X first, it will take Bx + By + Jy or Bx + Jx.
If assign Y first, it will take By + Bx + Jx
Either way, assigning X first will always be better or equal to assigning Y first, because Jx > Jy.
*/

#include <cstdio>
#include <algorithm>
#include <vector>

using namespace std;

struct Job {
    int j, b;
    bool operator < (const Job& other) const {
        return j > other.j; // Sort in descending order of briefing time
    };
};

int main() {
    int n, b, j, case_num = 1;
    while (scanf("%d", &n) && n) {
        vector<Job> jobs(n);
        for (int i = 0; i < n; ++i) {
            scanf("%d %d", &jobs[i].j, &jobs[i].b);
        }
        sort(jobs.begin(), jobs.end()); // using the overloaded operator < to sort jobs in descending order of briefing time
        int total_time = 0, max_time = 0;
        for (const auto& job : jobs) {
            total_time += job.b; // accumulate briefing time
            max_time = max(max_time, total_time + job.j); // calculate the maximum time
        }
        printf("Case %d: %d\n", case_num++, max_time);
    }

    return 0;
}