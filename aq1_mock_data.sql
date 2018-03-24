INSERT INTO api_party VALUES (2, 'CASUAL', 'ezhuang2@illinois.edu');

UPDATE api_member SET party_id=2 WHERE interested_ptr_id='tyou4@illinois.edu' OR interested_ptr_id='sujayd2@illinois.edu' OR interested_ptr_id='ezhuang2@illinois.edu';
