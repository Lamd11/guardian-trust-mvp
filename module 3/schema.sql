-- ============================================
-- SDG Dashboard Database Schema
-- PostgreSQL 14+
-- Author: Nishitha Thatha Anil
-- ============================================

-- Drop existing tables
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS likes CASCADE;
DROP TABLE IF EXISTS post_images CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS follows CASCADE;
DROP TABLE IF EXISTS user_challenges CASCADE;
DROP TABLE IF EXISTS challenge_sdg_mappings CASCADE;
DROP TABLE IF EXISTS challenges CASCADE;
DROP TABLE IF EXISTS indicators CASCADE;
DROP TABLE IF EXISTS targets CASCADE;
DROP TABLE IF EXISTS sdgs CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop existing enums
DROP TYPE IF EXISTS user_type CASCADE;
DROP TYPE IF EXISTS post_visibility CASCADE;
DROP TYPE IF EXISTS difficulty CASCADE;
DROP TYPE IF EXISTS age_group CASCADE;
DROP TYPE IF EXISTS repetition_period CASCADE;

-- ============================================
-- ENUMS
-- ============================================

CREATE TYPE user_type AS ENUM ('USER', 'EXPERT');
CREATE TYPE post_visibility AS ENUM ('PUBLIC', 'PRIVATE');
CREATE TYPE difficulty AS ENUM ('VERY_EASY', 'EASY', 'MEDIUM', 'HARD', 'VERY_HARD');
CREATE TYPE age_group AS ENUM ('ALL', 'YOUTH', 'ADULT', 'SENIOR', 'FAMILY');
CREATE TYPE repetition_period AS ENUM ('NONE', 'DAILY', 'WEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY');

-- ============================================
-- TABLES
-- ============================================

CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('user_' || replace(gen_random_uuid()::text, '-', '')),
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(200),
    avatar_url TEXT,
    bio TEXT,
    sdg_points INTEGER NOT NULL DEFAULT 0 CHECK (sdg_points >= 0),
    is_verified BOOLEAN NOT NULL DEFAULT false,
    verification_code_hash VARCHAR(255),
    verification_code_expires_at TIMESTAMP,
    password_reset_token VARCHAR(255),
    password_reset_expires_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    refresh_token TEXT,
    user_type user_type NOT NULL DEFAULT 'USER',
    password_setup_required BOOLEAN NOT NULL DEFAULT false,
    google_id VARCHAR(255) UNIQUE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_google_id ON users(google_id);
CREATE INDEX idx_users_user_type ON users(user_type);
CREATE INDEX idx_users_sdg_points ON users(sdg_points);

CREATE TABLE follows (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('follow_' || replace(gen_random_uuid()::text, '-', '')),
    follower_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    following_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_follow UNIQUE(follower_id, following_id)
);

CREATE INDEX idx_follows_follower_id ON follows(follower_id);
CREATE INDEX idx_follows_following_id ON follows(following_id);

CREATE TABLE sdgs (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('sdg_' || replace(gen_random_uuid()::text, '-', '')),
    sdg_number INTEGER NOT NULL UNIQUE CHECK (sdg_number >= 1 AND sdg_number <= 17),
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    color VARCHAR(7) NOT NULL,
    icon VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_sdgs_sdg_number ON sdgs(sdg_number);

CREATE TABLE targets (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('target_' || replace(gen_random_uuid()::text, '-', '')),
    sdg_id VARCHAR(50) NOT NULL REFERENCES sdgs(id) ON DELETE RESTRICT,
    target_number VARCHAR(10) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_targets_sdg_id ON targets(sdg_id);
CREATE UNIQUE INDEX idx_targets_target_number ON targets(target_number);

CREATE TABLE indicators (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('indicator_' || replace(gen_random_uuid()::text, '-', '')),
    target_id VARCHAR(50) NOT NULL REFERENCES targets(id) ON DELETE RESTRICT,
    sdg_id VARCHAR(50) NOT NULL REFERENCES sdgs(id) ON DELETE RESTRICT,
    indicator_number VARCHAR(20) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    measurement_unit VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_indicators_target_id ON indicators(target_id);
CREATE INDEX idx_indicators_sdg_id ON indicators(sdg_id);
CREATE UNIQUE INDEX idx_indicators_indicator_number ON indicators(indicator_number);

CREATE TABLE challenges (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('challenge_' || replace(gen_random_uuid()::text, '-', '')),
    challenge_number INTEGER NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    points INTEGER NOT NULL DEFAULT 0 CHECK (points >= 0),
    deadline TIMESTAMP NOT NULL,
    created_by_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    difficulty difficulty,
    estimated_time INTEGER,
    estimated_cost DECIMAL(10,2) CHECK (estimated_cost >= 0),
    is_repeatable BOOLEAN NOT NULL DEFAULT false,
    repetition_period repetition_period DEFAULT 'NONE',
    max_completions_per_user INTEGER CHECK (max_completions_per_user > 0),
    min_participants INTEGER CHECK (min_participants > 0),
    max_participants INTEGER CHECK (max_participants > 0),
    age_group age_group DEFAULT 'ALL',
    impact_unit VARCHAR(50),
    is_active BOOLEAN NOT NULL DEFAULT true,
    featured_until TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_challenges_challenge_number ON challenges(challenge_number);
CREATE INDEX idx_challenges_created_by_id ON challenges(created_by_id);
CREATE INDEX idx_challenges_difficulty ON challenges(difficulty);
CREATE INDEX idx_challenges_is_active ON challenges(is_active);
CREATE INDEX idx_challenges_deadline ON challenges(deadline);
CREATE INDEX idx_challenges_age_group ON challenges(age_group);
CREATE INDEX idx_challenges_featured_until ON challenges(featured_until);

CREATE TABLE challenge_sdg_mappings (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('mapping_' || replace(gen_random_uuid()::text, '-', '')),
    challenge_id VARCHAR(50) NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    sdg_id VARCHAR(50) NOT NULL REFERENCES sdgs(id) ON DELETE RESTRICT,
    target_id VARCHAR(50) REFERENCES targets(id) ON DELETE SET NULL,
    indicator_id VARCHAR(50) REFERENCES indicators(id) ON DELETE SET NULL,
    is_primary BOOLEAN NOT NULL DEFAULT false,
    challenge_code VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_challenge_sdg UNIQUE(challenge_id, sdg_id)
);

CREATE INDEX idx_mappings_challenge_id ON challenge_sdg_mappings(challenge_id);
CREATE INDEX idx_mappings_sdg_id ON challenge_sdg_mappings(sdg_id);
CREATE INDEX idx_mappings_target_id ON challenge_sdg_mappings(target_id);
CREATE INDEX idx_mappings_indicator_id ON challenge_sdg_mappings(indicator_id);
CREATE INDEX idx_mappings_challenge_code ON challenge_sdg_mappings(challenge_code);
CREATE INDEX idx_mappings_is_primary ON challenge_sdg_mappings(is_primary);

CREATE TABLE user_challenges (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('uc_' || replace(gen_random_uuid()::text, '-', '')),
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    challenge_id VARCHAR(50) NOT NULL REFERENCES challenges(id) ON DELETE RESTRICT,
    completed BOOLEAN NOT NULL DEFAULT false,
    completed_at TIMESTAMP,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity DECIMAL(10,2) CHECK (quantity >= 0),
    unit VARCHAR(50),
    location VARCHAR(200),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    impact_description TEXT,
    notes TEXT,
    proof_url TEXT,
    verified_by VARCHAR(50) REFERENCES users(id) ON DELETE SET NULL,
    verified_at TIMESTAMP,
    verification_notes TEXT,
    CONSTRAINT unique_user_challenge UNIQUE(user_id, challenge_id)
);

CREATE INDEX idx_user_challenges_user_id ON user_challenges(user_id);
CREATE INDEX idx_user_challenges_challenge_id ON user_challenges(challenge_id);
CREATE INDEX idx_user_challenges_completed ON user_challenges(completed);
CREATE INDEX idx_user_challenges_completed_at ON user_challenges(completed_at);
CREATE INDEX idx_user_challenges_location ON user_challenges(location);
CREATE INDEX idx_user_challenges_verified_by ON user_challenges(verified_by);

CREATE TABLE posts (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('post_' || replace(gen_random_uuid()::text, '-', '')),
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sdg_id VARCHAR(50) REFERENCES sdgs(id) ON DELETE SET NULL,
    caption TEXT NOT NULL,
    visibility post_visibility NOT NULL DEFAULT 'PUBLIC',
    is_challenge_post BOOLEAN NOT NULL DEFAULT false,
    challenge_id VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_sdg_id ON posts(sdg_id);
CREATE INDEX idx_posts_visibility ON posts(visibility);
CREATE INDEX idx_posts_is_challenge_post ON posts(is_challenge_post);
CREATE INDEX idx_posts_challenge_id ON posts(challenge_id);
CREATE INDEX idx_posts_created_at ON posts(created_at);

CREATE TABLE post_images (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('image_' || replace(gen_random_uuid()::text, '-', '')),
    post_id VARCHAR(50) NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    key VARCHAR(255) NOT NULL,
    url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_post_images_post_id ON post_images(post_id);

CREATE TABLE likes (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('like_' || replace(gen_random_uuid()::text, '-', '')),
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id VARCHAR(50) NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_post_like UNIQUE(user_id, post_id)
);

CREATE INDEX idx_likes_post_id ON likes(post_id);
CREATE INDEX idx_likes_user_id ON likes(user_id);

CREATE TABLE comments (
    id VARCHAR(50) PRIMARY KEY DEFAULT ('comment_' || replace(gen_random_uuid()::text, '-', '')),
    post_id VARCHAR(50) NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_id VARCHAR(50) REFERENCES comments(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_edited BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_parent_id ON comments(parent_id);
CREATE INDEX idx_comments_created_at ON comments(created_at);

-- ============================================
-- VIEWS
-- ============================================

CREATE OR REPLACE VIEW vw_sdg_summary AS
WITH challenge_stats AS (
    SELECT
        m.sdg_id,
        COUNT(DISTINCT m.challenge_id) as total_challenges,
        COUNT(uc.id) FILTER (WHERE uc.completed = true) as total_completions,
        COALESCE(SUM(uc.quantity) FILTER (WHERE uc.completed = true), 0) as total_impact
    FROM challenge_sdg_mappings m
    LEFT JOIN user_challenges uc ON uc.challenge_id = m.challenge_id
    WHERE m.is_primary = true
    GROUP BY m.sdg_id
),
post_stats AS (
    SELECT
        sdg_id,
        COUNT(*) as total_posts
    FROM posts
    WHERE sdg_id IS NOT NULL
    GROUP BY sdg_id
)
SELECT
    s.id,
    s.sdg_number,
    s.name,
    s.description,
    s.color,
    COALESCE(cs.total_challenges, 0) as total_challenges,
    COALESCE(cs.total_completions, 0) as total_completions,
    COALESCE(cs.total_impact, 0) as total_impact,
    COALESCE(ps.total_posts, 0) as total_posts
FROM sdgs s
LEFT JOIN challenge_stats cs ON cs.sdg_id = s.id
LEFT JOIN post_stats ps ON ps.sdg_id = s.id
ORDER BY s.sdg_number;

CREATE OR REPLACE VIEW vw_challenge_performance AS
WITH challenge_completion_stats AS (
    SELECT
        challenge_id,
        COUNT(*) FILTER (WHERE completed = true) as completion_count,
        COALESCE(SUM(quantity) FILTER (WHERE completed = true), 0) as total_impact,
        MAX(completed_at) as last_completed
    FROM user_challenges
    GROUP BY challenge_id
)
SELECT
    c.id,
    c.challenge_number,
    m.challenge_code,
    c.title,
    c.difficulty,
    c.points,
    s.name as sdg_name,
    COALESCE(ccs.completion_count, 0) as completion_count,
    COALESCE(ccs.total_impact, 0) as total_impact,
    c.impact_unit,
    ccs.last_completed,
    c.is_active
FROM challenges c
JOIN challenge_sdg_mappings m ON m.challenge_id = c.id AND m.is_primary = true
JOIN sdgs s ON m.sdg_id = s.id
LEFT JOIN challenge_completion_stats ccs ON ccs.challenge_id = c.id
ORDER BY completion_count DESC;

CREATE OR REPLACE VIEW vw_user_leaderboard AS
WITH user_challenge_stats AS (
    SELECT
        user_id,
        COUNT(*) FILTER (WHERE completed = true) as total_completions,
        COALESCE(SUM(quantity) FILTER (WHERE completed = true), 0) as total_impact,
        COUNT(DISTINCT challenge_id) FILTER (WHERE completed = true) as unique_challenges_completed,
        MAX(completed_at) as last_completion_date
    FROM user_challenges
    GROUP BY user_id
),
user_sdg_stats AS (
    SELECT
        uc.user_id,
        COUNT(DISTINCT m.sdg_id) as sdgs_contributed_to
    FROM user_challenges uc
    JOIN challenge_sdg_mappings m ON m.challenge_id = uc.challenge_id
    WHERE uc.completed = true
    GROUP BY uc.user_id
),
user_post_stats AS (
    SELECT
        user_id,
        COUNT(*) as total_posts
    FROM posts
    GROUP BY user_id
),
user_follower_stats AS (
    SELECT
        following_id as user_id,
        COUNT(*) as follower_count
    FROM follows
    GROUP BY following_id
),
user_following_stats AS (
    SELECT
        follower_id as user_id,
        COUNT(*) as following_count
    FROM follows
    GROUP BY follower_id
)
SELECT
    u.id,
    u.username,
    u.name,
    u.avatar_url,
    u.sdg_points as total_points,
    COALESCE(ucs.total_completions, 0) as total_completions,
    COALESCE(ucs.total_impact, 0) as total_impact,
    COALESCE(ucs.unique_challenges_completed, 0) as unique_challenges_completed,
    COALESCE(uss.sdgs_contributed_to, 0) as sdgs_contributed_to,
    COALESCE(ups.total_posts, 0) as total_posts,
    COALESCE(ufs.follower_count, 0) as follower_count,
    COALESCE(ufws.following_count, 0) as following_count,
    ucs.last_completion_date,
    u.created_at as joined_date
FROM users u
LEFT JOIN user_challenge_stats ucs ON ucs.user_id = u.id
LEFT JOIN user_sdg_stats uss ON uss.user_id = u.id
LEFT JOIN user_post_stats ups ON ups.user_id = u.id
LEFT JOIN user_follower_stats ufs ON ufs.user_id = u.id
LEFT JOIN user_following_stats ufws ON ufws.user_id = u.id
ORDER BY u.sdg_points DESC, total_completions DESC;

CREATE OR REPLACE VIEW vw_challenge_multi_sdg AS
SELECT
    c.id as challenge_id,
    c.challenge_number,
    c.title,
    c.description,
    c.difficulty,
    c.points,
    c.impact_unit,
    c.is_repeatable,
    c.repetition_period,
    c.is_active,
    ARRAY_AGG(DISTINCT m.sdg_id ORDER BY m.sdg_id) as sdg_ids,
    ARRAY_AGG(DISTINCT s.name ORDER BY m.sdg_id) as sdg_names,
    ARRAY_AGG(DISTINCT m.challenge_code ORDER BY m.sdg_id) as challenge_codes,
    COUNT(DISTINCT m.sdg_id) as sdg_count,
    c.created_at,
    c.updated_at
FROM challenges c
LEFT JOIN challenge_sdg_mappings m ON m.challenge_id = c.id
LEFT JOIN sdgs s ON s.id = m.sdg_id
GROUP BY c.id, c.challenge_number, c.title, c.description, c.difficulty,
         c.points, c.impact_unit, c.is_repeatable, c.repetition_period,
         c.is_active, c.created_at, c.updated_at;

CREATE OR REPLACE VIEW vw_user_feed AS
WITH post_likes AS (
    SELECT
        post_id,
        COUNT(*) as like_count
    FROM likes
    GROUP BY post_id
),
post_comments AS (
    SELECT
        post_id,
        COUNT(*) as comment_count
    FROM comments
    WHERE deleted_at IS NULL
    GROUP BY post_id
),
post_images_agg AS (
    SELECT
        post_id,
        ARRAY_AGG(url) as image_urls
    FROM post_images
    WHERE url IS NOT NULL
    GROUP BY post_id
)
SELECT
    p.id,
    p.user_id,
    u.username,
    u.name,
    u.avatar_url,
    p.caption,
    p.sdg_id,
    s.name as sdg_name,
    s.color as sdg_color,
    p.is_challenge_post,
    p.challenge_id,
    p.visibility,
    p.created_at,
    COALESCE(pl.like_count, 0) as like_count,
    COALESCE(pc.comment_count, 0) as comment_count,
    pia.image_urls
FROM posts p
JOIN users u ON u.id = p.user_id
LEFT JOIN sdgs s ON s.id = p.sdg_id
LEFT JOIN post_likes pl ON pl.post_id = p.id
LEFT JOIN post_comments pc ON pc.post_id = p.id
LEFT JOIN post_images_agg pia ON pia.post_id = p.id
ORDER BY p.created_at DESC;

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_sdgs_updated_at
    BEFORE UPDATE ON sdgs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_challenges_updated_at
    BEFORE UPDATE ON challenges
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_posts_updated_at
    BEFORE UPDATE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_comments_updated_at
    BEFORE UPDATE ON comments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
