# Deployment Scenarios

This guide covers common ways to run the memory system depending on your setup.

> **Vault repo visibility policy:**
> - Workspace template repo (this repo) — public is fine
> - Your runtime workspace repo — **private recommended**
> - Your vault repo — **private required**. Your vault contains personal memory data (conversations, decisions, notes). Never make it public.

## 1. Local Machine (Simplest)

Everything runs on your personal computer — OpenClaw, workspace, and vault.

```
Your PC
├── OpenClaw Gateway
├── workspace/  (~/.openclaw/workspace/)
└── vault/      (~/vaults/my-workspace/)
```

**Pros:** Zero network setup. Git push/pull handles backup.
**Cons:** Agent only runs when your machine is on.

No special configuration needed — follow the [Getting Started](../README.md#getting-started) steps.

## 2. Dedicated Server (Always-On)

Run OpenClaw on a dedicated machine (spare PC, Raspberry Pi, VPS, WSL instance) so the agent is always available. Your personal device accesses the vault for reading/editing.

```
Dedicated Server                    Your PC / Tablet / Phone
├── OpenClaw Gateway                ├── Obsidian / VS Code
├── workspace/                      └── vault/ (via git or SMB)
└── vault/ (source of truth)
```

### Vault Access from Your Devices

The vault lives on the server. To read/edit from your personal device:

**Option A: Git sync (recommended)**

Both the server and your device clone the same vault repo. Changes sync via git push/pull.

```bash
# On your personal device
# ⚠️ Your vault repo MUST be private — it contains personal memory data.
git clone git@github.com:you/my-vault-private.git ~/vaults/my-workspace

# Periodic sync (or use obsidian-git plugin)
cd ~/vaults/my-workspace && git pull
```

- ✅ Works everywhere (local, remote, mobile via Working Copy)
- ✅ Full history and conflict resolution
- ⚠️ Not real-time — requires explicit sync

**Option B: SMB/CIFS share (real-time access)**

Share the vault directory from the server via SMB. Mount it on your personal device.

```bash
# On the server — install and configure Samba
sudo apt install samba
# Add to /etc/samba/smb.conf:
# [vault]
#   path = /home/you/vaults/my-workspace
#   valid users = you
#   read only = no

# On your device (Linux/macOS)
sudo mount -t cifs //server-ip/vault ~/vaults/my-workspace -o username=you

# On Windows
# Map network drive: \\server-ip\vault
```

- ✅ Real-time — edits appear instantly on both sides
- ✅ Obsidian can open the vault directly
- ⚠️ Requires local network (or VPN for remote)
- ⚠️ No built-in history — pair with git for safety

**Recommended: Git + SMB together**

Use git as the source of truth and backup layer. Use SMB for real-time Obsidian access when on the same network.

```
vault/ (on server)
├── .git/          ← git handles backup + history
└── *.md           ← SMB provides real-time access
```

The server's `vault-backup.sh` cron commits and pushes daily, so even if SMB drops, nothing is lost.

### Firewall Notes

If using SMB, only expose it on your local network:

```bash
# UFW example — allow SMB only from local subnet
sudo ufw allow from 192.168.1.0/24 to any port 445
```

Never expose SMB to the public internet.

## 3. Cloud VPS (Remote-First)

Same as the dedicated server setup, but the server is a cloud VPS (AWS, DigitalOcean, etc.).

- Git sync is the primary vault access method (SMB over public internet is not recommended)
- Use SSH tunneling if you need real-time access: `ssh -L 8445:localhost:445 vps`
- Consider [Tailscale](https://tailscale.com/) or WireGuard for secure LAN-like access

## Which Setup Should I Use?

| Scenario | Recommendation |
|---|---|
| Just trying it out | Local machine |
| Want 24/7 agent availability | Dedicated server |
| Use Obsidian on multiple devices | Dedicated server + git sync |
| Want real-time vault editing | Dedicated server + SMB |
| No spare hardware | Cloud VPS + git sync |
