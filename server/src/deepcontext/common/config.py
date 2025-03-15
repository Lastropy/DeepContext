from dotenv import load_dotenv

print("Loading ENV Variables...")
load_dotenv("server/config/.env.development")
print("ENV Variables Loaded")