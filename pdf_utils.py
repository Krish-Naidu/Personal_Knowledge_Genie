import PyPDF2

def extract_text_from_pdf(file_path):
	"""
	Extracts and returns text from a PDF file.
	Args:
		file_path (str): Path to the PDF file.
	Returns:
		str: Extracted text from the PDF.
	"""
	text = ""
	with open(file_path, 'rb') as file:
		reader = PyPDF2.PdfReader(file)
		for page in reader.pages:
			text += page.extract_text() or ""
	return text


# call the above function
print(extract_text_from_pdf("./docs/sample.pdf"))


