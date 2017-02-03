CREATE TABLE `candidate_basic` (
	`cb_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`country_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`college_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`discipline_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`fullname` varchar(255) NOT NULL DEFAULT '',
	`academic_title` varchar(255) NOT NULL DEFAULT '',
	`other_title` varchar(255) NOT NULL DEFAULT '',
	`nationality` varchar(255) NOT NULL DEFAULT '',
	`email` varchar(255) NOT NULL DEFAULT '',
	`phonenumber` varchar(255) NOT NULL DEFAULT '',
	`external_link` varchar(255) NOT NULL DEFAULT '',
	`experience` TEXT NOT NULL,
	`desc` TEXT NOT NULL,
	`extra` TEXT NOT NULL,
	`avatar_url` TEXT NOT NULL,
	`discipline_desc` TEXT NOT NULL,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`cb_id`),
	KEY `country_id` (`country_id`),
	KEY `college_id` (`college_id`),
	KEY `discipline_id` (`discipline_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `candidate_education` (
	`ce_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`cb_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`college` varchar(255) NOT NULL DEFAULT '',
	`discipline` varchar(255) NOT NULL DEFAULT '',
	`start_time` varchar(255) NOT NULL DEFAULT '',
	`end_time` varchar(255) NOT NULL DEFAULT '',
	`duration` varchar(255) NOT NULL DEFAULT '',
	`degree` varchar(255) NOT NULL DEFAULT '',
	`desc` TEXT NOT NULL,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`ce_id`),
	KEY `cb_id` (`cb_id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `candidate_research` (
	`cr_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`cb_id` bigint UNSIGNED NOT NULL DEFAULT 0,
	`interests` TEXT NOT NULL,
	`current_research` TEXT NOT NULL,
	`research_summary` TEXT NOT NULL,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`cr_id`),
	KEY `cb_id` (`cb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `candidate_publications` (
	`cp_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`cb_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`publications` varchar(255) NOT NULL DEFAULT '',
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`cp_id`),
	KEY `cb_id` (`cb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `candidate_courses` (
	`cc_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`cb_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`courses_no` varchar(20) NOT NULL DEFAULT '',
	`courses_desc` TEXT NOT NULL,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`cc_id`),
	KEY `cb_id` (`cb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `candidate_workexperience` (
	`cw_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`cb_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`job_title` varchar(255) NOT NULL DEFAULT '',
	`company` varchar(255) NOT NULL DEFAULT '',
	`start_time` varchar(255) NOT NULL DEFAULT '',
	`end_time` varchar(255) NOT NULL DEFAULT '',
	`duration` varchar(255) NOT NULL DEFAULT '',
	`desc` TEXT NOT NULL,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`cw_id`),
	KEY `cb_id` (`cb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dim_college` (
	`college_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`country_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`state_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`city_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`college_name` varchar(255) NOT NULL DEFAULT '',
	`college_desc` TEXT NOT NULL,
	PRIMARY KEY (`college_id`),
	KEY `country_id` (`country_id`),
	KEY `state_id` (`state_id`),
	KEY `city_id` (`city_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dim_country` (
	`country_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`country_ab` varchar(20) NOT NULL DEFAULT '',
	`country_full` varchar(255) NOT NULL DEFAULT '',
	PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dim_city` (
	`city_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`city_ab` varchar(20) NOT NULL DEFAULT '',
	`city_full` varchar(255) NOT NULL DEFAULT '',
	PRIMARY KEY (`city_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dim_state` (
	`state_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`state_ab` varchar(20) NOT NULL DEFAULT '',
	`state_full` varchar(255) NOT NULL DEFAULT '',
	PRIMARY KEY (`state_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dim_discipline` (
	`discipline_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`discipline_origin` varchar(255) NOT NULL DEFAULT '',
	`discipline_chinese` varchar(255) NOT NULL DEFAULT '',
	PRIMARY KEY (`discipline_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

