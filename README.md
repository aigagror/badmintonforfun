# Documentation

## Badminton Ranked Play
*We will reserve one or two courts for ranked play. Participation is OPTIONAL. No one is pressured to play rank.*

### Goal
The goal of this system is to provide a method for matching players of similar skill level while also breaking the ice between people who don’t know each other very well. 

With every type of ranking system, there is also the glory of being at the top amongst your peers.

It is also meant to provide a convenient way for people to keep track and view their own as well as other people’s statistics. 

### The System
The System organizes the matches and records the results of each match. The system is only active during play time. During play, people sign into the system with their e-mail whenever they want to participate. People may also sign out at anytime. (Only official members of BFF may participate)

### Pairing
When a court becomes available, the system will generate a pair of players who are signed in. The system will try to match players that are closest in rank, with some degree of randomness. People who have been in the system longer and have not played a match will have a higher priority of being chosen. They decide whether they would like to challenge each other to a match or opt-out of a match. If a player does not respond within a certain time (e.g. 15 minutes), then it is considered an automatic opt-out. 

### What Happens During a Pairing
The following is a list of each scenario when the system has paired two people.

#### Both people challenge each other
The pair shall play a match. The winner receives a point towards their “Win” score. The loser gets nothing.

The players, score, and date of the match shall be recorded. 

Only certain players (e.g. board members) can record and submit the result of matches.

#### One challenges, the other opts out
The person who challenged receives a point towards their “Feared” score. And the person who opted out gets nothing. 

The date shall be recorded, but the person who opted out will not be in order to prevent any embarrassment. 

#### Both Players opt out
Nothing happens and nothing is recorded. 

### After a Pairing has Concluded
Both players are put back into the system’s queue to be paired with another random player. 

### Showing the Rankings
A website will display the list of players who were part of the system. 

The website should be able to query the players based on their Win score, their Feared score, a given time frame, number of matches, and/or their name.  


## Tournaments
In the middle of each semester, we host our traditional BFF tournament. It is a single elimination tournament, where each match is decided by a best of 3. Registered people sign-up before hand and each participant is randomly assigned a partner. Each team can give themselves a team name, which is optional.

A website should display a tree-based structure of the current state of the tournament. The leaf nodes contain information about the teams. The internal nodes contain information about the matches, including the score of the games, the dates played, and the overall winner. Here is a simple example: 
![alt text](https://github.com/aigagror/CS-411-BFF/blob/master/Sketch.png)


## Registrations
Registering for BFF requires a set of information
* Name
* Nickname (optional)
* NetID and/or phone number (depending on whether you are a UIUC student or not)
* E-mail address

People register on two tiers: 
1. Interested
2. Membership

|                                       | Interested                                      | Membership                |
|---------------------------------------|-------------------------------------------------|---------------------------|
| **Cost**                              | Free                                            | Membership Fee (e.g. $25) |
| **Duration**                          | Forever (unless unsubscribed from mailing list) | One semester. After that, their registration is downgraded to Interested. Can be renewed for next semester |
| **Can play badminton**                | No                                              | Yes                       |
| **Cost to participate in tournaments**| Some small fee (e.g. $5)                        | Free                      |
| **Will receive e-mails**              | Yes                                             | Yes                       |
| **Can use the new Rank Play system**  | No                                              | Yes                       |

### Checking Members
Members should be able to be queried based on name, netID and/or e-mail. Many people try to sneak into our club during playtime, and so it is important to quickly query members.

### Security and Accounts
Create accounts for each user. If users who have already registered are creating an account, they should be able to link their account to their registration (e.g. providing the e-mail that they used to register)
(OAuth login)


## The Board
The board is a specific group of people who are elected to run BFF. Every person on the board must be a registered member of BFF. The term of a board member is one year, and starts and ends in mid-May.

Within the board, there are certain roles that people can take on:

|	                      | President	            | Treasurer	                  | Officer |
|-----------------------|-----------------------|-----------------------------|---------|
| **Can have multiple**	| No	                  | No                          |	Yes     |
| **Description**	      | Makes lead decisions	| Handles financial situation	| Offers advice, feedback, and helps run the club whenever needed |

### Elections
At the end of every Spring semester, a new election is held in order to determine the new set of board members for next year. People who want to be on the board will state what role they want to apply for. They will also submit a short essay on why they want to apply for that role.

### Voting
Only registered members of BFF can vote for the candidates during the election. Voters must supply their e-mail when voting in order to ensure that they vote at most once.
