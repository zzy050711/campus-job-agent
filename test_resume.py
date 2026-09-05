from memory import get_user_profile
from services.doc_service import generate_resume


profile = get_user_profile()

result = generate_resume(profile)

print(result)