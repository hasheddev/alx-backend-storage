-- creates a stored procedure AddBonus that adds a new correction for a student.

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS AddBonus (
	IN user_id INT, IN project_name varchar(255), IN score INT)
BEGIN
	DECLARE nameCount INT;
	DECLARE projectId INT;
	SELECT COUNT(*) INTO nameCount FROM projects WHERE name = project_name;
	IF nameCount = 0 THEN
		INSERT INTO projects(name) VALUES(project_name);
	END IF;
	SELECT id INTO projectId FROM projects WHERE name = project_name;
	INSERT INTO corrections(user_id, project_id, score) VALUES(user_id, projectId, score);
END //
DELIMITER ;
