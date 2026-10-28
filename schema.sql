CREATE TABLE roles (
  id UUID NOT NULL,
  code VARCHAR(30) NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  CONSTRAINT pk_roles PRIMARY KEY (id),
  CONSTRAINT uq_roles_code UNIQUE (code)
);
CREATE TABLE users (
  id UUID NOT NULL,
  email VARCHAR(320) NOT NULL,
  username VARCHAR(80) NOT NULL,
  password_hash TEXT NOT NULL,
  display_name VARCHAR(160) NOT NULL,
  bio TEXT,
  preferred_language VARCHAR(2) DEFAULT 'en' NOT NULL,
  is_active BOOLEAN DEFAULT true NOT NULL,
  last_login_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  CONSTRAINT pk_users PRIMARY KEY (id),
  CONSTRAINT ck_users_language CHECK (preferred_language IN ('en', 'fa')),
  CONSTRAINT ck_users_nonblank_identity
  CHECK (
    length(trim(email)) > 0
    AND length(trim(username)) > 0
  )
  
);
CREATE UNIQUE INDEX uq_users_email_lower
    ON users (lower(email));

CREATE UNIQUE INDEX uq_users_username_lower
    ON users (lower(username));

CREATE TABLE user_roles(
  user_id UUID NOT NULL,
  role_id UUID NOT NULL,
  CONSTRAINT pk_user_roles PRIMARY KEY (user_id, role_id),
  CONSTRAINT fk_user_roles_user_id_users
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,

  CONSTRAINT fk_user_roles_role_id_roles
  FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
);

CREATE TABLE categories (
  id UUID NOT NULL,
  slug VARCHAR(80) NOT NULL,
  name_en VARCHAR(120) NOT NULL,
  name_fa VARCHAR(120) NOT NULL,
  sort_order INTEGER DEFAULT 0 NOT NULL,
  is_active BOOLEAN DEFAULT true NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  CONSTRAINT pk_categories PRIMARY KEY (id),
  CONSTRAINT uq_categories_slug UNIQUE (slug)
);

CREATE TABLE tags (
  id UUID NOT NULL,
  slug VARCHAR(100) NOT NULL,
  name_en VARCHAR(120) NOT NULL,
  name_fa VARCHAR(120) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  CONSTRAINT pk_tags PRIMARY KEY (id),
  CONSTRAINT uq_tags_slug UNIQUE (slug)
);

CREATE TABLE articles(
  id UUID NOT NULL,
  author_id UUID NOT NULL,
  category_id UUID NOT NULL,
  deleted_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  CONSTRAINT pk_articles PRIMARY KEY (id),
  CONSTRAINT fk_articles_author_id_users
  FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE RESTRICT,
  CONSTRAINT fk_articles_category_id_categories
  FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE RESTRICT
);

CREATE INDEX ix_articles_author_id
ON articles (author_id);

CREATE INDEX ix_articles_category_id
ON articles (category_id);

CREATE TABLE media_assets (
  id UUID NOT NULL,
  uploaded_by_id UUID NOT NULL,
  storage_key VARCHAR(600) NOT NULL,
  original_filename VARCHAR(255) NOT NULL,
  mime_type VARCHAR(120) NOT NULL,
  size_bytes BIGINT NOT NULL,
  width INTEGER,
  height INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  sha256 VARCHAR(64),
  CONSTRAINT pk_media_assets PRIMARY KEY (id),
  CONSTRAINT uq_media_assets_storage_key UNIQUE (storage_key),
  CONSTRAINT fk_media_assets_uploaded_by_id_users
  FOREIGN KEY (uploaded_by_id) REFERENCES users (id) ON DELETE RESTRICT,
  CONSTRAINT ck_media_assets_size CHECK (size_bytes >= 0),
  CONSTRAINT ck_media_assets_width CHECK (width IS NULL OR width > 0),
  CONSTRAINT ck_media_assets_height CHECK (height IS NULL OR height > 0)
);

CREATE INDEX ix_media_assets_uploaded_by_id
ON media_assets (uploaded_by_id);

CREATE INDEX ix-media_assetes_sha256
ON media_assets (sha256);

CREATE TABLE article_translations(
  id UUID NOT NULL,
  article_id UUID NOT NULL,
  language VARCHAR(2) NOT NULL,
  title VARCHAR(300) NOT NULL,
  slug VARCHAR(350) NOT NULL,
  summary TEXT,
  body_document JSONB DEFAULT '{}'::jsonb NOT NULL,
  editor_format VARCHAR(50) DEFAULT 'unselected' NOT NULL,
  document_version INTEGER DEFAULT 1 NOT NULL,
  body_html TEXT,
  body_text TEXT,
  cover_media_id UUID,
  status VARCHAR(24) DEFAULT 'draft' NOT NULL,
  submitted_at TIMESTAMP WITH TIME ZONE,
  published_at TIMESTAMP WITH TIME ZONE,
  archived_at TIMESTAMP WITH TIME ZONE,
  last_edited_by_id UUID,
  lock_version INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAuLT now() NOT NULL,
  CONSTRAINT pk_article_translations PRIMARY KEY (id),

  CONSTRAINT uq_article_translations_article_id
  UNIQUE (article_id, language),

  CONSTRAINT uq_article_translations_language
  UNIQUE (language, slug),
);



