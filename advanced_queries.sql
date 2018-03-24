-- TODO: Setup some mock data to demonstrate the queries


SELECT "First Advanced Query: Party on the queue (%s) with the minimum average play time of the members involved from today";
SELECT party.id AS party_id, party.leader_id, AVG (play_time) AS average_party_play_time_seconds
FROM api_party AS party, api_member AS m1 JOIN
(
    SELECT pin.member_id, SUM((julianday(fm.endDate)-julianday(m2.startDate))*86400.0) AS play_time
    FROM api_match AS m2 JOIN api_finishedmatch fm JOIN api_playedin AS pin
    WHERE m2.id=fm.match_ptr_id AND m2.id=pin.match_id AND date(m2.startDate) > date(julianday())
    GROUP BY pin.member_id
)
WHERE party.id=m1.party_id AND m1.interested_ptr_id=member_id AND party.queue_id = %s
GROUP BY party.id ORDER BY play_time ASC LIMIT 1;



SELECT "Second Advanced Query: Members in order of highest wins/total games ratio";
SELECT member.interested_ptr_id, COUNT(CASE WHEN (playedin.team = 'A' AND match.scoreA > match.scoreB) OR
                                                 (playedin.team = 'B' AND match.scoreB > match.scoreA) THEN 1 ELSE NULL END) AS wins, COUNT(*) AS total_games
FROM (api_member AS member
  INNER JOIN api_playedin AS playedin ON member.interested_ptr_id = playedin.member_id)
  INNER JOIN api_match AS match ON match.id = playedin.match_id
GROUP BY member.interested_ptr_id
ORDER BY wins * 1.0 / total_games DESC;
