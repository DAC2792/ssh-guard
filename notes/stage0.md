1. Installed an SSH server on my local device to begin testing log in attempts

2. Checked the SSH server was running and listening on port 22 (local)

3. Successfully logged in to the SSH and then closed connection from Linux

4. Purposely failed 3 successive login attempts to test if I'd be pushed out, SSH closed the connection. I could re-attempt another login immediately, SSH guard however will lock the users IP in future.

5. Accessed the log history and found all traces of login attempts (successful and unsuccessful)