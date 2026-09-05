from services.file_service import read_pdf



def parse_document(file_path):

    text = read_pdf(
        file_path
    )


    return {
        "content": text
    }