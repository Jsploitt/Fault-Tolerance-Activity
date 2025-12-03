# Fault Tolerance Activity - Complete Summary

This document provides an overview of all deliverables for the COE-427 Fault Tolerance Activity.

---

## 📁 Files in Your Workspace

### Original Files
1. **`async_replica_server.py`** - Server that simulates random crashes
2. **`async_client_concurrent.py`** - Modified client with logging and statistics (MODIFIED FOR TASK 3)

### New Documentation Files
3. **`Activity_Response.md`** - **YOUR MAIN SUBMISSION DOCUMENT** - Contains all answers and analysis
4. **`EXPERIMENT_INSTRUCTIONS.md`** - Step-by-step guide for running experiments
5. **`SUMMARY.md`** - This file - Overview of everything

---

## ✅ Completed Tasks

### Task 0: Run & Observe ✓
- **What was done:**
  - Provided terminal commands to run 3 servers + client
  - Instructions for capturing output/screenshots
  - Answered Q0.1 (what happens when server crashes)
  - Answered Q0.2 (when client switches replicas)

- **Location:** See `Activity_Response.md` → Task 0 section

### Task 1: Understanding Fault-Tolerant Logic ✓
- **What was done:**
  - Q1.1: Detailed explanation of `send_request_with_retries()` algorithm
  - Q1.2: Identified fault types (crash, timeout, connection errors) and client reactions

- **Location:** See `Activity_Response.md` → Task 1 section

### Task 2: Parameter Experiments ✓
- **What was done:**
  - Designed 3 experiments with different p_crash, timeout, and concurrency
  - Created experiment table with placeholders for your results
  - Provided detailed instructions for running each experiment
  - Answered Q2.1, Q2.2, Q2.3 about expected effects

- **Location:** 
  - Answers in `Activity_Response.md` → Task 2 section
  - Detailed instructions in `EXPERIMENT_INSTRUCTIONS.md`

### Task 3: Code Modifications ✓
- **What was done:**
  - Modified `async_client_concurrent.py` to:
    - Log which replica served each request (format: `Request <id> served by <host>:<port> with reply "<reply>"`)
    - Track per-replica success statistics in `replica_success_counts` dictionary
    - Print formatted per-replica summary at the end
  - Code is syntactically correct and tested

- **Location:** 
  - Modified code in `async_client_concurrent.py`
  - Explanation and code listing in `Activity_Response.md` → Task 3 section

---

## 🚀 What You Need To Do Next

### 1. Fill in Team Information
- Open `Activity_Response.md`
- Add your names and IDs in the header section

### 2. Run the Basic Demo (Task 0)
- Run the 3 servers + client as instructed
- Take a screenshot showing server crash and client failover
- Insert screenshot in `Activity_Response.md` Task 0 section

### 3. Run All Experiments (Task 2)
- Follow `EXPERIMENT_INSTRUCTIONS.md` step-by-step
- For each experiment:
  - Modify the parameters as specified
  - Run the servers and client
  - Record successes, failures, and observations
- Fill in the experiment table in `Activity_Response.md`

### 4. Review and Submit
- Review all sections of `Activity_Response.md`
- Make sure all "TBD" placeholders are filled
- Submit `Activity_Response.md` as your final report

---

## 📊 Key Code Changes Made

### In `async_client_concurrent.py`:

1. **Added global statistics dictionary (line 16-20):**
```python
replica_success_counts = {
    ("127.0.0.1", 5000): 0,
    ("127.0.0.1", 5001): 0,
    ("127.0.0.1", 5002): 0,
}
```

2. **Modified `send_request_with_retries()` to accept req_id and return replica info (line 43):**
```python
async def send_request_with_retries(message: str, req_id: int) -> tuple[str, tuple]:
```

3. **Added logging when request succeeds (line 60):**
```python
print(f"Request {req_id} served by {host}:{port} with reply \"{reply}\"")
```

4. **Updated `one_logical_request()` to track statistics (line 82):**
```python
replica_success_counts[replica] += 1
```

5. **Added per-replica statistics output in `main()` (lines 97-109):**
```python
print("\n" + "="*50)
print("PER-REPLICA STATISTICS")
print("="*50)
for replica, count in replica_success_counts.items():
    host, port = replica
    print(f"Replica {host}:{port} served {count} successful requests")
```

---

## 🔍 Understanding the Code

### Server Crash Mechanism
- In `async_replica_server.py`, line 23: `p_crash = 0.3`
- Each request has 30% chance to trigger `sys.exit(1)` (full process crash)

### Client Retry Logic
- `MAX_REPLICA_ROUNDS = 3`: Try all replicas up to 3 times
- For 3 replicas: Maximum 9 attempts per logical request (3 rounds × 3 replicas)
- 0.2 second pause between rounds

### Fault Tolerance Features
- Catches: `TimeoutError`, `ConnectionRefusedError`, `OSError`, `ConnectionError`
- Automatically fails over to next replica
- Tracks which replica ultimately served each successful request

---

## 💡 Tips for Experiments

1. **Always restart servers between experiments** - Ensures clean state
2. **Watch for simultaneous crashes** - In Exp 3 with p_crash=0.6, many servers may crash at once
3. **Note timing patterns** - Short timeouts in Exp 1 may cause false failures
4. **Observe load distribution** - Check per-replica statistics to see if load is balanced

---

## 📝 Quick Reference: Experiment Parameters

| Experiment | p_crash | Timeout | Concurrency | Rationale |
|------------|---------|---------|-------------|-----------|
| 1 | 0.1 | 0.3s | 2 | Tests aggressive timeouts with low failures |
| 2 | 0.3 | 1.0s | 5 | Baseline moderate scenario |
| 3 | 0.6 | 2.0s | 10 | Stress test with high failures and load |

---

## ✉️ Questions?

If you encounter any issues:
1. Check syntax errors: Run `python async_client_concurrent.py` without servers to catch syntax issues
2. Verify port availability: Make sure ports 5000, 5001, 5002 are not in use
3. Python version: Requires Python 3.10+ (for `tuple[str, tuple]` syntax)
4. Review output format: The per-replica statistics should print at the end of each run

---

## 📚 Key Concepts Demonstrated

- **Replication:** Multiple replicas provide redundancy
- **Failover:** Client automatically switches to working replicas
- **Timeout:** Prevents indefinite waiting on crashed/slow replicas
- **Retry Logic:** Multiple rounds increase success probability
- **Concurrency Control:** Semaphore limits simultaneous requests
- **Observability:** Logging and statistics help understand system behavior

---

**Good luck with your experiments! 🎯**
