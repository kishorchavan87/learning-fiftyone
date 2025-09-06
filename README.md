# FiftyOne AWS Demo (Free Tier EC2)

This project sets up a **synthetic dataset demo** of [Voxel51 FiftyOne](https://voxel51.com/) on an AWS EC2 Ubuntu instance (t3.micro, Free Tier eligible).

## Steps

### 1. Launch EC2
- Ubuntu 22.04 LTS AMI
- t3.micro (Free Tier)
- Allow SSH (22) from your IP only
- Attach key pair

### 2. SSH in
```bash
ssh -i /path/to/key.pem ubuntu@<EC2_PUBLIC_IP>
