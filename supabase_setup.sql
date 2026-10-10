-- Run in Supabase: SQL Editor

-- 1. Profiles: one row per auth user, holds the role
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  role text not null default 'user' check (role in ('admin', 'user'))
);

-- 2. Reports: role -> Power BI URL
create table public.reports (
  role text primary key check (role in ('admin', 'user')),
  url  text not null
);

insert into public.reports (role, url) values
('admin', 'https://app.powerbi.com/groups/444a8209-f144-47b4-bf7e-cb11e7fff1e1/reports/fd7dfe54-0e3e-463f-9134-a164b57530f2/664849b1fdc130364264?experience=power-bi'),
('user',  'https://app.powerbi.com/groups/me/reports/71fd7a21-6c6e-486c-a5da-7108a7078464/664849b1fdc130364264?experience=power-bi');

-- 3. Auto-create a 'user' profile whenever someone signs up
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id) values (new.id);
  return new;
end; $$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- 4. Row-level security
alter table public.profiles enable row level security;
alter table public.reports  enable row level security;

-- Users can read only their own profile (no update policy => they cannot change their own role)
create policy "read own profile" on public.profiles
  for select to authenticated using (auth.uid() = id);

-- Users can read only the report URL for their own role
create policy "read own role report" on public.reports
  for select to authenticated
  using (role = (select p.role from public.profiles p where p.id = auth.uid()));

-- 5. Create users in Dashboard > Authentication > Users, then promote an admin:
-- update public.profiles set role = 'admin'
--   where id = (select id from auth.users where email = 'you@example.com');
