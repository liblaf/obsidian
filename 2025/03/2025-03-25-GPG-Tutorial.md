---
created: 2025-03-25T08:49:16+08:00
modified: 2025-03-25T12:30:21+08:00
tags:
  - Git
  - GPG
  - Security
title: GPG Tutorial
---

## TL;DR

### I just want that green "Verified" badge on my GitHub commits

1. Read this first: [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
2. [Generate a new GPG key](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key)
3. [Tell Git about your signing key](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key)
4. [Add a GPG key to your GitHub account](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account)

### What are public and secret keys?

- Anyone with a **public key** can **encrypt** a message, yielding a *ciphertext*.
- Only the corresponding **private key** can **decrypt** the *ciphertext* to obtain the original message.

## Introduction

### Public-key Cryptography[^wikipedia]

**Public-key cryptography**, or **asymmetric cryptography**, is the field of cryptographic systems that use pairs of related keys. Each key pair consists of a **public key** and a corresponding **private key**. Key pairs are generated with cryptographic algorithms based on mathematical problems termed one-way functions. Security of public-key cryptography depends on keeping the private key secret; the public key can be openly distributed without compromising security.

In a **public-key encryption** system, anyone with a public key can encrypt a message, yielding a *ciphertext*, but only those who know the corresponding private key can decrypt the ciphertext to obtain the original message.

For example, a journalist can publish the public key of an encryption key pair on a web site so that sources can send secret messages to the news organization in ciphertext.

Only the journalist who knows the corresponding private key can decrypt the ciphertexts to obtain the sources' messages --- an eavesdropper reading email on its way to the journalist cannot decrypt the ciphertexts. However, public-key encryption does not conceal metadata like what computer a source used to send a message, when they sent it, or how long it is. Public-key encryption on its own also does not tell the recipient anything about who sent a message --- it just conceals the content of the message.

[^wikipedia]: [Public-key cryptography - Wikipedia](https://en.wikipedia.org/wiki/Public-key_cryptography)

### GNU Privacy Guard[^gnupg]

GnuPG is a complete and free implementation of the OpenPGP standard as defined by [RFC4880](https://www.ietf.org/rfc/rfc4880.txt) (also known as *PGP*). GnuPG allows you to encrypt and sign your data and communications; it features a versatile key management system, along with access modules for all kinds of public key directories. GnuPG, also known as *GPG*, is a command line tool with features for easy integration with other applications.

[^gnupg]: [The GNU Privacy Guard](https://www.gnupg.org/)

### Verify Commit Signature[^github]

You can sign commits and tags locally, to give other people confidence about the origin of a change you have made. If a commit or tag has a GPG, SSH, or S/MIME signature that is cryptographically verifiable, GitHub marks the commit or tag "Verified" or "Partially verified".

[^github]: [About commit signature verification - GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)

## List Keys

```console
$ gpg --keyid-format long --list-options show-ownertrust --list-public-keys
pub   ed25519/9234E2737A49D82A 2025-03-25 [SC] [ultimate]
      FE194EC8F4B09D40FB16B8569234E2737A49D82A
uid                 [ultimate] liblaf <30631553+liblaf@users.noreply.github.com>
sub   cv25519/5632BF6364A13237 2025-03-25 [E]
sub   ed25519/2F451BE41CBA0019 2025-03-25 [S]
```

```console
$ gpg --keyid-format long --list-options show-ownertrust --list-secret-keys
sec   ed25519/9234E2737A49D82A 2025-03-25 [SC] [ultimate]
      FE194EC8F4B09D40FB16B8569234E2737A49D82A
uid                 [ultimate] liblaf <30631553+liblaf@users.noreply.github.com>
ssb   cv25519/5632BF6364A13237 2025-03-25 [E]
ssb   ed25519/2F451BE41CBA0019 2025-03-25 [S]
```

### Key Components Explained

- **key types**:
  - `pub` / `sec`: public / secret primary key
  - `sub` / `ssb`: public / secret subkey
  - `ed25519` / `cv25519`: algorithm
- **key identification**:
  - key ID: `9234E2737A49D82A`
  - fingerprint: `FE194EC8F4B09D40FB16B8569234E2737A49D82A`

### Usage Flags (Capabilities)

| Flag  |     Usage      |
| :---: | :------------: |
| `[E]` |   encryption   |
| `[S]` |    signing     |
| `[C]` | certification  |
| `[A]` | authentication |

The `[SC]` means that key have both:

- signing `[S]` capability
- certification `[C]` capability

This is typically seen on your primary key.

Only the primary key can have the certification `[C]` capability, which allows it to:

- sign other keys (certify them)
- create revocation certificates
- perform identity certifications (UID signatures)

Subkeys can have the following capabilities:

- encryption `[E]`
- signing `[S]`
- authentication `[A]`

### Trust Values

Trust values are used to indicate ownertrust and validity of keys and user IDs. `[ultimate]` in `pub` / `sec` line means **key validity status** (whether YOU consider this key valid). `[ultimate]` in `uid` line means **ownertrust level** (how much you trust THIS KEY'S OWNER to verify OTHER keys). Your own key should have **both** set to `[ultimate]`.

| Letter | Trust Values |                          Description                          |
| :----: | :----------: | :-----------------------------------------------------------: |
|  `-`   |  `unknown`   |         No ownertrust assigned / not yet calculated.          |
|  `e`   |  `expired`   | Trust calculation has failed; probably due to an expired key. |
|  `q`   | `undefined`  |            Not enough information for calculation.            |
|  `n`   |   `never`    |                     Never trust this key.                     |
|  `m`   |  `marginal`  |                      Marginally trusted.                      |
|  `f`   |    `full`    |                        Fully trusted.                         |
|  `u`   |  `ultimate`  |                      Ultimately trusted.                      |
|  `r`   |  `revoked`   |  For validity only: the key or the user ID has been revoked.  |
|  `?`   |    `err`     |        The program encountered an unknown trust value.        |

## Generate a new GPG Key

```console
$ gpg --full-generate-key
gpg (GnuPG) 2.4.7; Copyright (C) 2024 g10 Code GmbH
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

```console
Please select what kind of key you want:
   (1) RSA and RSA
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (9) ECC (sign and encrypt) *default*
  (10) ECC (sign only)
  (14) Existing key from card
Your selection?
```

```console
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (4) NIST P-384
   (6) Brainpool P-256
Your selection?
```

```console
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0)
```

```console
GnuPG needs to construct a user ID to identify your key.

Real name: liblaf
Email address: 30631553+liblaf@users.noreply.github.com
Comment:
You selected this USER-ID:
    "liblaf <30631553+liblaf@users.noreply.github.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
```

```console
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: directory '/home/liblaf/.gnupg/openpgp-revocs.d' created
gpg: revocation certificate stored as '/home/liblaf/.gnupg/openpgp-revocs.d/FE194EC8F4B09D40FB16B8569234E2737A49D82A.rev'
public and secret key created and signed.

pub   ed25519 2025-03-25 [SC]
      FE194EC8F4B09D40FB16B8569234E2737A49D82A
uid                      liblaf <30631553+liblaf@users.noreply.github.com>
sub   cv25519 2025-03-25 [E]
```

## Add a subkey

```console
$ gpg --edit-key '9234E2737A49D82A' addkey
gpg (GnuPG) 2.4.7; Copyright (C) 2024 g10 Code GmbH
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  ed25519/9234E2737A49D82A
     created: 2025-03-25  expires: never       usage: SC
     trust: ultimate      validity: ultimate
ssb  cv25519/5632BF6364A13237
     created: 2025-03-25  expires: never       usage: E
[ultimate] (1). liblaf <30631553+liblaf@users.noreply.github.com>
```

```console
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
  (10) ECC (sign only)
  (12) ECC (encrypt only)
  (14) Existing key from card
Your selection? 10
```

```console
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (4) NIST P-384
   (6) Brainpool P-256
Your selection?
```

```console
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0)
Key does not expire at all
Is this correct? (y/N) y
Really create? (y/N) y
```

```console
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  ed25519/9234E2737A49D82A
     created: 2025-03-25  expires: never       usage: SC
     trust: ultimate      validity: ultimate
ssb  cv25519/5632BF6364A13237
     created: 2025-03-25  expires: never       usage: E
ssb  ed25519/2F451BE41CBA0019
     created: 2025-03-25  expires: never       usage: S
[ultimate] (1). liblaf <30631553+liblaf@users.noreply.github.com>
```

Don't forget to save the changes:

```console
gpg> save
```

## Configure Git

Use the `gpg --keyid-format long --list-secret-keys` command to list the long form of the GPG keys for which you have both a public and private key. A private key is required for signing commits or tags.

From the list of GPG keys, copy the long form of the GPG key ID you'd like to use. You may want to use a subkey. In this example, the GPG subkey ID is `2F451BE41CBA0019`:

```console
$ gpg --keyid-format long --list-secret-keys
sec   ed25519/9234E2737A49D82A 2025-03-25 [SC]
      FE194EC8F4B09D40FB16B8569234E2737A49D82A
uid                 [ultimate] liblaf <30631553+liblaf@users.noreply.github.com>
ssb   cv25519/5632BF6364A13237 2025-03-25 [E]
ssb   ed25519/2F451BE41CBA0019 2025-03-25 [S]
```

To set your GPG signing key in Git, paste the text below, substituting in the GPG key ID you'd like to use.

```console
$ git config --global user.signingKey '2F451BE41CBA0019'
```

If you use multiple keys and subkeys, then you should append an exclamation mark `!` to the key to tell git that this is your preferred key. Sometimes you may need to escape the exclamation mark with a back slash: `\!`.

Optionally, to configure Git to sign all commits and tags by default, enter the following command:

```console
$ git config --global commit.gpgSign true
$ git config --global tag.gpgSign true
```

For more information, see [Signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).

To sign commits associated with your account on GitHub, you can [add a public GPG key to your personal account](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account).

## Export \& Import Keys

### Export Public Keys

```console
$ gpg --armor --export --output 'signing.asc' '2F451BE41CBA0019'
$ cat 'signing.asc'
-----BEGIN PGP PUBLIC KEY BLOCK-----
...
-----END PGP PUBLIC KEY BLOCK-----
```

You can [add the GPG key to your GitHub account](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account).

### Export Secret Keys

> [!WARNING]
> Security of public-key cryptography depends on keeping the private key secret.
> **NEVER NEVER NEVER** share your private key with anyone.

```console
$ gpg --armor --export-secret-keys --output 'secret.asc' '9234E2737A49D82A'
$ cat 'secret.asc'
-----BEGIN PGP PRIVATE KEY BLOCK-----
...
-----END PGP PRIVATE KEY BLOCK-----
```

### Import Secret Keys

```console
$ gpg --import 'secret.asc'
gpg: key 9234E2737A49D82A: public key "liblaf <30631553+liblaf@users.noreply.github.com>" imported
gpg: key 9234E2737A49D82A: secret key imported
gpg: Total number processed: 1
gpg:               imported: 1
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
```

### Trust the Key

Imported keys are not trusted by default. You can trust the key by running the following command:

```console
$ gpg --edit-key '9234E2737A49D82A' trust
gpg (GnuPG) 2.4.7; Copyright (C) 2024 g10 Code GmbH
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  ed25519/9234E2737A49D82A
     created: 2025-03-25  expires: never       usage: SC
     trust: unknown       validity: unknown
ssb  cv25519/5632BF6364A13237
     created: 2025-03-25  expires: never       usage: E
ssb  ed25519/2F451BE41CBA0019
     created: 2025-03-25  expires: never       usage: S
[ unknown] (1). liblaf <30631553+liblaf@users.noreply.github.com>
```

Your own key should have ownertrust set to `[ultimate]`:

```console
sec  ed25519/9234E2737A49D82A
     created: 2025-03-25  expires: never       usage: SC
     trust: unknown       validity: unknown
ssb  cv25519/5632BF6364A13237
     created: 2025-03-25  expires: never       usage: E
ssb  ed25519/2F451BE41CBA0019
     created: 2025-03-25  expires: never       usage: S
[ unknown] (1). liblaf <30631553+liblaf@users.noreply.github.com>

Please decide how far you trust this user to correctly verify other users' keys
(by looking at passports, checking fingerprints from different sources, etc.)

  1 = I don't know or won't say
  2 = I do NOT trust
  3 = I trust marginally
  4 = I trust fully
  5 = I trust ultimately
  m = back to the main menu

Your decision? 5
Do you really want to set this key to ultimate trust? (y/N) y
```

```console
gpg> save
```

## See Also

- [About commit signature verification - GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- [Public-key cryptography - Wikipedia](https://en.wikipedia.org/wiki/Public-key_cryptography)
- [The GNU Privacy Handbook](https://www.gnupg.org/gph/en/manual.html)
