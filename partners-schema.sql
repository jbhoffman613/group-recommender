drop database if exists partners;
create database partners;
use partners;

-- USER - User_id, Name, Email, Phone number, Year in school, Current grade in class
drop table if exists user;
create table user (
	user_id int primary key,
    user_name varchar(25) NOT NULL,
    email varchar(255) NOT NULL,
    phone_number varchar(100) NULL,
    year int NOT NULL,
    grade double(2,2) NULL
);

-- A skill is like git, AWS, java, python, GoLang, Scala, swift
drop table if exists skill;
create table skill (
	skill_id int primary key,
    skill_name varchar(25) NOT NULL
);

drop table if exists skillset;
create table skillset (
	user_id int NOT NULL,
	skill_id int NOT NULL,
    
    constraint foreign key (user_id) references user(user_id),
    constraint foreign key (skill_id) references skill(skill_id)
);

-- Interest is the project type like web app, mobile app, data visualization, analysis
drop table if exists interest;
create table interest (
	interest_id int primary key,
    interest_name varchar(100) NOT NULL
);

drop table if exists user_interest;
create table user_interest (
	user_id int NOT NULL,
	interest_id int NOT NULL,
    
    constraint foreign key (user_id) references user(user_id),
    constraint foreign key (interest_id) references interest(interest_id)
);

-- Preference is who the user wants to work with. They can prefer up to two people. 
drop table if exists preference;
create table preference (
	user_id int NOT NULL,
    user_prefers int NOT NULL,
    
    constraint foreign key (user_id) references user(user_id),
    constraint foreign key (user_prefers) references user(user_id)
);

-- This is when the user is available. They can be available at multiple times. 
drop table if exists user_availability;
create table user_availability (
	availability_id int primary key, -- allows us to find a particular availability and examine it 
	user_id int,
    day ENUM('Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'),
    start_time TIME,
    end_time TIME,
    
    constraint foreign key (user_id) references user(user_id)
);

-- This is a list of all group groups
drop table if exists project_group;
create table project_group (
	group_id int primary key,
    group_name varchar(25)
);

-- This is who belongs to each group 
drop table if exists group_member;
create table group_member (
	group_id int,
    user_id int,
    
    constraint foreign key (user_id) references user(user_id),
    constraint foreign key (group_id) references project_group(group_id)
);


