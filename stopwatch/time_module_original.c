#include <stdio.h>
#include <time.h>

// This function returns struct timespec with two fields
// First field contains the number of seconds since the Unix epoch (January 1, 1970)
// Second field contains the number of nanoseconds
// have passed within the current second
long timespec_to_ms(struct timespec ts) {
    return ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

// Function to get the current timestamp in milliseconds
long get_current_timestamp_ms() {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    return timespec_to_ms(ts);  
}

// Function to calculate the difference between two timestamps
void calculate_elapsed_time(long start_time_ms, long end_time_ms, int string_format) {
    long elapsed_ms = end_time_ms - start_time_ms;
    
    
    long hours = elapsed_ms / 3600000;
    elapsed_ms %= 3600000;
    long minutes = elapsed_ms / 60000;
    elapsed_ms %= 60000;
    long seconds = elapsed_ms / 1000;
    long milliseconds = elapsed_ms % 1000;

    if (string_format) {
        printf("%02ld:%02ld:%02ld:%03ld\n", hours, minutes, seconds, milliseconds);
    } else {
        printf("Milliseconds: %ld, Seconds: %ld, Minutes: %ld, Hours: %ld\n", milliseconds, seconds, minutes, hours);
    }
}

int main() {
    long start_time_ms = get_current_timestamp_ms(); 
    
    // Simulate a delay (for demonstration purposes)
    printf("Simulating work for 5 seconds...\n");
    sleep(5);  

    long end_time_ms = get_current_timestamp_ms();  
    
    printf("Elapsed time (string format): ");
    calculate_elapsed_time(start_time_ms, end_time_ms, 1);
    
    printf("Elapsed time (component format): ");
    calculate_elapsed_time(start_time_ms, end_time_ms, 0);

    return 0;
}
