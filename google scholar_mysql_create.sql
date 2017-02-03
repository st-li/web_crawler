CREATE TABLE `google_publication` (
	`publication_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`cate1_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`cate2_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`name` varchar(255) NOT NULL DEFAULT '',
	`desc` TEXT NOT NULL,
	`h5_idx` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`h5_med` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`rank` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`publication_id`),
	KEY `cate1_id` (`cate1_id`),
	KEY `cate2_id` (`cate2_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `google_articles` (
	`article_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`publication_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`cate1_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`cate2_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`article_title` varchar(255) NOT NULL DEFAULT '',
	`article_link` varchar(255) NOT NULL DEFAULT '',
	`article_authors` varchar(255) NOT NULL DEFAULT '',
	`publish_info` varchar(255) NOT NULL DEFAULT '',
	`ref_link` varchar(255) NOT NULL DEFAULT '',
	`ref_count` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`publish_date` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`article_id`),
	KEY `publication_id` (`publication_id`),
	KEY `cate1_id` (`cate1_id`),
	KEY `cate2_id` (`cate2_id`),
	KEY `publish_date` (`publish_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `google_affiliations` (
	`affiliation_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`publication_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`article_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`desc` TEXT NOT NULL,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`affiliation_id`),
	KEY `publication_id` (`publication_id`),
	KEY `article_id` (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `google_authors` (
	`author_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`publication_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`article_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`affiliation_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`fullname` varchar(255) NOT NULL DEFAULT '',
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`author_id`),
	KEY `publication_id` (`publication_id`),
	KEY `article_id` (`article_id`),
	KEY `affiliation_id` (`affiliation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `google_category` (
	`cate_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`fid` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
	`name` varchar(255) NOT NULL DEFAULT '',
	`cate_url` TEXT NOT NULL,
	`create_time` DATETIME NOT NULL,
	`last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`cate_id`),
	KEY `fid` (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

