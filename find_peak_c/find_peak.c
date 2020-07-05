#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

void local_maxima(
    float* x, int x_len,
    int* midpoints, int* left_edges, int* right_edges, int* peak_len
    ) {
    int m = 0, i = 1, i_max = x_len - 1;
    int i_ahead;

    while(i < i_max){
        if(x[i - 1] < x[i]){
            i_ahead = i + 1;

            while(i_ahead < i_max && x[i_ahead] == x[i]){
                i_ahead += 1;
            }

            if (x[i_ahead] < x[i]) {
                left_edges[m] = i;
                right_edges[m] = i_ahead - 1;
                midpoints[m] = (left_edges[m] + right_edges[m]) / 2;
                m += 1;
                i = i_ahead;
            }
        }
        i += 1;
    }
    *peak_len = m;
}

typedef struct
{
    int index;
    float priority;
} priority_sort_result_t;

int compare(const void* aa, const void* bb) {
    float 
        a = ((priority_sort_result_t*)aa)->priority, 
        b = ((priority_sort_result_t*)bb)->priority;
    if(a<b) return -1;
    else if (a>b) return 1;
    else return 0;
}


void select_by_peak_distance(
    int* peaks,
    int peaks_len,
    float* priority,
    float distance,

    bool* keep
) {
    priority_sort_result_t* priority_to_position = malloc(peaks_len * sizeof(priority_sort_result_t));
    int distance_ = (int)distance;
    for (int i = 0; i < peaks_len; i++)
    {
        priority_to_position[i].index = i;
        priority_to_position[i].priority = priority[i];
    }
    qsort(
        priority_to_position, 
        peaks_len, 
        sizeof(*priority_to_position),
        compare
    );

    // Highest priority first -> iterate in reverse order (decreasing)
    for (int i = peaks_len-1; i >= 0; i--)
    {
        // "Translate" `i` to `j` which points to current peak whose
        // neighbours are to be evaluated
        printf("[%d] %f\n", priority_to_position[i].index, priority_to_position[i].priority);
        int j = priority_to_position[i].index;
        // Skip evaluation for peak already marked as "don't keep"
        if (keep[j] == 0) continue;

        int k = j-1;
        // Flag "earlier" peaks for removal until minimal distance is exceeded
        while(k >= 0 && peaks[j] - peaks[k] < distance_) {
            keep[k] = 0;
            k -= 1;
        }

        k = j+1;
        while(k < peaks_len && peaks[k] - peaks[j] < distance_) {
            keep[k] = 0;
            k += 1;
        }
    }
    
    free(priority_to_position);
}

void peak_prominences(
    float* x, int x_len, int* peaks, int peaks_len, int wlen,
    float* prominences, int* left_bases, int* right_bases
) {
    // printf("hello\n");
    char show_warning = 0;

    for (int peak_nr = 0; peak_nr < peaks_len; peak_nr++)
    {
        int peak = peaks[peak_nr];
        int i_min = 0, i_max = x_len - 1;
        if (peak < i_min || peak > i_max)
        {
            // error handleing
        }
        
        if (2 <= wlen)
        {
            // Adjust window around the evaluated peak (within bounds);
            // if wlen is even the resulting window length is is implicitly
            // rounded to next odd integer
            // original: i_min = max(peak - wlen/2, i_min)
            //           i_max = min(peak + wlen/2, i_max)
            i_min = (peak - wlen/2 > i_min) ? peak - wlen/2 : i_min;
            i_max = (peak + wlen/2 < i_max) ? peak + wlen/2 : i_max;
        }

        // Find the left base in interval [i_min, peak]
        int i = left_bases[peak_nr] = peak;
        float left_min = x[peak];
        while (i_min <= i && x[i] <= x[peak])
        {
            if (x[i] < left_min)
            {
                left_min = x[i];
                left_bases[peak_nr] = i;
            }
            i -= 1;
        }

        // Find the right base in interval [peak, i_max]
        i = right_bases[peak_nr] = peak;
        float right_min = x[peak];
        while (i <= i_max && x[i] <= x[peak])
        {
            if (x[i] < right_min)
            {
                right_min = x[i];
                right_bases[peak_nr] = i;
            }
            i += 1;
        }

        prominences[peak_nr] = x[peak] - 
            // max(left_min, right_min)
            ((left_min > right_min) ? left_min : right_min);
        
        if (prominences[peak_nr] == 0)
        {
            show_warning = 1;
        }
    }

}

void find_peaks(
    float* x, int x_len, float distance, float prominence, int wlen,
    int* peaks, int* peaks_len_p
) {
    int peaks_size = x_len / 2 * sizeof(int);
    int
        *left_edges = malloc(peaks_size), 
        *right_edges = malloc(peaks_size);
    int peaks_len;
    local_maxima(
        x, x_len,
        peaks, left_edges, right_edges, &peaks_len
    );
    free(left_edges); free(right_edges);

    // make a peaks value array
    float* x_peaks = malloc(peaks_len * sizeof(float));
    for (int i = 0; i < peaks_len; i++)
    {
        x_peaks[i] = x[peaks[i]];
    }
    
    bool* keep = malloc(peaks_len * sizeof(bool));
    memset(keep, 1, peaks_len);
    printf("sizeof(bool) == %lu", sizeof(bool));
    select_by_peak_distance(peaks, peaks_len, x_peaks, distance, keep);
    free(x_peaks);

    int selected_peaks_len = 0;
    for (int i = 0; i < peaks_len; i++)
    {
        if (keep[i])
        {
            peaks[selected_peaks_len] = peaks[i];
            selected_peaks_len += 1;
        }
    }
    free(keep);
    peaks_len = selected_peaks_len;
    
    if (prominence != 0){
        float *prominences = malloc(peaks_len * sizeof(*x));
        int *left_bases = malloc(peaks_len * sizeof(*peaks));
        int *right_bases = malloc(peaks_len * sizeof(*peaks));
        peak_prominences(
            x, x_len, peaks, peaks_len, wlen, 
            prominences, left_bases, right_bases
        );

        int p_selected_peaks_len = 0;
        for (int i = 0; i < peaks_len; i++)
        {
            if (prominences[i] > prominence)
            {
                peaks[p_selected_peaks_len] = peaks[i];
                p_selected_peaks_len += 1;
            }
        }
        peaks_len = p_selected_peaks_len;
    }

    *peaks_len_p = peaks_len;
}