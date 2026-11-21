# Performance Profiling Dashboard

An interactive web-based project demonstrating **Performance Profiling**, with a focus on identifying **CPU and memory bottlenecks** in a Python FastAPI application.

The project demonstrates the complete performance optimization workflow:

**Measure → Identify Bottleneck → Optimize → Re-profile → Compare**

---

## 📌 Project Overview

Applications may become slow, consume excessive memory, or use computing resources inefficiently. However, knowing that an application is slow does not automatically tell developers **which part of the application is responsible**.

Performance profiling helps developers measure application behavior and identify where execution time and memory are being consumed.

Instead of optimizing based on assumptions, profiling follows a measurement-driven approach:

```text
Performance Problem
        ↓
Profile Application
        ↓
Identify Bottleneck
        ↓
Optimize Code
        ↓
Profile Again
        ↓
Compare Results
```

This project provides a practical demonstration of this process using a **FastAPI backend and an interactive web dashboard**.

---

## 🎯 Project Objectives

The main objectives of this project are to:

- Understand performance profiling
- Identify performance bottlenecks
- Demonstrate CPU profiling
- Demonstrate memory profiling
- Measure execution time
- Measure peak memory allocation
- Optimize inefficient code
- Compare original and optimized implementations
- Validate that optimization does not change the expected output
- Visualize profiling results through an interactive dashboard

---

## 🧠 What is Performance Profiling?

Performance profiling is the process of analyzing a running program to determine where system resources are being consumed.

A profiler can help answer questions such as:

- Which function is taking the most execution time?
- Which operation is consuming excessive memory?
- Where is the performance bottleneck?
- Did an optimization actually improve performance?
- Does the optimized implementation still produce the same result?

The main principle demonstrated by this project is:

> **Measure first. Optimize second.**

---

## 🚧 What is a Performance Bottleneck?

A bottleneck is a part of an application that limits its overall performance.

For example:

```text
User Request
     ↓
Authentication     → Fast
     ↓
Database Query     → Fast
     ↓
Data Processing    → SLOW  ← Bottleneck
     ↓
Response
```

Even if most components are fast, one inefficient operation can affect the performance of the complete application.

Profiling helps locate this limiting component.

---

# 🖥️ System Architecture

The project consists of an interactive frontend connected to a FastAPI backend.

```text
Web Dashboard
      ↓
JavaScript Request
      ↓
FastAPI Backend
      ↓
Application Workload
      ↓
┌──────────────────────────┐
│ CPU / Memory Profilers   │
│ cProfile / tracemalloc   │
└──────────────────────────┘
      ↓
Bottleneck Identification
      ↓
Code Optimization
      ↓
Re-profile
      ↓
Before vs After Comparison
```

The dashboard is used to trigger profiling experiments and display the results returned by the backend.

---

# ⚙️ CPU Profiling Experiment

## Problem

The CPU experiment contains an intentionally inefficient computation.

The original implementation performs a calculation multiple times when the calculated value could instead be stored and reused.

Conceptually:

```text
Original Implementation

Calculate value
      ↓
Use value for condition
      ↓
Calculate same value again
      ↓
Use result
```

This introduces unnecessary CPU computation.

---

## CPU Optimization

The optimized implementation calculates the required value once and reuses it.

```text
Optimized Implementation

Calculate value once
        ↓
Store result
      ↙     ↘
Condition   Reuse value
```

Both implementations process the same workload and produce the same result.

This allows a fair comparison between the original and optimized implementations.

---

## CPU Profiling Tools

The project uses:

- Python `cProfile`
- `time.perf_counter()`
- Repeated execution
- Average execution-time comparison

`cProfile` helps inspect where execution time is being spent, while `perf_counter()` provides high-resolution timing for performance comparison.

---

## Repeated Performance Testing

A single execution time can vary because of system activity.

Therefore, the final CPU analysis executes:

```text
Original Implementation
        ↓
      5 Runs
        ↓
Calculate Average

        VS

Optimized Implementation
        ↓
      5 Runs
        ↓
Calculate Average
```

The results are then compared.

---

## Example CPU Result

One experimental run produced:

```text
Original Average Execution Time:   0.3465 seconds
Optimized Average Execution Time:  0.3055 seconds
Execution-Time Improvement:        11.84%
Output Validation:                 SAME
```

The exact values may change depending on the machine, Python version, background processes, and current system workload.

The important observation is that both implementations are verified to produce the **same output** before their performance is compared.

---

# 💾 Memory Profiling Experiment

## Problem

The memory experiment demonstrates how the choice of data structure can affect memory consumption.

The original implementation calculates approximately **2,000,000 values** and stores all of them inside a Python list.

Conceptually:

```text
Generate 2,000,000 values
          ↓
Store complete list in memory
          ↓
Large temporary allocation
          ↓
Process the values
```

The complete intermediate list exists in memory even though the final operation only needs to process its values.

---

## Memory Optimization

The optimized implementation uses a **generator**.

Instead of creating the complete list, values are generated when they are required.

```text
Generate value
      ↓
Process value
      ↓
Generate next value
      ↓
Process value
      ↓
Continue...
```

This is known as **lazy evaluation**.

It avoids materializing the complete intermediate dataset in memory.

---

## Memory Profiling Tool

The project uses Python's:

```text
tracemalloc
```

`tracemalloc` tracks Python memory allocations while the operation is running.

Instead of only comparing memory before and after execution, the project measures the **peak traced memory allocation during execution**.

This is useful because temporary objects may already have been released by the time an operation finishes.

---

## Example Memory Result

In one experiment, the list-based implementation reached approximately:

```text
77.37 MB peak traced memory allocation
```

The generator-based implementation required only a very small additional traced allocation compared with materializing the complete list.

A displayed value such as `0.00 MB` for the optimized implementation should not be interpreted as the application using zero memory. It indicates that the additional traced allocation was extremely small when rounded to megabytes.

Results can vary depending on the environment.

---

# 📊 Interactive Performance Dashboard

The project includes a web interface called **PerformanceLab**.

The dashboard allows users to run the profiling experiments directly from the browser.

It includes:

### CPU Bottleneck Test

Runs the intentionally inefficient CPU workload and profiles its execution.

### Optimized CPU Test

Runs the improved CPU implementation for comparison.

### Memory Bottleneck Test

Executes the list-based memory-intensive operation.

### Optimized Memory Test

Uses generator-based processing to reduce temporary memory allocation.

### Full Performance Analysis

Executes repeated CPU tests and automatically displays:

- Original average execution time
- Optimized average execution time
- Execution-time improvement percentage
- Same-output validation
- Before vs optimized visualization

The results displayed on the dashboard are generated by the backend profiling experiments rather than being hard-coded.

---

# 🔄 Complete Profiling Workflow

The complete experiment follows this process:

```text
1. Run Application Workload
              ↓
2. Measure Performance
              ↓
3. Identify Bottleneck
              ↓
4. Analyze Cause
              ↓
5. Optimize Implementation
              ↓
6. Run Same Workload Again
              ↓
7. Compare Results
              ↓
8. Validate Improvement
```

This demonstrates the standard idea behind performance profiling:

> Optimization should be based on measurements rather than assumptions.

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | Backend API framework |
| Uvicorn | ASGI server |
| HTML | Dashboard structure |
| CSS | Dashboard design |
| JavaScript | Frontend-backend communication |
| cProfile | CPU profiling |
| tracemalloc | Peak Python memory allocation profiling |
| time.perf_counter | Execution-time measurement |
| psutil | Process/system information support |
| memory-profiler | Additional memory profiling support |

---

# 📁 Project Structure

```text
performance-profiling/
│
├── main.py
├── index.html
├── style.css
├── script.js
├── requirements.txt
├── README.md
├── .gitignore
│
├── presentation/
│   └── Performance_Profiling.pptx
│
├── report/
│   └── Performance_Profiling_Report.pdf
│
├── script/
│   └── Presentation_Script.pdf
│
└── screenshots/
    └── profiling-results/
```

The presentation, report, presenter script, and final screenshots can be included in the same repository as part of the complete academic submission.

---

# 🚀 How to Run the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
cd performance-profiling
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

---

## 3. Activate the Virtual Environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Start the FastAPI Server

```bash
uvicorn main:app --reload
```

The server should start at:

```text
http://127.0.0.1:8000
```

---

## 6. Open the Performance Dashboard

Open the following address in a browser:

```text
http://127.0.0.1:8000
```

---

## 7. Open FastAPI Documentation

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The profiling endpoints can also be tested directly from this interface.

---

# 🧪 Profiling Experiments

The application provides endpoints for:

```text
CPU Profiling
/profile/cpu

Optimized CPU Profiling
/profile/cpu/optimized

CPU Performance Comparison
/profile/cpu/compare

Memory Profiling
/profile/memory

Optimized Memory Profiling
/profile/memory/optimized
```

These endpoints are connected to the web dashboard.

---

# 🌍 Why Performance Profiling Matters

Performance problems can affect:

- Application response time
- User experience
- Server resource consumption
- Application scalability
- Infrastructure cost
- System reliability
- Performance under high traffic

For example, consider a backend API used by thousands of users.

If one processing function consumes most of the execution time, increasing server resources may temporarily hide the problem but does not necessarily fix the inefficient code.

Profiling helps developers identify the actual bottleneck so that optimization efforts can focus on the correct component.

---

# 💡 Key Learnings

This project demonstrates several important concepts:

### 1. Do not guess performance problems

A slow application does not automatically reveal which component is responsible.

### 2. Measure the application

Profiling provides measurable information about execution time and memory allocation.

### 3. Identify the bottleneck

Find the operation that is limiting performance.

### 4. Optimize the bottleneck

Improve the identified inefficient operation rather than randomly modifying unrelated code.

### 5. Measure again

Optimization should always be followed by another measurement.

### 6. Validate correctness

A faster implementation is not useful if it changes the expected result.

Therefore, the project verifies that the original and optimized CPU implementations produce the same output.

---

# 📈 Real-World Applications

Performance profiling is commonly useful in systems such as:

- E-commerce applications
- Search systems
- Backend APIs
- Data-processing applications
- Financial platforms
- Social-media applications
- Recommendation systems
- Cloud applications
- High-traffic web services

Profiling can help developers locate expensive operations before they affect a large number of users.

---

# 🎓 Academic Topic

## Performance Profiling

**Identifying Bottlenecks, CPU Profiling and Memory Profiling**

This project was developed as a practical demonstration of performance profiling concepts.

It combines theoretical concepts with a working FastAPI implementation to demonstrate how performance problems can be measured, identified, optimized, and validated.

---

# 📝 Final Conclusion

Performance optimization should not begin by randomly changing code.

The correct approach is:

```text
Measure
   ↓
Identify
   ↓
Optimize
   ↓
Measure Again
```

CPU profiling helps identify where execution time is being spent, while memory profiling helps identify expensive memory allocations.

By combining profiling with before-and-after measurements, developers can make optimization decisions based on actual evidence.

> **Measure first. Optimize second.**