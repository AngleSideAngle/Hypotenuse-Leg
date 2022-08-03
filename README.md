# Hypotenuse-Leg
---
The code for the HypotenuseLeg discord bot, it allows you to navigate channels and connect to them. Everything you send in the sending channel will then be sent through the bot into the receiving channel, and the other way around.
It is only meant for having fun between friends, do not use it for anything malicious.

Update: discord.py is BACK!
Developement on this bot will continue, although at a slower pace than before

# Setup
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