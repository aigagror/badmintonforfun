SELECT api_member.interested_ptr_id 
FROM api_member JOIN 
    (SELECT SUM(endDate - startDate) as PLAY_TIME, interested_ptr_id FROM api_finishedmatch GROUP BY interested_ptr_id WHERE start > TODAY()) 
    WHERE api_member.queue_id = %s
ORDER BY PLAY_TIME ASC LIMIT 1;