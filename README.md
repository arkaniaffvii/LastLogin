# LastLoginWindows
LastLoginWindows is a lightweight utility that runs automatically upon user login on a Windows system and displays the date and time of the previous successful login for the current user account.

This utility is supported on Windows 10/11 Pro by default.  
On Windows 10/11 Home editions, additional configuration steps are required to enable the Windows Security Event with ID 4801, which is necessary to track the last time the user account was unlocked.

## Enable Event ID 4801 ON Windows 10/11 Home
### 1. List Available Subcategories (Optional but Recommended)

Open PowerShell as Administrator and run the following command:
```
auditpol /list /subcategory:*
```
Look for an entry similar to the following (it can change depending on your system language):
```
Other Logon/Logoff Events
```

### 2. Enable Account Lock/Unlock Auditing
Run the following command using the exact subcategory name identified in the previous step:
```
auditpol /set /subcategory:"Other Logon/Logoff Events" /success:enable
```

### 3. Verify That Auditing is Enabled
To confirm that the setting has been successfully applied, execute:
```
auditpol /get /subcategory:"Other Logon/Logoff Events"
```
You should see an output similar to:
```
Other Logon/Logoff Events    Success
```

Once these steps are completed, you can proceed with the installation of this script.

## Requirements

To run this script, the following requirements must be met:

✔️ Administrator privileges  
✔️ Python 3.x  
✔️ `pywin32` module

### Installing pywin32

Install the required module using pip:

```
pip install pywin32
```

## Schedule the Task for Automatic Execution

### 1. Open Task Scheduler

Press **Win + R**, then type:
```
taskschd.msc
```
and press **Enter**.

---

### 2. Create a Task (NOT a “Basic Task”)

In the right-hand panel, select:  
**Create Task…**

---

### 3. General Tab

Configure the task as follows:

**Name:**  
Display Last Unlock

**Security options:**

✅ Run with highest privileges  

**Configure for:**  
Windows 10 or Windows 11  

**User account:**  
Your user account (or `SYSTEM` if you want full system-level execution)

This ensures the task runs with administrator privileges.

---

### 4. Triggers Tab

Click **New…**

**Begin the task:**  
On an event  

**Settings:**  
Custom  

Click **New…** and configure the XML filter:

**Log:**  
Security  

**Event ID:**  
4801  

Click **OK → OK**

Each account unlock event will trigger the task.

---

### 5. Actions Tab

Click **New…**

**Action:**  
Start a program  

**Program/script:**  

**WARNING**: Do NOT rely on `python.exe` from the system PATH.  
Use the **full absolute path**
**Add arguments:**

"C:\Users\xxx\OneDrive\Documentos\RegistroInicioSesion.py"

**Start in (VERY IMPORTANT):**

C:\Users\xxx\OneDrive\Documentos


Click **OK**

---

### 6. Conditions Tab

Uncheck all options:

❌ Start the task only if the computer is on AC power  
❌ Stop if the computer switches to battery power  

(This prevents the task from failing to run under certain conditions.)

---

### 7. Settings Tab

Enable the following options:

✅ Allow task to be run on demand  
✅ Run task as soon as possible after a scheduled start is missed
