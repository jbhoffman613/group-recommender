drop database if exists partners;
create database partners;
use partners;

-- USER - User_id, Name, Email, Phone number, Year in school, Current grade in class
drop table if exists user;
create table user (
	user_id int primary key,
    user_name varchar(25),
    email varchar(255),
    phone_number varchar(100),
    year int,
    grade double(2,2)
);

drop table if exists skill;
create table skill (
	skill_id int primary key,
    skill_name varchar(25)
);

drop table if exists skillset;
create table skillset (
	user_id int,
	skill_id int,
    
    constraint foreign key (user_id) references user(user_id),
    constraint foreign key (skill_id) references skill(skill_id)
);

drop table if exists interest;
create table interest (
	interest_id int primary key,
    interest_name varchar(100)
);

drop table if exists user_interest;
create table user_interest (
	user_id int,
	interest_id int,
    
    constraint foreign key (user_id) references user(user_id),
    constraint foreign key (interest_id) references interest(interest_id)
);

drop table if exists preference;
create table preference (
	user_id int,
    user_prefers int,
    
    constraint foreign key (user_id) references user(user_id),
    constraint foreign key (user_prefers) references user(user_id)
);

drop table if exists user_availability;
create table user_availability (
	availability_id int primary key, -- allows us to find a particular availability and examine it 
	user_id int,
    day ENUM('Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'),
    start_time TIME,
    end_time TIME,
    
    constraint foreign key (user_id) references user(user_id)
);

drop table if exists project_group;
create table project_group (
	group_id int primary key,
    group_name varchar(25)
);

drop table if exists group_member;
create table group_member (
	group_id int,
    user_id int,
    
    constraint foreign key (user_id) references user(user_id),
    constraint foreign key (group_id) references project_group(group_id)
);


