// This is the problem UVa 11292, the dragon of Loowater. Detailed description: https://pages.cs.wisc.edu/~dieter/ICPC/13-14/problems/ps3.pdf

/*
The core idea is that we don't want to hire high cost knights to slay small heads, 
and we want to hire the cheapest knight that can slay a head. 
So we sort both the heads and the knights, 
and then we try to match the smallest head with the smallest knight that can slay it. 
If we can't find a knight for a head, we return "Loowater is doomed!". 
Otherwise, we keep track of the total cost of hiring knights and return that.
*/

#include <cstdio>
#include <algorithm>

using namespace std;

const int MAXN = 20000;
int heads[MAXN], knights[MAXN];

int main() {
    int n, m; // n is num head, m is num knight
    while (scanf("%d %d", &n, &m) == 2 && n && m) {
        for (int i = 0; i < n; ++i) {
            scanf("%d", &heads[i]);
        }
        for (int i = 0; i < m; ++i) {
            scanf("%d", &knights[i]);
        }

        sort(heads, heads + n);
        sort(knights, knights + m);

        int total_cost = 0;
        int knight_index = 0;
        bool doomed = false;

        for (int head_index = 0; head_index < n; ++head_index) {
            while (knight_index < m && knights[knight_index] < heads[head_index]) {
                knight_index++; // find the cheapest knight that can slay the head
            }
            if (knight_index == m) {
                doomed = true; // no knights left
                break;
            }
            total_cost += knights[knight_index];
            knight_index++;
        }

        if (doomed) {
            printf("Loowater is doomed!\n");
        } else {
            printf("%d\n", total_cost);
        }
    }
    
}