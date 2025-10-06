# Pipe Firestarter Storage

## Installation and Usage Flow

**Note**: This runs on Solana DevNet and uses DevNet SOL. — DO NOT USE MAINNET SOL.

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/PipeNetwork/pipe.git
cd pipe

# Install pipe-cli globally on their system
cargo install --path .
```

This will:
- Build the pipe-cli binary from source
- Install it in `~/.cargo/bin/` (which should be in their PATH)
- Make the `pipe` command available system-wide

### 2. First Time Setup

```bash
# Create a new user account
pipe new-user
```

This will generate a new user ID and app key, storing them in `~/.pipe-cli.json`

### 3. Basic File Operations

```bash
# Upload a single file
pipe upload-file myfile.pdf stored-name

# Download a file
pipe download-file stored-name downloaded.pdf

# Upload with encryption
pipe upload-file sensitive.doc secure --encrypt

# Download and decrypt
pipe download-file secure decrypted.doc --decrypt
```

### 4. Directory Operations

```bash
# Upload an entire directory
pipe upload-directory /path/to/folder

# Upload with a specific tier for faster speed
pipe upload-directory /important/data --tier premium

# Skip files that were already uploaded
pipe upload-directory /large/dataset --skip-uploaded
```

### 5. Advanced Features

```bash
# List all your files
pipe list-uploads

# Get file info
pipe file-info myfile

# Local encryption (without uploading)
pipe encrypt-local file.txt file.txt.enc

# Generate encryption keys
pipe keygen --name mykey --algorithm aes256
```

The key advantage is that after running `cargo install --path .`, users have a fully functional `pipe` command available anywhere on the system, making it easy to upload/download files to the Pipe decentralized storage network with optional client-side encryption.