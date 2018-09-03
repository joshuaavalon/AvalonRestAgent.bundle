# AvalonRestAgent.bundle

[![license](https://img.shields.io/github/license/joshuaavalon/AvalonRestAgent.bundle.svg)](https://github.com/joshuaavalon/AvalonRestAgent.bundle/blob/master/LICENSE)

This is a Plex rest API agent.
This allows users to implement your own rest API metadata server without implement the Plex agent.

## Requirements

* Able to implement your rest API metadata server with any language


## Install 

```bash
cd /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/
git clone https://github.com/joshuaavalon/AvalonRestAgent.bundle.git
chown plex:plex AvalonRestAgent.bundle
service plexmediaserver restart
```

You need to enter Plex token and metadata server URL in setting.

## API Schema

[See here][schema]


## Frequently Asked Questions

**How do I implement an rest API metadata server?**

Read the [schema][schema] and implement it yourself. 
If you do not know how to do it, this agent is not designed for you.

**I do not want to open my metadata server to public. What should I do?**

There are two ways to do it.

1. Place the metadata server in the same LAN of Plex. Use LAN ip for the agent to access.
2. Implement HTTP basic authentication in your API server. Then, you can use http://username:password@example.com for the server address.


[schema]: https://joshuaavalon.github.io/AvalonRestAgent.bundle/