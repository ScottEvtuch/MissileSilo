# Missile Silo

This application is intended to serve as a broker for ssh-agent requests while enforcing "two-person rule" style policies like [the kind used for nuclear missile launches](https://en.wikipedia.org/wiki/Two-man_rule). Missile Silo listens on its own socket where users can request signatures for SSH authentication attempts.

_**This project is very much in the "proof of concept" phase at this point and is not stable at all.**_

* Why use this?

  Good question! I expect the most common use case would be for "break-glass" keys that should only be used in the event of a failure of some other authentication system. If your primary method of login relies on the availability of some LDAP infrastructure you may want to allow a group of trusted people to authenticate without that infrastructure but not allow an individual person to do so.

* Isn't this pointless if the user has root?

  I view this application as more of a policy tool than a security tool. The intention is to provide an easy way to require multiple approvals before the usage a particular SSH key. This is obviously much more secure if other users of the system don't have access to Missile Silo's keys via the filesystem. At some point I will add support for "launch codes" that use something like Shamir's Secret Sharing to protect the private keys.

## Usage

Once Missile Silo is running you can use it like any other SSH agent

```
export SSH_AUTH_SOCK="/tmp/missilesilo"
ssh root@server.example.net
```

```
ssh root@server.example.net -o IdentityAgent="/tmp/missilesilo"
```

```
ansible-playbook site.yml --ssh-common-args='-o IdentityAgent="/tmp/missilesilo"'
```

## Planned Features

- [ ] Forward requests to a list of Duo 2FA users
- [ ] Allow requests to be approved on the command line
- [ ] Protect key data with "launch codes" required to decrypt private keys
