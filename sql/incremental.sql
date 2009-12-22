-- incremental changes to make original bouncer DB work in Django

-- primary keys
ALTER TABLE `mirror_ip_to_country` ADD `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

ALTER TABLE `mirror_location_mirror_map` DROP PRIMARY KEY ,ADD UNIQUE ( `location_id` , `mirror_id` ) ;
ALTER TABLE `mirror_location_mirror_map` ADD `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

ALTER TABLE `mirror_mirror_region_map` DROP PRIMARY KEY , ADD UNIQUE ( `mirror_id` , `region_id` );
ALTER TABLE `mirror_mirror_region_map` ADD `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

-- boolean fields
ALTER TABLE `mirror_location_mirror_map` CHANGE `location_active` `location_active` TINYINT NOT NULL DEFAULT '0' ;
UPDATE `mirror_location_mirror_map` SET location_active = 0 WHERE location_active = 1;
UPDATE `mirror_location_mirror_map` SET location_active = 1 WHERE location_active = 2;
ALTER TABLE `mirror_mirrors` CHANGE `mirror_active` `mirror_active` TINYINT NOT NULL DEFAULT '0' ;
UPDATE `mirror_mirrors` SET mirror_active = 0 WHERE mirror_active = 1;
UPDATE `mirror_mirrors` SET mirror_active = 1 WHERE mirror_active = 2;
ALTER TABLE `mirror_products` CHANGE `product_active` `product_active` TINYINT NOT NULL DEFAULT '1' ;
UPDATE `mirror_products` SET product_active = 0 WHERE product_active = 1;
UPDATE `mirror_products` SET product_active = 1 WHERE product_active = 2;

-- foreign keys
ALTER TABLE `mirror_country_to_region` CHANGE `region_id` `region_id` INT( 10 ) UNSIGNED NULL DEFAULT NULL;
UPDATE `mirror_country_to_region` SET region_id = NULL WHERE region_id = 0;
ALTER TABLE `mirror_regions`  ENGINE =  InnoDB;
ALTER TABLE `mirror_country_to_region` ADD FOREIGN KEY ( `region_id` ) REFERENCES `mirror_regions` (`region_id`) ON DELETE SET NULL ;

-- converted users
ALTER TABLE `mirror_users` ADD `converted` TINYINT NOT NULL DEFAULT '0';
