-- INSERT INTO venue (
--     name,
--     city,
--     state,
--     address,
--     phone,
--     image_link,
--     facebook_link,
--     seeking_talent,
--     seeking_description,
--     website
--   )
-- VALUES (
-- 'Park Square Live Music & Coffee',
-- 'San Francisco',
--   'CA',
--   '1015 Folsom Street',
--   '123-123-1234',
--   'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60', 
--  'https://www.facebook.com/TheMusicalHop', 
--   'true', 
--   'We are on the lookout for a local artist to play every two weeks. Please call us.', 
--   'https://www.themusicalhop.com'
--   );




-- INSERT INTO venue (
--     name,
--     city,
--     state,
--     address,
--     phone,
--     image_link,
--     facebook_link,
--     seeking_talent,
--     seeking_description,
--     website
--   )
-- VALUES (
-- 'The Musical Hop',
-- 'San Francisco',
--   'CA',
--   '1015 Folsom Street',
--   '123-123-1234',
--   'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60', 
--  'https://www.facebook.com/TheMusicalHop', 
--   'true', 
--   'We are on the lookout for a local artist to play every two weeks. Please call us.', 
--   'https://www.themusicalhop.com'
--   );

-- INSERT INTO venue (
--     name,
--     city,
--     state,
--     address,
--     phone,
--     image_link,
--     facebook_link,
--     seeking_talent,
--     seeking_description,
--     website
--   )
-- VALUES (
-- 'The Musical Hop',
-- 'San Francisco',
--   'CA',
--   '1015 Folsom Street',
--   '123-123-1234',
--   'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60', 
--  'https://www.facebook.com/TheMusicalHop', 
--   'true', 
--   'We are on the lookout for a local artist to play every two weeks. Please call us.', 
--   'https://www.themusicalhop.com'
--   );

-- UPDATE venue SET genres='Jazz, Reggae, Swing, Classical,Folk' where id=1;



-- SELECT * from venue


-- INSERT INTO venue (
--     name,
--     city,
--     state,
--     address,
--     phone,
--     image_link,
--     facebook_link,
--     seeking_talent,
--     seeking_description,
--     website,
--     genres
--   )
-- VALUES (
--    'Park Square Live Music & Coffee',
-- 'San Francisco',
--   'CA',
--   '34 Whiskey Moore Ave',
--   '415-000-1234',
--   'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80', 
--  'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', 
--   False, 
--   '', 
--   'https://www.parksquarelivemusicandcoffee.com',
--   'Rock n Roll,Jazz,Classical,Folk'
--   );


-- SELECT * FROM venue


-- INSERT INTO artist (
--     name,
--     city,
--     state,
--     phone,
--     genres,
--     image_link,
--     facebook_link,
--     seeking_venue,
--     seeking_description,
--     website
--   )
-- VALUES (
--    'Guns N Petals',
--    'San Francisco',
--    'CA',
--    '326-123-5000',
--    'Rock n Roll',
--    'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
--    'https://www.facebook.com/GunsNPetals',
--    'True',
--    'Looking for shows to perform at in the San Francisco Bay Area!',
--    'https://www.gunsnpetalsband.com'
--   );


-- INSERT INTO artist (
--     name,
--     city,
--     state,
--     phone,
--     genres,
--     image_link,
--     facebook_link,
--     seeking_venue,
--     seeking_description,
--     website
--   )
--   VALUES (
--    'Matt Quevedo',
--    'New York',
--    'NY',
--    '300-400-5000',
--    'Jazz',
--    'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
--    'https://www.facebook.com/mattquevedo923251523',
--    'False',
--    '',
--    ''
--   );



-- INSERT INTO artist (
--     name,
--     city,
--     state,
--     phone,
--     genres,
--     image_link,
--     facebook_link,
--     seeking_venue,
--     seeking_description,
--     website
--   )
--   VALUES (
--    'The Wild Sax Band',
--    'San Francisco',
--    'CA',
--    '432-325-5432',
--    'Jazz,Classical',
--    'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
--    '',
--    'False',
--    '',
--    ''
--   );


-- SELECT * from artist

-- INSERT INTO show (venue_id, artist_id, start_time)
-- VALUES (
--    3,
--    3,
--    '2035-04-15T20:00:00.000Z'
--   );

-- SELECT  * FROM show



-- INSERT INTO venue (
--     name,
--     city,
--     state,
--     address,
--     phone,
--     image_link,
--     facebook_link,
--     seeking_talent,
--     seeking_description,
--     website,
--     genres
--   )
-- VALUES (
--    'Beerta Banaadir',
-- 'Mogadoshu',
--   'BA',
--   'wadada ceelgaabta',
--   '123-000-5678',
--   'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80', 
--  'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', 
--   True, 
--   'we are seeking a talent perosn', 
--   'https://www.parksquarelivemusicandcoffee.com',
--   'Rock n Roll,Jazz,Classical,Folk'
--   );


-- 5 beerta nabada
-- 4 sharma boy
-- SELECT * from venue;

-- UPDATE artist SET image_link = 'https://i.scdn.co/image/ab67616d0000b2734a6347ba84bf0a55e2d4aeb7' where id = 4;


-- UPDATE artist SET website = 'https://google.com' where id =2


UPDATE venue SET genres='Rock n Roll, Reggae, Swing, Classical' where id =3;
SELECT * FROM venue;

-- DELETE from venue where id=4;