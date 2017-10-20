# Python tcp tunnel over ssh

This script is useful when ssh tunneling is disabled on the remote server.

1. Copy the `tunserver.py` to remote server (e.g. via sftp)
2. Run `python tunnel.py remote-server-address 'python /path-to/tunserver.py target-host port'
3. Connect to local port `5080`

(todo - make local port configurable and remote server port too)