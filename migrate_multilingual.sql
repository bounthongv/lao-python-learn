-- Multilingual migration for Lao Python Learning Platform
-- Run this on PostgreSQL to add language support

-- 1. Add language column to lessons table
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS lang VARCHAR(5) DEFAULT 'lo';

-- 2. Create translations table for UI labels (optional, for future)
CREATE TABLE IF NOT EXISTS ui_translations (
    key VARCHAR(100) PRIMARY KEY,
    lo TEXT,
    en TEXT,
    th TEXT,
    zh TEXT
);

-- 3. Update existing lessons to have lang='lo'
UPDATE lessons SET lang = 'lo' WHERE lang IS NULL;

-- 4. Create index for language filtering
CREATE INDEX IF NOT EXISTS idx_lessons_lang ON lessons(lang, "order");

-- 5. Insert sample English translations for lessons (optional - for testing)
-- You can add more languages later by inserting into this table
-- INSERT INTO lessons (title, slug, content_markdown, example_code, "order", lang) VALUES
-- ('1. Python Basics', 'lesson-1-basics-en', '# Python Basics\n\n...', 'print("Hello Python")', 1, 'en'),
-- ('2. Conditions', 'lesson-2-conditions-en', '# Conditions\n\n...', 'if x > 0: print("positive")', 2, 'en');