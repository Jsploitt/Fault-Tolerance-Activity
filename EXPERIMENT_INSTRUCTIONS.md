# Experiment Execution Instructions

This document provides step-by-step instructions for running the three experiments for Task 2.

---

## Experiment 1: Low Crash Probability with Short Timeout

**Parameters:**
- `p_crash = 0.1`
- `REQUEST_TIMEOUT = 0.3` seconds
- `MAX_CONCURRENT = 2`
- `TOTAL_REQUESTS = 50`

### Steps:

1. **Modify `async_replica_server.py`**
   - Open the file
   - Find line 23: `p_crash = 0.3`
   - Change it to: `p_crash = 0.1`
   - Save the file

2. **Modify `async_client_concurrent.py`**
   - Open the file
   - Change line 10: `REQUEST_TIMEOUT = 1.0` to `REQUEST_TIMEOUT = 0.3`
   - Change line 12: `TOTAL_REQUESTS = 20` to `TOTAL_REQUESTS = 50`
   - Change line 13: `MAX_CONCURRENT = 5` to `MAX_CONCURRENT = 2`
   - Save the file

3. **Run the experiment**
   - Open 4 terminal windows
   - Terminal 1: `python async_replica_server.py 5000 A`
   - Terminal 2: `python async_replica_server.py 5001 B`
   - Terminal 3: `python async_replica_server.py 5002 C`
   - Terminal 4: `python async_client_concurrent.py`

4. **Record results**
   - Note the "Total succeeded" and "Total failed" from the client output
   - Record per-replica statistics
   - Write observations about timeout behavior and failover patterns

5. **Restart crashed servers as needed**
   - If servers crash during the run, restart them with the same command

---

## Experiment 2: Moderate Crash Probability with Balanced Settings

**Parameters:**
- `p_crash = 0.3`
- `REQUEST_TIMEOUT = 1.0` seconds
- `MAX_CONCURRENT = 5`
- `TOTAL_REQUESTS = 50`

### Steps:

1. **Modify `async_replica_server.py`**
   - Change line 23: `p_crash = 0.1` to `p_crash = 0.3`
   - Save the file

2. **Modify `async_client_concurrent.py`**
   - Change line 10: `REQUEST_TIMEOUT = 0.3` to `REQUEST_TIMEOUT = 1.0`
   - Verify line 12: `TOTAL_REQUESTS = 50` (should already be set)
   - Change line 13: `MAX_CONCURRENT = 2` to `MAX_CONCURRENT = 5`
   - Save the file

3. **Run the experiment**
   - Follow the same terminal setup as Experiment 1
   - Restart all servers fresh to ensure clean state

4. **Record results**
   - Note successes, failures, and per-replica statistics
   - Observe how moderate crash rate affects system behavior

---

## Experiment 3: High Crash Probability with Long Timeout and High Concurrency

**Parameters:**
- `p_crash = 0.6`
- `REQUEST_TIMEOUT = 2.0` seconds
- `MAX_CONCURRENT = 10`
- `TOTAL_REQUESTS = 50`

### Steps:

1. **Modify `async_replica_server.py`**
   - Change line 23: `p_crash = 0.3` to `p_crash = 0.6`
   - Save the file

2. **Modify `async_client_concurrent.py`**
   - Change line 10: `REQUEST_TIMEOUT = 1.0` to `REQUEST_TIMEOUT = 2.0`
   - Verify line 12: `TOTAL_REQUESTS = 50` (should already be set)
   - Change line 13: `MAX_CONCURRENT = 5` to `MAX_CONCURRENT = 10`
   - Save the file

3. **Run the experiment**
   - Follow the same terminal setup as previous experiments
   - Restart all servers fresh

4. **Record results**
   - Note successes, failures, and per-replica statistics
   - Observe how high crash rate and concurrency interact
   - Note if many servers crash simultaneously and how the system recovers

---

## Tips

- **Between experiments:** Restart all servers to ensure clean state
- **If many servers crash:** You may need to manually restart them during long-running experiments
- **Capture output:** Consider redirecting client output to a file for detailed analysis:
  ```powershell
  python async_client_concurrent.py > experiment1_output.txt
  ```
- **Take screenshots:** Capture interesting failover patterns or the per-replica statistics output

---

## Expected Observations

- **Experiment 1:** May see false timeouts even with low crash rate due to aggressive 0.3s timeout
- **Experiment 2:** Baseline behavior with balanced parameters
- **Experiment 3:** Frequent crashes, more failover attempts, but long timeout may help recovery

---

## Data Collection Template

After each experiment, fill in this table:

| Metric | Experiment 1 | Experiment 2 | Experiment 3 |
|--------|--------------|--------------|--------------|
| Total Requests | 50 | 50 | 50 |
| Succeeded | ___ | ___ | ___ |
| Failed | ___ | ___ | ___ |
| Success Rate (%) | ___ | ___ | ___ |
| Replica A Requests | ___ | ___ | ___ |
| Replica B Requests | ___ | ___ | ___ |
| Replica C Requests | ___ | ___ | ___ |
| Approximate Time | ___ s | ___ s | ___ s |
