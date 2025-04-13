# EE5523-Final-Project

## Getting Started with GitHub

Follow these commands to get a development environment setup.

I have a macbook but I also use WSL on my Windows desktop.

### Create an SSH key

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Terminal:

```bash
deepvoicepickle@Windows:~$ ssh-keygen -t rsa -b 4096 -C "dgonzales4055@gmail.com"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/deepvoicepickle/.ssh/id_rsa): <press enter here>
Enter passphrase (empty for no passphrase): <press enter here>
Enter same passphrase again: <press enter here>
Your public key has been saved in /home/deepvoicepickle/.ssh/id_rsa.pub
The key fingerprint is:
...
<stuff pops up here>
...
```

> Simply press enter for all the prompts above

Next, it should generate a file called `id_rsa.pub`

Run these commands:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

Terminal Output:

```bash
ssh-add ~/.ssh/id_rsa
Agent pid 986
Identity added: /home/deepvoicepickle/.ssh/id_rsa (dgonzales4055@gmail.com)
```

Finally, view the actual key and copy it to your clipboard:

```bash
deepvoicepickle@Windows:~$ cat ~/.ssh/id_rsa.pub
ssh-rsa copymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopyme
copymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopyme
copymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopyme
copymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopymecopyme dgonzales4055@gmail.com
```

> That isn't my actual key lol

Next, log into GitHub and go to Settings:

![alt text](image.png)

Then, click on SSH and GPG keys

![alt text](image-1.png)

Now, click on the New SSH key green button:

![alt text](image-2.png)

Finally, add the key:

![alt text](image-3.png)

## Testing to make sure this works

Clone the repo:

```bash
git clone git@github.com:dilldylanpickle/EE5523-Final-Project.git
```

Terminal Output:

```bash
deepvoicepickle@Windows:/mnt/c/Users/deepv/GitHub$ git clone git@github.com:dilldylanpickle/EE5523-Final-Project.git
Cloning into 'EE5523-Final-Project'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Receiving objects: 100% (3/3), done.
```

Run this command:

```bash
ssh -T git@github.com
```

Terminal Output:

```bash
deepvoicepickle@Windows:/mnt/c/Users/deepv/GitHub/EE5523-Final-Project$ ssh -T git@github.com
Hi dilldylanpickle! You've successfully authenticated, but GitHub does not provide shell access.
```

Set up remote so you dont need to enter password:

```bash
git remote set-url origin git@github.com:dilldylanpickle/EE5523-Final-Project.git
```
