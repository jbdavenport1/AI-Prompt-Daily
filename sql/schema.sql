create extension if not exists pgcrypto;

create table if not exists prompts (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    category text not null,
    subcategory text,
    audience text,
    tool text not null,
    prompt_text text not null,
    why_it_works text,
    how_to_customize text,
    expected_output text,
    difficulty text default 'beginner',
    tags text[],
    active boolean default true,
    last_used_at timestamptz,
    times_used integer default 0,
    created_at timestamptz default now()
);

create table if not exists skills (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    category text not null,
    lesson_text text not null,
    example_prompt text,
    level text default 'beginner',
    estimated_minutes integer default 3,
    active boolean default true,
    last_used_at timestamptz,
    times_used integer default 0,
    created_at timestamptz default now()
);

create table if not exists issues (
    id uuid primary key default gen_random_uuid(),
    issue_date date not null unique,
    subject text not null,
    html_content text not null,
    text_content text,
    status text default 'draft',
    sent_at timestamptz,
    created_at timestamptz default now()
);

create table if not exists issue_headlines (
    id uuid primary key default gen_random_uuid(),
    issue_id uuid references issues(id) on delete cascade,
    title text not null,
    url text not null,
    source text,
    summary text,
    rank_score numeric,
    created_at timestamptz default now()
);

create table if not exists issue_prompts (
    id uuid primary key default gen_random_uuid(),
    issue_id uuid references issues(id) on delete cascade,
    prompt_id uuid references prompts(id),
    created_at timestamptz default now()
);

create table if not exists issue_skills (
    id uuid primary key default gen_random_uuid(),
    issue_id uuid references issues(id) on delete cascade,
    skill_id uuid references skills(id),
    created_at timestamptz default now()
);

create table if not exists subscribers (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    full_name text,
    status text default 'active',
    plan text default 'free',
    stripe_customer_id text,
    stripe_subscription_id text,
    created_at timestamptz default now()
);
