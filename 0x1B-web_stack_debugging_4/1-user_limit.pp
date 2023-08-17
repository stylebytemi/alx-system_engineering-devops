# Create the holberton user if not already present
user { 'holberton':
  ensure => present,
  shell  => '/bin/bash',
  home   => '/home/holberton',
}

# Set the password for the holberton user (replace 'password' with the actual password)
user { 'holberton_password':
  user     => 'holberton',
  password => 'password',
}

# Give the holberton user necessary permissions
file { '/home/holberton':
  ensure  => 'directory',
  owner   => 'holberton',
  group   => 'holberton',
  mode    => '0755',
  require => User['holberton'],
}

# Adjust file limits for the holberton user
exec { 'increase-file-limits-for-holberton':
  command => 'echo "holberton soft nofile 50000" >> /etc/security/limits.conf && echo "holberton hard nofile 50000" >> /etc/security/limits.conf',
  path    => '/usr/local/bin/:/bin/',
  creates => '/etc/security/limits.conf',
}

# Reload PAM configuration to apply the changes
service { 'pam-config-reload':
  command => '/sbin/pam-config -a --user holberton',
  require => Exec['increase-file-limits-for-holberton'],
}

# Allow user to log in via SSH
ssh_authorized_key { 'holberton':
  user    => 'holberton',
  type    => 'ssh-rsa',
  key     => 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCUAc2UnCxXh/gFskYUR4eRNZfZSWx/lJsqbhx0OyBXJslu2AIDJn11jAcjBi3qgM2lkptpw0Y6c6zSgBTiVvaQyb1vlNk3IuKAbxvg5Vd0Mg8OlfqaPHq+jYn+ocgzdPRBLdRz1pngAYi3Be/LfNEEqPa+tGWtapPqVmce3clfU6V38+Z+YTG6iSdRWZCB5NMSSXXIFqxKDK3iw7CtAspXSFXo6mUh327M8CUgrgUxrJRJjKXD3mbq09E/f7+/g6xUBALPUvdn+sgJIygoAb0V8rtguSCVd5zl4atWoLA5v7XBENzNo5A0WEcGPjkkfujkQ+ZlsBavDpEm/XBIaJWuEkovfCsXtBXIprmi4YVoGBfVW8MQab/8iDh03jK5r6bO8nU66Vyde4/PKRj24KNi8qPEwh/YyKqqXp6x938aLmtHFv0DCr/F6AX++wpWH1+6gDkw+OiDfB5BPy6D2XY/qycWbiSAB7cp7twibqT6cI+n2OtRXoqrL7dmpjfqfE5bzb8QzTqn/2kN+Kos0JtoNl8scdNUYM9Sa95YDyojQS40MTvSiGd8aEgXC6n4tL8kkzPIAN2VvjSqigchzdZ1RAp39sQk8FNcCzKvTiPl1VsQzmqUtVxcma0Ask67h1o9vAsfL6goH168pQu0/7qVofOiC6oFWOLqfX3f4jaBrw== root@8357930305de',
  ensure  => present,
  require => User['holberton'],
}
