# 🛡️ ssh-guard

A small Python tool that watches a Linux machine for failed SSH login attempts, alerts when one IP address keeps failing, and can lock that IP out using the firewall.

Think of it as a security guard for the front door: it watches who keeps getting the password wrong, raises the alarm, and (if allowed) stops them from trying again.

> ⚠️ **Learning project.** Built to learn Linux, Python and defensive security. Only run it on machines you own. It is a mini version of the ideas behind real tools like `fail2ban`, not a replacement for them.

---

## 🎯 Goals

**What the tool should do**
1. Read SSH login logs on a Linux machine
2. Spot failed login attempts and which IP they came from
3. Count failures per IP within a time window
4. Alert when an IP crosses the threshold
5. Optionally block that IP with the firewall, then unblock it after a set time

**What I want to learn from building it**
- 🐧 Linux: services (`systemctl`), SSH, logs (`journalctl`, `/var/log/auth.log`), permissions, `sudo`, firewall (`ufw` / `iptables`)
- 🐍 Python: reading files and command output, regular expressions, dictionaries and counting, time handling, config files, running system commands safely
- 🛡️ Security: how brute-force attacks look in logs, detection vs prevention, false positives, not locking yourself out
- 🧰 Workflow: Git/GitHub, clear commits, a README people can follow

---

## 🔁 How it works

```
SSH login attempts
        │
        ▼
Linux writes them to the log (journalctl / auth.log)
        │
        ▼
ssh-guard reads new log lines
        │
        ▼
Finds "Failed password ... from <IP>" lines
        │
        ▼
Counts failures per IP in the last X minutes
        │
        ▼
Over threshold? ──no──► keep watching
        │
       yes
        ▼
Is the IP on the safe list? ──yes──► alert only, never block
        │
        no
        ▼
🚨 Alert  ➜  🔒 Block IP (if enabled)  ➜  ⏱️ Unblock after ban time
```

---

## ⚙️ Settings (planned `config` file)

| Setting | Example | What it means |
|---|---|---|
| `threshold` | `5` | Failures allowed before action |
| `window_minutes` | `10` | Only count failures within this time window |
| `ban_minutes` | `30` | How long a blocked IP stays blocked |
| `safe_list` | `["127.0.0.1"]` | IPs that are never blocked |
| `dry_run` | `true` | Log what *would* be blocked without blocking anything |
| `alerts_enabled` | `false` | Send email/notification alerts |

**Why a time window?** Without it, someone who mistypes their password once a week would eventually get banned. "5 failures in 10 minutes" looks like an attack; "5 failures in a month" doesn't.

**Why dry run is on by default?** So nothing gets blocked until I've proved detection works. 🙂

---

## 🪜 Build stages

### Stage 0: Set up the lab 🏠
- [ ] Create this GitHub repo and clone it locally
- [ ] Install and start the SSH server in WSL (`openssh-server`)
- [ ] Log in successfully over SSH
- [ ] Deliberately fail some logins and find them in the logs by hand (`journalctl` / `grep`)
- [ ] Write down in `notes/` what a failed-login log line looks like

### Stage 1: Detect 🔍
- [ ] Python script reads the log lines
- [ ] Pull out the IP address from each failed attempt (regex)
- [ ] Count failures per IP and print a summary

### Stage 2: Watch and alert 🚨
- [ ] Keep running and read new lines as they arrive
- [ ] Only count failures inside the time window
- [ ] Print a clear alert when an IP crosses the threshold
- [ ] Load settings from the config file
- [ ] Bonus: send email alerts, reusing ideas from the weather bot

### Stage 3: Lock out 🔒
- [ ] Safe list check before any block
- [ ] Dry-run mode that only logs "would block X"
- [ ] Block an IP with the firewall
- [ ] Unblock automatically after `ban_minutes`
- [ ] Test from a different IP (e.g. SSH from Windows PowerShell into WSL), so I'm not blocking myself

### Stage 4: Stretch goals ✨ (only if I'm enjoying it)
- [ ] Write a log of all alerts and bans to a file
- [ ] Simple tests with `pytest` using sample log lines
- [ ] Run it as a `systemd` service so it starts automatically
- [ ] Daily summary: top offending IPs

---

## 🚫 Out of scope (for now)

- Running on real production servers
- Watching services other than SSH
- A web dashboard
- Anything aimed at machines I don't own

---

## 🗂️ Planned repo layout

```
ssh-guard/
├── SPEC.md            # this spec
├── README.md          # written at the end of the build
├── config.example.json
├── ssh_guard.py       # main script
├── tests/             # stage 4
├── sample_logs/       # fake log lines for testing
└── notes/             # what I learned at each stage
```

---

## ✅ Definition of done

- Running ssh-guard and failing 5 SSH logins within 10 minutes from a test IP produces an alert
- With `dry_run: false`, that IP is blocked, cannot connect, and is unblocked after the ban time
- Safe-listed IPs are never blocked
- Someone else could follow this README to set it up
- I can explain, in plain English, how every part works 💬

---

## 🔐 Safety rules

1. Only test on my own machine/lab
2. Keep `dry_run` on until detection is proven
3. Always have the safe list set before enabling blocking
4. Never commit real passwords, email credentials or IPs: use `config.example.json` in the repo and keep the real `config.json` in `.gitignore`
