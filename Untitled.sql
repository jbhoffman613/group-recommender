use partners;
--- Workbook used to formulate and test the queries in the backend

(select * from skillset where user_id = 9 and skill_id in
(select skill_id from skillset where user_id = 2))
union (select * from skillset where user_id = 2) order by skill_id;

select
	user1.skill_id,
    user1.user_id as user2_id,
    user1.value as value1,
    user2.user_id as user2_is,
    user2.value as value2
from skillset as user1
join skillset as user2 ON
	user1.skill_id = user2.skill_id
where
	user1.user_id = 2 and
    user2.user_id = 9;

select count(*) as valuesBroken
from user_interest
where user_id = 0
and interest_id not in
(select interest_id from user_interest where user_id = 2);

select count(*) from availability
where user_id = 2;

select
	count(*)
from availability as user1
join availability as user2 on user1.day = user2.day and user1.start = user2.start
where user1.user_id = 2 and user2.user_id = 3;

select (select count(*) from availability
where user_id = 2) - (select
	count(*)
from availability as user1
join availability as user2 on user1.day = user2.day and user1.start = user2.start
where user1.user_id = 2 and user2.user_id = 3) as valuesBroken;

select count(*) as valuesBroken
from skillset as user1
	join skillset as user2 ON user1.skill_id = user2.skill_id
where user1.user_id = 2 and user2.user_id = 27 and user1.value != user2.value;

select * from user_preference where user_preference.user_id=4;

select ABS((select year from user where user_id = 0) - (select year from user where user_id = 1)) as diff_year;

select user_id from user where user_id != 2;

SELECT
	skill_name
FROM skillset
INNER JOIN skill ON
	(skillset.skill_id = skill.skill_id)
WHERE user_id = 0;

update skill
	set skill_name='Non-relational'
    where skill_id = 0;

update skill
	set skill_name='Python'
    where skill_id = 1;

update skill
	set skill_name='Java'
    where skill_id = 2;

update skill
	set skill_name='Flask/Python Web Frameworks'
    where skill_id = 3;

update skill
	set skill_name='GitHub'
    where skill_id = 4;

update skill
	set skill_name='AWS'
    where skill_id = 5;

update skill
	set skill_name='JS'
    where skill_id = 6;

update skill
	set skill_name='Racket'
    where skill_id = 7;

update skill
	set skill_name='Scala'
    where skill_id = 8;

update skill
	set skill_name='HTML/CSS'
    where skill_id = 9;

select * from skill;

SELECT
	user_id,
	skill_name
FROM skillset
INNER JOIN skill
	ON (skillset.skill_id = skill.skill_id)
WHERE user_id = 0;

select name, email, phone_number from user where user_id in (0, 17, 19, 22);

select * from user;

-- update skill
-- 	set skill_name='Non-relational'
--     where skill_id = 0;
