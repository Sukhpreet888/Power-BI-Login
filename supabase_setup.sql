-- Run in the Supabase SQL Editor.
-- If you already ran an earlier version, inspect existing objects before rerunning.

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  role text not null default 'user' check (role in ('admin', 'user'))
);

create table if not exists public.reports (
  role text primary key check (role in ('admin', 'user')),
  url text not null
);

insert into public.reports (role, url) values
('admin', 'https://app.powerbi.com/groups/444a8209-f144-47b4-bf7e-cb11e7fff1e1/reports/fd7dfe54-0e3e-463f-9134-a164b57530f2/664849b1fdc130364264?experience=power-bi'),
('user',  'https://app.powerbi.com/groups/me/reports/71fd7a21-6c6e-486c-a5da-7108a7078464/664849b1fdc130364264?experience=power-bi')
on conflict (role) do update set url = excluded.url;

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id) values (new.id)
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

alter table public.profiles enable row level security;
alter table public.reports enable row level security;

drop policy if exists "read own profile" on public.profiles;
create policy "read own profile" on public.profiles
  for select to authenticated using (auth.uid() = id);

drop policy if exists "read own role report" on public.reports;
create policy "read own role report" on public.reports
  for select to authenticated
  using (role = (select p.role from public.profiles p where p.id = auth.uid()));

-- Create users in Authentication > Users, then promote an admin from SQL Editor:
-- update public.profiles set role = 'admin'
-- where id = (select id from auth.users where email = 'your-admin-email@example.com');
