# Power BI Streamlit Portal (Supabase backend)

## Files
- app.py                          Streamlit app
- supabase_setup.sql              Tables, trigger, RLS, report URLs (run first)
- seed_test_users.sql             Creates the two TEST users (run second)
- requirements.txt
- .streamlit/secrets.toml.example Copy to secrets.toml and fill in

## Setup
1. Supabase SQL Editor: run supabase_setup.sql, then seed_test_users.sql.
2. Copy .streamlit/secrets.toml.example -> .streamlit/secrets.toml
   and add your Project URL and anon key (Project Settings > API).
3. pip install -r requirements.txt
4. streamlit run app.py

## TEST credentials (change/delete before real use)
- Admin: admin@example.com / Admin@123456
- User:  user@example.com  / User@123456

Never put the service_role key in secrets.toml.
