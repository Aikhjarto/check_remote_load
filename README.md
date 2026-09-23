# check_remote_load

A Nagios/Icinga plugin that reads `/proc/loadavg` from a remote machine via
ssh and checks the 1, 5 and 15 minute load averages.

```sh
check_remote_load -H server.example.com -u monitor -w 1.0,0.8,0.75 -c 2.0,2.0,1.1
```

| Option | Meaning |
|---|---|
| `-H` | Host to connect to (default: localhost) |
| `-u` | User name for ssh (default: root) |
| `-w` | Warning thresholds for the 1, 5 and 15 minute averages (default: 1.0,0.8,0.75) |
| `-c` | Critical thresholds for the 1, 5 and 15 minute averages (default: 2.0,2.0,1.1) |

The monitoring user needs key based ssh access to the remote machine; `bc` is
used for the comparison.
