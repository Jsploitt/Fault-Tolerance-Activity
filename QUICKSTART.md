# Quick Start Guide

## Test the Modified Client (Right Now!)

Before running experiments, test that everything works:

### 1. Start the Servers (3 terminals)

```powershell
# Terminal 1
python async_replica_server.py 5000 A

# Terminal 2
python async_replica_server.py 5001 B

# Terminal 3
python async_replica_server.py 5002 C
```

### 2. Run the Client (4th terminal)

```powershell
python async_client_concurrent.py
```

### 3. Expected Output

You should see:
- Client attempting connections to replicas
- Some servers crashing (they'll print crash messages and exit)
- Client failing over to other replicas
- **NEW:** Request logging like: `Request 5 served by 127.0.0.1:5001 with reply "OK 12"`
- **NEW:** Per-replica statistics at the end:

```
==================================================
PER-REPLICA STATISTICS
==================================================
Replica 127.0.0.1:5000 served 8 successful requests
Replica 127.0.0.1:5001 served 7 successful requests
Replica 127.0.0.1:5002 served 5 successful requests

Total succeeded: 20, Total failed: 0
==================================================
```

---

## If Something Goes Wrong

### Syntax Error about `tuple[str, tuple]`
**Problem:** Python version < 3.10  
**Solution:** Either:
- Use Python 3.10+, OR
- Change line 43 in `async_client_concurrent.py`:
  ```python
  # From:
  async def send_request_with_retries(message: str, req_id: int) -> tuple[str, tuple]:
  
  # To:
  from typing import Tuple
  async def send_request_with_retries(message: str, req_id: int) -> Tuple[str, tuple]:
  ```

### Port Already in Use
**Problem:** Error like "Address already in use"  
**Solution:** 
```powershell
# Find processes using ports 5000-5002
netstat -ano | findstr :5000
netstat -ano | findstr :5001
netstat -ano | findstr :5002

# Kill the process (replace PID with the actual process ID)
taskkill /PID <PID> /F
```

### Servers Keep Crashing
**Problem:** With p_crash=0.3, servers randomly crash  
**Solution:** This is expected! Just restart crashed servers:
```powershell
# If server A crashed, restart it:
python async_replica_server.py 5000 A
```

---

## Files Overview

| File | Purpose | Status |
|------|---------|--------|
| `async_replica_server.py` | Server (crashes randomly) | Original - don't modify unless running experiments |
| `async_client_concurrent.py` | Client with logging/stats | **MODIFIED** - ready to use |
| `Activity_Response.md` | Your submission document | **TO BE COMPLETED** by you |
| `EXPERIMENT_INSTRUCTIONS.md` | Step-by-step experiment guide | Reference when running Task 2 |
| `SUMMARY.md` | Complete overview | Start here for big picture |
| `QUICKSTART.md` | This file | Use to test everything works |

---

## Next Steps

1. ✅ Test the modified client (follow this guide)
2. 📸 Capture a screenshot showing failover behavior (Task 0)
3. 🧪 Run the 3 experiments following `EXPERIMENT_INSTRUCTIONS.md`
4. 📝 Fill in results in `Activity_Response.md`
5. 👥 Add team member names and IDs
6. 📤 Submit `Activity_Response.md`

---

## Quick Verification Checklist

- [ ] Python 3.10+ installed (`python --version`)
- [ ] All 3 servers start successfully
- [ ] Client connects and makes requests
- [ ] You see "Request X served by..." messages
- [ ] Per-replica statistics print at the end
- [ ] You can observe failover when servers crash

**If all checked:** You're ready to run the experiments! 🚀
