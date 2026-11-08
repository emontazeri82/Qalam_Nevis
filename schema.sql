-- ============================================================
-- QALAM NEVIS DATABASE SCHEMA
-- PostgreSQL
-- ============================================================


-- ============================================================
-- UUID SUPPORT
-- ============================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- ============================================================
-- ROLES
-- Examples:
-- admin
-- editor
-- writer
-- ============================================================

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(30) NOT NULL,
    description TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_roles_code
        UNIQUE (code),

    CONSTRAINT ck_roles_code_nonblank
        CHECK (length(trim(code)) > 0)
);


-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Email is required for every user.
    -- authenticates using username.
    email VARCHAR(320) NOT NULL,

    username VARCHAR(80) NOT NULL,

    password_hash TEXT NOT NULL,

    display_name VARCHAR(160) NOT NULL,

    bio TEXT,

    preferred_language VARCHAR(2)
        NOT NULL
        DEFAULT 'en',

    is_active BOOLEAN
        NOT NULL
        DEFAULT true,

    last_login_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    CONSTRAINT ck_users_language
        CHECK (preferred_language IN ('en', 'fa')),

    CONSTRAINT ck_users_username_nonblank
        CHECK (length(trim(username)) > 0),

    CONSTRAINT ck_users_email_nonblank
        CHECK (length(trim(email)) > 0),

    CONSTRAINT ck_users_display_name_nonblank
        CHECK (length(trim(display_name)) > 0)
);


-- Case-insensitive username uniqueness

CREATE UNIQUE INDEX uq_users_username_lower
    ON users (lower(username));


-- Email is optional, but when supplied it must be unique.

CREATE UNIQUE INDEX uq_users_email_lower
    ON users (lower(email));


-- ============================================================
-- USER ↔ ROLE
-- Many-to-many relationship
-- ============================================================

CREATE TABLE user_roles (
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,

    CONSTRAINT pk_user_roles
        PRIMARY KEY (user_id, role_id),

    CONSTRAINT fk_user_roles_user
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user_roles_role
        FOREIGN KEY (role_id)
        REFERENCES roles (id)
        ON DELETE CASCADE
);


CREATE INDEX ix_user_roles_role_id
    ON user_roles (role_id);


-- ============================================================
-- CATEGORIES
--
-- Examples:
-- stories
-- reports
-- criticism
--
-- Archive should NOT be a category.
-- ============================================================

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    slug VARCHAR(80) NOT NULL,

    name_en VARCHAR(120) NOT NULL,
    name_fa VARCHAR(120) NOT NULL,

    sort_order INTEGER
        NOT NULL
        DEFAULT 0,

    is_active BOOLEAN
        NOT NULL
        DEFAULT true,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    CONSTRAINT uq_categories_slug
        UNIQUE (slug),

    CONSTRAINT ck_categories_slug_nonblank
        CHECK (length(trim(slug)) > 0),

    CONSTRAINT ck_categories_name_en_nonblank
        CHECK (length(trim(name_en)) > 0),

    CONSTRAINT ck_categories_name_fa_nonblank
        CHECK (length(trim(name_fa)) > 0)
);


-- ============================================================
-- TAGS
-- ============================================================

CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    slug VARCHAR(100) NOT NULL,

    name_en VARCHAR(120) NOT NULL,
    name_fa VARCHAR(120) NOT NULL,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    CONSTRAINT uq_tags_slug
        UNIQUE (slug),

    CONSTRAINT ck_tags_slug_nonblank
        CHECK (length(trim(slug)) > 0)
);


-- ============================================================
-- ARTICLES
--
-- This represents the conceptual article.
-- Language-specific content lives in article_translations.
-- ============================================================

CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    author_id UUID NOT NULL,

    category_id UUID NOT NULL,

    deleted_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    CONSTRAINT fk_articles_author
        FOREIGN KEY (author_id)
        REFERENCES users (id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_articles_category
        FOREIGN KEY (category_id)
        REFERENCES categories (id)
        ON DELETE RESTRICT
);


CREATE INDEX ix_articles_author_id
    ON articles (author_id);

CREATE INDEX ix_articles_category_id
    ON articles (category_id);

CREATE INDEX ix_articles_deleted_at
    ON articles (deleted_at);


-- ============================================================
-- ARTICLE ↔ TAG
-- Many-to-many relationship
-- ============================================================

CREATE TABLE article_tags (
    article_id UUID NOT NULL,
    tag_id UUID NOT NULL,

    CONSTRAINT pk_article_tags
        PRIMARY KEY (article_id, tag_id),

    CONSTRAINT fk_article_tags_article
        FOREIGN KEY (article_id)
        REFERENCES articles (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_article_tags_tag
        FOREIGN KEY (tag_id)
        REFERENCES tags (id)
        ON DELETE CASCADE
);


CREATE INDEX ix_article_tags_tag_id
    ON article_tags (tag_id);


-- ============================================================
-- MEDIA ASSETS
--
-- Images/files uploaded by writers/editors/admins.
-- ============================================================

CREATE TABLE media_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    uploaded_by_id UUID NOT NULL,

    storage_key VARCHAR(600) NOT NULL,

    original_filename VARCHAR(255) NOT NULL,

    mime_type VARCHAR(120) NOT NULL,

    size_bytes BIGINT NOT NULL,

    width INTEGER,
    height INTEGER,

    sha256 VARCHAR(64),

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    CONSTRAINT uq_media_assets_storage_key
        UNIQUE (storage_key),

    CONSTRAINT fk_media_assets_uploaded_by
        FOREIGN KEY (uploaded_by_id)
        REFERENCES users (id)
        ON DELETE RESTRICT,

    CONSTRAINT ck_media_assets_size
        CHECK (size_bytes >= 0),

    CONSTRAINT ck_media_assets_width
        CHECK (
            width IS NULL
            OR width > 0
        ),

    CONSTRAINT ck_media_assets_height
        CHECK (
            height IS NULL
            OR height > 0
        )
);


CREATE INDEX ix_media_assets_uploaded_by_id
    ON media_assets (uploaded_by_id);

CREATE INDEX ix_media_assets_sha256
    ON media_assets (sha256);


-- ============================================================
-- ARTICLE TRANSLATIONS
--
-- Each article can have:
--
-- one English version
-- one Farsi version
--
-- Each language can have its own publication status.
-- ============================================================

CREATE TABLE article_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    article_id UUID NOT NULL,

    language VARCHAR(2) NOT NULL,

    title VARCHAR(300) NOT NULL,

    slug VARCHAR(350) NOT NULL,

    summary TEXT,

    -- Structured rich-text editor document
    body_document JSONB
        NOT NULL
        DEFAULT '{}'::jsonb,

    -- Allows us to identify the editor/document format.
    editor_format VARCHAR(50)
        NOT NULL
        DEFAULT 'unselected',

    document_version INTEGER
        NOT NULL
        DEFAULT 1,

    -- Rendered/searchable versions
    body_html TEXT,
    body_text TEXT,

    cover_media_id UUID,

    -- Publishing workflow
    status VARCHAR(24)
        NOT NULL
        DEFAULT 'draft',

    submitted_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    archived_at TIMESTAMPTZ,

    last_edited_by_id UUID,

    -- Optimistic locking
    lock_version INTEGER
        NOT NULL
        DEFAULT 1,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),


    CONSTRAINT uq_article_translations_article_language
        UNIQUE (article_id, language),

    CONSTRAINT uq_article_translations_language_slug
        UNIQUE (language, slug),


    CONSTRAINT fk_article_translations_article
        FOREIGN KEY (article_id)
        REFERENCES articles (id)
        ON DELETE CASCADE,


    CONSTRAINT fk_article_translations_cover_media
        FOREIGN KEY (cover_media_id)
        REFERENCES media_assets (id)
        ON DELETE SET NULL,


    CONSTRAINT fk_article_translations_last_editor
        FOREIGN KEY (last_edited_by_id)
        REFERENCES users (id)
        ON DELETE SET NULL,


    CONSTRAINT ck_article_translations_language
        CHECK (
            language IN ('en', 'fa')
        ),


    CONSTRAINT ck_article_translations_status
        CHECK (
            status IN (
                'draft',
                'submitted',
                'in_review',
                'changes_requested',
                'approved',
                'rejected',
                'published',
                'archived'
            )
        ),


    CONSTRAINT ck_article_translations_title_nonblank
        CHECK (
            length(trim(title)) > 0
        ),


    CONSTRAINT ck_article_translations_slug_nonblank
        CHECK (
            length(trim(slug)) > 0
        ),


    CONSTRAINT ck_article_translations_document_version
        CHECK (
            document_version >= 1
        ),


    CONSTRAINT ck_article_translations_lock_version
        CHECK (
            lock_version >= 1
        )
);


CREATE INDEX ix_article_translations_article_id
    ON article_translations (article_id);

CREATE INDEX ix_article_translations_status
    ON article_translations (status);

CREATE INDEX ix_article_translations_cover_media_id
    ON article_translations (cover_media_id);

CREATE INDEX ix_article_translations_last_edited_by_id
    ON article_translations (last_edited_by_id);

CREATE INDEX ix_article_translations_published_at
    ON article_translations (published_at);


-- Useful for public article pages.
CREATE INDEX ix_article_translations_language_status
    ON article_translations (language, status);


-- ============================================================
-- EDITORIAL REVIEWS
--
-- Writer submits article
--       ↓
-- Editor/Admin reviews
--       ↓
-- approve / reject / request changes
-- ============================================================

CREATE TABLE editorial_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    article_translation_id UUID NOT NULL,

    reviewer_id UUID NOT NULL,

    decision VARCHAR(24) NOT NULL,

    comment TEXT,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    CONSTRAINT fk_editorial_reviews_translation
        FOREIGN KEY (article_translation_id)
        REFERENCES article_translations (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_editorial_reviews_reviewer
        FOREIGN KEY (reviewer_id)
        REFERENCES users (id)
        ON DELETE RESTRICT,

    CONSTRAINT ck_editorial_reviews_decision
        CHECK (
            decision IN (
                'approved',
                'changes_requested',
                'rejected'
            )
        )
);


CREATE INDEX ix_editorial_reviews_translation_id
    ON editorial_reviews (article_translation_id);

CREATE INDEX ix_editorial_reviews_reviewer_id
    ON editorial_reviews (reviewer_id);


-- ============================================================
-- ARTICLE STATUS HISTORY
--
-- Keeps an audit trail.
--
-- Example:
--
-- draft
-- submitted
-- in_review
-- changes_requested
-- submitted
-- approved
-- published
-- ============================================================

CREATE TABLE article_status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    article_translation_id UUID NOT NULL,

    changed_by_id UUID,

    old_status VARCHAR(24),

    new_status VARCHAR(24) NOT NULL,

    note TEXT,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    CONSTRAINT fk_article_status_history_translation
        FOREIGN KEY (article_translation_id)
        REFERENCES article_translations (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_article_status_history_user
        FOREIGN KEY (changed_by_id)
        REFERENCES users (id)
        ON DELETE SET NULL,

    CONSTRAINT ck_article_status_history_old_status
        CHECK (
            old_status IS NULL
            OR old_status IN (
                'draft',
                'submitted',
                'in_review',
                'changes_requested',
                'approved',
                'rejected',
                'published',
                'archived'
            )
        ),

    CONSTRAINT ck_article_status_history_new_status
        CHECK (
            new_status IN (
                'draft',
                'submitted',
                'in_review',
                'changes_requested',
                'approved',
                'rejected',
                'published',
                'archived'
            )
        )
);


CREATE INDEX ix_article_status_history_translation_id
    ON article_status_history (article_translation_id);

CREATE INDEX ix_article_status_history_changed_by_id
    ON article_status_history (changed_by_id);

CREATE INDEX ix_article_status_history_created_at
    ON article_status_history (created_at);


-- ============================================================
-- ARTICLE REVISIONS
--
-- Stores snapshots of article content.
--
-- This protects writers from losing previous versions and gives
-- editors/admins access to revision history.
-- ============================================================

CREATE TABLE article_revisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    article_translation_id UUID NOT NULL,

    edited_by_id UUID,

    revision_number INTEGER NOT NULL,

    title VARCHAR(300) NOT NULL,

    summary TEXT,

    body_document JSONB
        NOT NULL
        DEFAULT '{}'::jsonb,

    body_html TEXT,
    body_text TEXT,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT now(),

    CONSTRAINT fk_article_revisions_translation
        FOREIGN KEY (article_translation_id)
        REFERENCES article_translations (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_article_revisions_editor
        FOREIGN KEY (edited_by_id)
        REFERENCES users (id)
        ON DELETE SET NULL,

    CONSTRAINT uq_article_revisions_number
        UNIQUE (
            article_translation_id,
            revision_number
        ),

    CONSTRAINT ck_article_revisions_number
        CHECK (
            revision_number >= 1
        )
);


CREATE INDEX ix_article_revisions_translation_id
    ON article_revisions (article_translation_id);

CREATE INDEX ix_article_revisions_edited_by_id
    ON article_revisions (edited_by_id);


-- ============================================================
-- AUTOMATIC updated_at
--
-- DEFAULT now() only handles INSERT.
-- This trigger handles UPDATE.
-- ============================================================

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Roles
CREATE TRIGGER trg_roles_updated_at
BEFORE UPDATE ON roles
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Users
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Categories
CREATE TRIGGER trg_categories_updated_at
BEFORE UPDATE ON categories
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Tags
CREATE TRIGGER trg_tags_updated_at
BEFORE UPDATE ON tags
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Articles
CREATE TRIGGER trg_articles_updated_at
BEFORE UPDATE ON articles
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Media
CREATE TRIGGER trg_media_assets_updated_at
BEFORE UPDATE ON media_assets
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Article translations
CREATE TRIGGER trg_article_translations_updated_at
BEFORE UPDATE ON article_translations
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- ============================================================
-- INITIAL ROLES
-- ============================================================

INSERT INTO roles (code, description)
VALUES
    ('admin', 'Full administrative access'),
    ('editor', 'Reviews and manages submitted articles'),
    ('writer', 'Creates and submits articles')
ON CONFLICT (code) DO NOTHING;


-- ============================================================
-- INITIAL QALAM NEVIS CATEGORIES
-- ============================================================

INSERT INTO categories (
    slug,
    name_en,
    name_fa,
    sort_order
)
VALUES
    ('stories', 'Stories', 'داستان‌ها', 1),
    ('reports', 'Reports', 'گزارش‌ها', 2),
    ('criticism', 'Criticism', 'نقد', 3)
ON CONFLICT (slug) DO NOTHING;



