`iq` discord bot
================
iq is a discord bot where you can make iq send you a question you can now answer the question with another command and get points. If you get a specific amount of points you'll level up. And then iq will send you even harder questions!

## Invite `iq`
You can [invite iq](https://discordapp.com/oauth2/authorize?client_id=698639299851321364&permissions=8&scope=bot) to your own discord server.


## Commands
Here are some of the commands. All commands have `iq` as their prefix.
```
question         - asks the user a question, can be answered with the answer command.
answer <answer>  - answers a question.
join <subject>   - join a specified subject.
```

### Admin commands
Following commands require `iq.admin` role.
```
new_subject <name> <levels> <quest_per_level> - creates a new subject.
remove_subject <name> - removes a specified subject.

add_quest <subject> <level> "<question>" <answer> - adds a question and it's answer to a specific subject to a specific level. 

remove_quest <subject> <level> "<question>" - removes a question and it's answer from a specific subject from a specific level.
```
In `remove_quest` and `add_quest` the question parameter requires either double or singe quotes around it.

## Authors
[vsp](https://github.com/vsp0) - Head-Developer
