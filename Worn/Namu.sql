-- SELECT * FROM namuwiki.namuwiki;
-- SELECT * FROM namuwiki.namuwiki where title = "걸그룹";
-- SELECT * FROM namuwiki;
-- SELECT COUNT(*)
ALTER TABLE namuwiki CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER DATABASE namuwiki CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
SHOW variables LIKE 'c%';