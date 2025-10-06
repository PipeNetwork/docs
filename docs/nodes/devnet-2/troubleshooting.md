# Troubleshooting

Help for troubleshooting common mistakes

## Issues and Solutions

### systemd Service Stuck in Activating Status

1) Test systemd config: 
```bash
sudo systemd-analyze verify pop.service
```
- If no output, no errors were detected

2) Review service config:
```bash
cat /etc/systemd/system/pop.service
```

3) Compare with documentation example

### curl/wget Download Issues

If download seems incomplete:

1) Test download URL:
```bash
curl -I -s https://downloadurl.com | head -n 1
curl -Is https://downloadurl.com >/dev/null && echo "URL is accessible! ✅" || echo "URL is not accessible ❌"
```

2) Verify binary:
```bash
./pop --version
```

### Port Conflicts

**Error**: `Error: Os { code: 98, kind: AddrInUse, message: "Address already in use" }`

Solutions:
1. Disable old DevNet1 instances
2. Reboot server
3. Check port usage:
```bash
sudo lsof -i :8003
# or
sudo netstat -tulpn | grep 8003
```

### Multiple Config Files

#### Common Error Messages
- "IP-xxx.xx.xxx.xxx is already associated with node_id=..."
- "Node already registered"
- "Failed to register node"

#### Root Cause
Multiple `node_info.json` files can cause registration conflicts.

#### Diagnostic Script

Save as `find-nodeinfo.sh`:

```bash
#!/bin/bash
echo "Searching for node_info.json files..."
echo "----------------------------------------"

sudo find / -name node_info.json -type f -exec stat --format="%Z %n" {} \; 2>/dev/null | sort -n > /tmp/node_files.txt

if [ ! -s /tmp/node_files.txt ]; then
    echo "No node_info.json files found on the system"
    exit 0
fi

echo "Found node_info.json files:"
while IFS=" " read -r mtime path; do
    echo "  $path (modified: $(date -d @$mtime '+%Y-%m-%d %H:%M:%S'))"
done < /tmp/node_files.txt
```