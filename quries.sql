USE cloudapp;
CREATE TABLE resource_prop (
    res_prop_id INT PRIMARY KEY,
    res_id INT,
    prop_name VARCHAR(30),
    prop_input_type VARCHAR(30),
    is_mandatory VARCHAR(3),
    FOREIGN KEY (res_id) REFERENCES resource(res_id)
);
INSERT INTO resource_prop (res_prop_id, res_id, prop_name, prop_input_type, is_mandatory) VALUES
(1, 1, 'Name', 'textbox', 'yes'),
(2, 1, 'Colour', 'dropdown', 'yes'),
(3, 1, 'Wheelcount', 'textbox', 'yes'),
(4, 1, 'Manufacture', 'dropdown', 'yes'),
(5, 1, 'Isac', 'checkbox', 'yes'),
(6, 3, 'Name', 'textbox', 'yes'),
(7, 3, 'Isitmammal', 'radio', 'yes'),
(8, 2, 'Name', 'textbox', 'yes'),
(9, 2, 'Colour', 'dropdown', 'yes'),
(10, 10, 'Name', 'textbox', 'yes'),
(11, 10, 'Usable', 'radio', 'yes');
