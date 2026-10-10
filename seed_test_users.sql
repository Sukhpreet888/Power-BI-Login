-- TEST USERS ONLY. Run AFTER supabase_setup.sql, in the Supabase SQL Editor.
-- Delete these users (Authentication > Users) before real use.

create extension if not exists pgcrypto with schema extensions;

do $$
declare
  rec record;
  new_id uuid;
begin
  for rec in
    select * from (values
      ('admin@example.com', 'Admin@123456', 'admin'),
      ('user@example.com',  'User@123456',  'user')
    ) as t(email, pw, role)
  loop
    if exists (select 1 from auth.users where email = rec.email) then
      continue;
    end if;

    new_id := gen_random_uuid();

    insert into auth.users (
      instance_id, id, aud, role, email, encrypted_password, email_confirmed_at,
      raw_app_meta_data, raw_user_meta_data, created_at, updated_at,
      confirmation_token, email_change, email_change_token_new, recovery_token
    ) values (
      '00000000-0000-0000-0000-000000000000', new_id, 'authenticated', 'authenticated',
      rec.email, extensions.crypt(rec.pw, extensions.gen_salt('bf')), now(),
      '{"provider":"email","providers":["email"]}', '{}', now(), now(),
      '', '', '', ''
    );

    insert into auth.identities (
      id, user_id, provider_id, identity_data, provider,
      last_sign_in_at, created_at, updated_at
    ) values (
      gen_random_uuid(), new_id, new_id::text,
      jsonb_build_object('sub', new_id::text, 'email', rec.email, 'email_verified', true),
      'email', now(), now(), now()
    );

    -- profile row is created by the trigger; set the role
    update public.profiles set role = rec.role where id = new_id;
  end loop;
end $$;

-- Verify
select u.email, p.role
from auth.users u join public.profiles p on p.id = u.id
where u.email in ('admin@example.com', 'user@example.com');
