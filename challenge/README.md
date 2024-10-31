# HTTP Request Smuggling CTF Challenge

## Challenge Description

Our company recently upgraded its blog platform to use HTTP/2 for better performance. However, we still maintain compatibility with older systems through HTTP/2 downgrading. The admin reviews all reported posts for security. Can you find a way to gain admin access?

**Difficulty**: Hard  
**Category**: Web Security  
**Points**: 500  

## Story

As a security researcher, you've discovered a blog platform that recently upgraded to HTTP/2. The platform allows users to:
- Create and view blog posts
- Report suspicious content
- Admin automatically reviews reported content

Your goal is to exploit the system and capture the flag from the admin dashboard.

## Setup Instructions

1. Clone this repository
2. Add to your /etc/hosts:
```bash
127.0.0.1 localhost
```

3. Start the challenge:
```bash
cd challenge
./setup/init.sh
```

4. Access the platform at https://localhost

## Initial Access

You have been provided with a regular user account:
- Username: `alice`
- Password: `user1_pass`

## Objective

Find and exploit vulnerabilities in the platform to:
1. Access the admin dashboard
2. Retrieve the flag

The flag format is: `CTF{...}`

## Notes

- The platform uses HTTP/2 with downgrading to HTTP/1.1
- All reported posts are automatically reviewed by an admin
- The admin dashboard contains the flag
- Do not attack the infrastructure or other participants

Good luck!