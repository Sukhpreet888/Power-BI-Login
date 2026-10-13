# Power BI Streamlit Portal (Supabase)

## Fix for `StreamlitSecretNotFoundError`

The app expects this exact file path relative to `app.py`:

`.streamlit/secrets.toml`

The downloaded project includes `.streamlit/secrets.toml.example` as a template. Copy it to `secrets.toml` in the same `.streamlit` folder, then replace the placeholders with your actual Supabase values.

Example:
```toml
SUPABASE_URL = "https://YOUR-PROJECT-REF.supabase.co"
SUPABASE_KEY = "YOUR-ANON-OR-PUBLISHABLE-KEY"
```

Find both values in Supabase Dashboard > Project Settings > API. Use the anon/public or publishable key, not the `service_role`/secret key.

## Run on Windows / Anaconda Prompt

1. Extract this ZIP.
2. Open Anaconda Prompt and change directory to the extracted folder, for example:
   `cd "C:\Users\ASUS\Downloads\power_bi_streamlit_portal_fixed"`
3. Create the secrets file:
   - Open `.streamlit` inside the project.
   - Copy `secrets.toml.example`.
   - Rename the copy to `secrets.toml` (make sure Windows has not added `.txt`).
   - Edit it and enter the real Supabase URL and key.
4. Install packages:
   `python -m pip install -r requirements.txt`
5. Start the app:
   `python -m streamlit run app.py`

## Supabase database setup

1. Open Supabase > SQL Editor.
2. Run `supabase_setup.sql`.
3. To use the included demo accounts, run `seed_test_users.sql` after setup. This is optional and for testing only.
4. Demo login:
   - Admin: `admin@example.com` / `Admin@123456`
   - User: `user@example.com` / `User@123456`

If those accounts already exist with different passwords, the seed script does not reset their passwords. Delete the test accounts from Supabase Authentication > Users and rerun the seed script, or create/reset them through Supabase.

## Important

- Never put the Supabase `service_role` key in Streamlit secrets.
- The report links in `supabase_setup.sql` are the links supplied with this project. Confirm that they point to the intended reports.
- This app opens the assigned Power BI report in a new browser destination; it does not bypass Power BI sharing/licensing or embed the report inside the Streamlit page.
- Change or remove demo credentials before production use.
