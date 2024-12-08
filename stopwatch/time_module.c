#include <Python.h>
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
void calculate_elapsed_time(long start_time_ms, long end_time_ms, int string_format, char* result) {
    long elapsed_ms = end_time_ms - start_time_ms;

    long hours = elapsed_ms / 3600000;
    elapsed_ms %= 3600000;
    long minutes = elapsed_ms / 60000;
    elapsed_ms %= 60000;
    long seconds = elapsed_ms / 1000;
    long milliseconds = elapsed_ms % 1000;

    if (string_format) {
        // Format the result as a string (e.g., "01:23:45:678")
        snprintf(result, 50, "%02ld:%02ld:%02ld:%03ld", hours, minutes, seconds, milliseconds);
    } else {
        // Format the result as individual components (e.g., "Milliseconds: 0, Seconds: 5, Minutes: 0, Hours: 0")
        snprintf(result, 100, "Milliseconds: %ld, Seconds: %ld, Minutes: %ld, Hours: %ld", milliseconds, seconds, minutes, hours);
    }
}

// Python wrapper for get_current_timestamp_ms
static PyObject* py_get_current_timestamp_ms(PyObject* self, PyObject* args) {
    return PyLong_FromLong(get_current_timestamp_ms());
}

// Python wrapper for calculate_elapsed_time
static PyObject* py_calculate_elapsed_time(PyObject* self, PyObject* args) {
    long start_time_ms, end_time_ms;
    int string_format;

    if (!PyArg_ParseTuple(args, "llI", &start_time_ms, &end_time_ms, &string_format)) {
        return NULL;
    }

    char result[100];
    calculate_elapsed_time(start_time_ms, end_time_ms, string_format, result);

    return Py_BuildValue("s", result);
}

// Method table for the module
static PyMethodDef TimeMethods[] = {
    {"get_current_timestamp_ms", py_get_current_timestamp_ms, METH_NOARGS, "Get current timestamp in milliseconds"},
    {"calculate_elapsed_time", py_calculate_elapsed_time, METH_VARARGS, "Calculate elapsed time between two timestamps"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef timemodule = {
    PyModuleDef_HEAD_INIT,
    "time_module",   // Module name
    "Time-related functions",  // Module docstring
    -1,  // Size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    TimeMethods
};

// Module initialization function
PyMODINIT_FUNC PyInit_time_module(void) {
    return PyModule_Create(&timemodule);
}
