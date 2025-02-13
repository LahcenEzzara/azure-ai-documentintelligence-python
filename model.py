import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

# Load environment variables from .env file
load_dotenv()

endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("FORM_RECOGNIZER_KEY")
model_id = os.getenv("CUSTOM_MODEL_ID")
formUrl = os.getenv("DOCUMENT_URL")

document_intelligence_client  = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Make sure your document's type is included in the list of document types the custom model can analyze
poller = document_intelligence_client.begin_analyze_document(
    model_id, AnalyzeDocumentRequest(url_source=formUrl)
)
result = poller.result()

for idx, document in enumerate(result.documents):
    print("--------Analyzing document #{}--------".format(idx + 1))
    print("Document has type {}".format(document.doc_type))
    print("Document has confidence {}".format(document.confidence))
    print("Document was analyzed by model with ID {}".format(result.model_id))
    for name, field in document.fields.items():
        print("......found field of type '{}' with value '{}' and with confidence {}".format(field.type, field.content, field.confidence))

# iterate over tables, lines, and selection marks on each page
for page in result.pages:
    print("\nLines found on page {}".format(page.page_number))
    for line in page.lines:
        print("...Line '{}'".format(line.content.encode('utf-8')))
    for word in page.words:
        print(
            "...Word '{}' has a confidence of {}".format(
                word.content.encode('utf-8'), word.confidence
            )
        )
    if page.selection_marks:
        for selection_mark in page.selection_marks:
            print(
                "...Selection mark is '{}' and has a confidence of {}".format(
                    selection_mark.state, selection_mark.confidence
                )
            )

for i, table in enumerate(result.tables):
    print("\nTable {} can be found on page:".format(i + 1))
    for region in table.bounding_regions:
        print("...{}".format(i + 1, region.page_number))
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
                cell.row_index, cell.column_index, cell.content.encode('utf-8')
            )
        )
print("-----------------------------------")