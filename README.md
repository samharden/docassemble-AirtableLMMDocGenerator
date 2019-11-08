This is a document generation utility for the Airtable Legal Matter Management base. 
The original template is here (free): https://airtable.com/templates/legal/expSOFU7KC5yav5TR/legal-matter-management 
I've modified the template for purposes of this package, 
and you can get that version here: https://airtable.com/shrUfrmYivppjGXuf 

Note that the modified version has a 'Document types' table, so that DA can draw from 
it to list the types of documents you can create. Based on what document type you choose, 
DA loads the required template and gets the required interview file. So far I have 
added Letter and Contract as internal options to DA with templates. 

You will need to write both the interview files and the templates for the other 
document types yourself. You can do it, I believe in you.

If you want to add a new document type please be aware you will need to add it 
both in Airtable and DA. 

I haven't fully tested the file upload functionality, since Airtable requires a URL 
from which to download the file into the table and I'm working locally (AT can't get 
a URL beginning with 'localhost'). 

Enjoy responsibly.