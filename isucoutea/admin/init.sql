DROP TABLE IF EXISTS teas;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS location_relations;

CREATE TABLE `teas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `location` varchar(256) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `locations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `location_relations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location_from_id` int(11) NOT NULL,
  `location_to_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
