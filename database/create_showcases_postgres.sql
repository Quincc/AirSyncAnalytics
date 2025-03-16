-- Витрина активности пользователей
CREATE TABLE IF NOT EXISTS user_activity_summary AS
SELECT
    user_id,
    COUNT(session_id) AS total_sessions,
    AVG(EXTRACT(EPOCH FROM (end_time - start_time))) AS avg_session_duration,
    SUM(array_length(pages_visited, 1)) AS total_pages_visited,
    SUM(array_length(actions, 1)) AS total_actions
FROM UserSessions
GROUP BY user_id;

-- Витрина эффективности работы поддержки
CREATE TABLE IF NOT EXISTS support_performance AS
SELECT
    user_id,
    COUNT(ticket_id) AS total_tickets,
    AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) AS avg_resolution_time,
    COUNT(CASE WHEN status = 'closed' THEN 1 END) AS closed_tickets,
    AVG(array_length(messages, 1)) AS avg_messages_per_ticket
FROM SupportTickets
GROUP BY user_id;