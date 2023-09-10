create_notifications = """
INSERT INTO public.wrappers (name, body, id, created_at, updated_at)
VALUES ('Wrapper 1', 'Wrapper Body 1', '123e4567-e89b-12d3-a456-426614174000', NOW(), NOW());

INSERT INTO public.senders (name, description, id, created_at, updated_at)
VALUES ('Sender 1', 'Description 1', '123e4567-e89b-12d3-a456-426614174000', NOW(), NOW());

INSERT INTO public.templates (name, description, subject, body, json_vars, wrapper_id, sender_id, id, created_at, updated_at)
VALUES ('Template 1', 'Description 1', 'Subject 1', 'Body 1', '{"var1": "value1", "var2": "value2"}', '123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000', NOW(), NOW());

INSERT INTO public.notifications (event_name, template_id, notification_type, id, created_at, updated_at)
VALUES ('users.created', '123e4567-e89b-12d3-a456-426614174000', 'instant', '123e4567-e89b-12d3-a456-426614174000', NOW(), NOW());

INSERT INTO public.notifications (event_name, template_id, notification_type, id, created_at, updated_at)
VALUES ('films.new', '123e4567-e89b-12d3-a456-426614174000', 'scheduled', '2b4dcdc8-db56-4251-accc-adba10c03a47', NOW(), NOW());
"""  # noqa: E501
