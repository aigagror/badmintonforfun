-- TODO: Setup some mock data to demonstrate the queries


SELECT "First Advanced Query: Party on the queue with the minimum average play time of the members involved from today";




SELECT "Second Advanced Query: Members in order of highest wins/total games ratio";
SELECT member.interested_ptr_id, COUNT(CASE WHEN (playedin.team = 'A' AND match.scoreA > match.scoreB) OR
                                                 (playedin.team = 'B' AND match.scoreB > match.scoreA) THEN 1 ELSE NULL END) AS wins, COUNT(*) AS total_games
FROM api_member AS member, api_match AS match, api_playedin AS playedin
WHERE member.interested_ptr_id = playedin.member_id AND match.id = playedin.match_id
GROUP BY member.interested_ptr_id
ORDER BY wins * 1.0 / total_games DESC;
