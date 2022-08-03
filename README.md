# Hypotenuse-Leg
This repository contains code for the HypotenuseLeg discord bot.
It allows you to navigate channels and connect to them.
Everything you send in the sending channel will then be sent through the bot into the receiving channel, and the other way around.
It is only meant for having fun between friends, do not use it for anything malicious.

### Discord's TOS
[Discord's TOS](https://discord.com/developers/docs/policies-and-agreements/terms-of-service)
disallows using
[self bots](https://support.discord.com/hc/en-us/articles/115002192352-Automated-user-accounts-self-bots-).

However, this is not a self bot.
HL is controlling a bot through the discord api, which is normal and not against the rules.

I have not found any evidence that bots being puppeteered by users is against the TOS.
Nevertheless, use at your own risk.

### Updates
discord.py is BACK!

Developement on this bot will continue, although at a slower pace than before

## Setup
This is a bash script that will quickly set up HL
If you're using linux with bash, this most definitely will work.
However, you probably are not, in which case, there are no guarantees.
```sh
git clone https://github.com/AngleSideAngle/Hypotenuse-Leg.git
cd Hypotenuse-Leg
source bin/activate
pip install -r requirements.txt
deactivate
cp secrets_template.py ./src/secrets.py
nano ./src/secrets.py
```
You'll be launched into a text editor where you can edit secrets.py with the proper values for your bot.