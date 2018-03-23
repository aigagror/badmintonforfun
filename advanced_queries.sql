-- TODO: Setup some mock data to demonstrate the queries


SELECT "First Advanced Query: Members on the queue with the minimum amount of play time from today";
-- TODO
SELECT api_member.interested_ptr_id
FROM api_member JOIN
    (SELECT SUM(endDate - startDate) as PLAY_TIME, interested_ptr_id
     FROM api_finishedmatch GROUP BY interested_ptr_id
     WHERE start > TODAY())
    WHERE api_member.queue_id = 'CASUAL'
ORDER BY PLAY_TIME ASC LIMIT 1;



SELECT "Second Advanced Query: Members in order of highest wins/total games ratio";
-- TODO