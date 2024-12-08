import time_module
import time

# Get current timestamp in milliseconds
timestamp_ms = time_module.get_current_timestamp_ms()
print(f"Current timestamp in milliseconds: {timestamp_ms}")

# Simulate a delay (5 seconds)
time.sleep(5)

# Get end timestamp
end_timestamp_ms = time_module.get_current_timestamp_ms()

# Calculate elapsed time in string format
elapsed_time_str = time_module.calculate_elapsed_time(timestamp_ms, end_timestamp_ms, 1)
print(f"Elapsed time (string format): {elapsed_time_str}")

# Calculate elapsed time in components
elapsed_time_comp = time_module.calculate_elapsed_time(timestamp_ms, end_timestamp_ms, 0)
print(f"Elapsed time (component format): {elapsed_time_comp}")
