-- ============================================
-- 标签功能数据库迁移脚本
-- ============================================
-- 说明：为家庭共享日历与任务管理系统添加标签功能
-- 执行方式：mysql -u username -p family_calendar < labels_migration.sql

USE family_calendar;

-- ============================================
-- 标签表
-- ============================================
CREATE TABLE IF NOT EXISTS labels (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '标签ID',
    group_id INT NOT NULL COMMENT '所属群组ID',
    name VARCHAR(50) NOT NULL COMMENT '标签名称',
    color VARCHAR(20) NOT NULL DEFAULT '#3B82F6' COMMENT '标签颜色（十六进制）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_group_id (group_id),
    UNIQUE KEY uk_group_name (group_id, name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标签表';

-- ============================================
-- 事件-标签关联表（多对多）
-- ============================================
CREATE TABLE IF NOT EXISTS event_labels (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '关联记录ID',
    event_id INT NOT NULL COMMENT '事件ID',
    label_id INT NOT NULL COMMENT '标签ID',
    INDEX idx_event_id (event_id),
    INDEX idx_label_id (label_id),
    UNIQUE KEY uk_event_label (event_id, label_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='事件-标签关联表';

-- ============================================
-- 任务-标签关联表（多对多）
-- ============================================
CREATE TABLE IF NOT EXISTS task_labels (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '关联记录ID',
    task_id INT NOT NULL COMMENT '任务ID',
    label_id INT NOT NULL COMMENT '标签ID',
    INDEX idx_task_id (task_id),
    INDEX idx_label_id (label_id),
    UNIQUE KEY uk_task_label (task_id, label_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务-标签关联表';

-- ============================================
-- 说明
-- ============================================
-- 1. 标签属于群组级别，同一群组内的事件和任务可共享标签
-- 2. 使用多对多关系，一个事件/任务可以有多个标签，一个标签可以关联多个事件/任务
-- 3. uk_group_name 唯一索引确保同一群组内标签名称不重复
-- 4. uk_event_label 和 uk_task_label 防止重复关联

