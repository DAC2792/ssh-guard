# Path to the login attempt file
LOG_FILE = "sample_logs/ssh_sample.log"

# Dictionary to collect failed attempts into
failures = {}

# Open log file, read, strip whitespace and newlines out.
with open(LOG_FILE) as file:
    for line in file:
        line = line.strip()
        # Use the below string to find failed log in attempts
        if "Failed password for" in line:
            # Count backwards to find the IP: the username can be faked by an attacker, but the end of the line can't
            words = line.split()
            ip = words[-4]
            # Assign 1 to each new IP found with a failed login. Add 1 each time it reappears
            failures[ip] = failures.get(ip, 0) + 1

# Print results of each IP and how many failed log in attempts
for ip, count in failures.items():
    print(f"{ip} -> {count} failed logins")