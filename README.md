# CS-411-BFF
🏸💯💯

See the [documentation](https://github.com/aigagror/CS-411-BFF/tree/master/Documentation)


* SQL Script to set up
* APIs
Interested(Person ID, Name, Former Board Member, E-mail)

	* Registered As Interested
	* Take Interested -> Member
	* Delete Interested
	* Mail to Interested
	
Member(Person ID, Level, Private/Public, Date Joined)

	* Member -> Interested
	* Set Private Public Interested
	* Set Level
	* Member -> Board Member
	
Board Member(Person ID, Job)

	* Board Member -> Member
	* Change job of board member
	
Election(Date)

	* Create new election
	* See results of election
	* Delete election
	
Votes(Votee ID, Election Date, Voter ID)

	* Vote for somebody
	* Modify your vote
	
Campaign(Job, Pitch, Election Date, Campaigner ID)

	* Add a new campaign
	* Withdraw from campaign
	* Add pitch
	* Modify pitch
	
Queue(Type)

	* Add team to queue of type
	* Remove self from queue
	
Match(Match ID, Start Date, A Score, B Score, Team A ID, Team B ID)

	* Create match
	* Finish Match -> Change ELO Score
	* Change Score
	* View all matches
	
Finished Match(Match ID, End Date)

	* View finished matches
	* Calculate time played per person per day
	
IsIn(Member ID, Queue Type)

	* What queues is `ID` in?
	
Court(Court ID)

	* Add courts
	* Delete courts
	* Is there a match currently playing?
	
Tournament(Date)

	* Add tournament
	* Report winner
	* Add match to tournament
	* Add court to type
	* Change court's queue type
	* Remove court's queue type
	* Add match to court
	* Remove match
