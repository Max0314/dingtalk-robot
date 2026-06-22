CREATE TABLE IF NOT EXISTS dingtalk_robot_event (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    conversation_id VARCHAR(191) NOT NULL DEFAULT '',
    conversation_title VARCHAR(256) NOT NULL DEFAULT '',
    conversation_type VARCHAR(32) NOT NULL DEFAULT '',
    sender_nick VARCHAR(128) NOT NULL DEFAULT '',
    sender_id VARCHAR(128) NOT NULL DEFAULT '',
    robot_code VARCHAR(191) NOT NULL DEFAULT '',
    message_text VARCHAR(1000) NOT NULL DEFAULT '',
    command VARCHAR(64) NOT NULL DEFAULT '',
    handle_status VARCHAR(32) NOT NULL DEFAULT '',
    response_text VARCHAR(2000) NOT NULL DEFAULT '',
    payload_json MEDIUMTEXT NULL,
    created_at DATETIME NOT NULL,
    KEY idx_dingtalk_robot_event_created (created_at),
    KEY idx_dingtalk_robot_event_conversation (conversation_id),
    KEY idx_dingtalk_robot_event_sender (sender_id)
);

CREATE TABLE IF NOT EXISTS dingtalk_robot_send_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    business_type VARCHAR(64) NOT NULL DEFAULT '',
    business_id VARCHAR(128) NOT NULL DEFAULT '',
    target_type VARCHAR(32) NOT NULL DEFAULT 'group',
    target_name VARCHAR(256) NOT NULL DEFAULT '',
    conversation_id VARCHAR(191) NOT NULL DEFAULT '',
    robot_code VARCHAR(191) NOT NULL DEFAULT '',
    msg_key VARCHAR(128) NOT NULL DEFAULT '',
    process_query_key VARCHAR(256) NOT NULL DEFAULT '',
    send_status VARCHAR(32) NOT NULL DEFAULT '',
    error_text VARCHAR(2000) NOT NULL DEFAULT '',
    created_at DATETIME NOT NULL,
    KEY idx_dingtalk_robot_send_created (created_at),
    KEY idx_dingtalk_robot_send_business (business_type, business_id),
    KEY idx_dingtalk_robot_send_conversation (conversation_id)
);
