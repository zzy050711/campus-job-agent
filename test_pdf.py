from services.file_service import read_pdf



text = read_pdf(
    "resume.pdf"
)


print(text)