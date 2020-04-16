# Custom subjects
This will give you an introduction to making questions and custom subjects. Please note that it's required to have the role *iq.admin* before running any of the following commands.

### Making a subject
To make your own subjects using: `iq new_subject <name>` where *<name>* is the name of the subject. For example if you wanted to make a computer science subject you could use: `iq new_subject cs`.

### Removing a subject
To remove a subject use: `iq remove_subject <name>` where *<name>* is the name of the subject.

### Assigning a question to a subject
To  assign a question to a specific subject using: `iq add_quest <subject> <level> "<question>" <answer>` where *<subject>* is the subject, *<level>* is the level in the subject, it's required to have double quotes around the *<question>* parameter and at last where *<answer>* is the answer to the question. Examples below.

```
iq add_quest cs 1 "How many bits for a byte?" 8
```
This command shows that the question is being assigned to the *cs* subject. And it is a level 1 question so it is an *easy* question. The question is: *How many bits for a byte?* and we assign the answer to *8*.

```
iq add_quest math 2 "What is the magnitude of this vector? v = [5, 2]" 5.39
```
In this example we assign a question to the *math* subject in level 2 so it's a bit harder than level 1. The question is *What is the magnitude of this vector? v = [5, 2]* and the answer is *5.39*.
