from docassemble.base.util import get_config
from docassemble.base.util import DAObject, DAList
## Assuming you've added your airtable creds into the Config YAML:
at_api_key = get_config('AIRTABLE API KEY')
at_base_lmm = get_config('AT BASE LMM')

## Need to install package airtable-python-wrapper for this ##
import airtable
from airtable import Airtable

import requests

matter_table = Airtable(at_base_lmm, 'Matters', api_key=at_api_key)
intake_table = Airtable(at_base_lmm, 'Intake copy', api_key=at_api_key)
documents_table = Airtable(at_base_lmm, 'Documents', api_key=at_api_key)
tasks_table = Airtable(at_base_lmm, 'Tasks', api_key=at_api_key)
document_type_table = Airtable(at_base_lmm, 'Document Types', api_key=at_api_key)
client_table = Airtable(at_base_lmm, 'Clients', api_key=at_api_key)


def get_matters():
  show_this = []
  for rec in matter_table.get_all():
    matter_id = rec['id']
    matter_short_name = rec['fields']['Client ... Issue']
    show_this.append(tuple((matter_id, matter_short_name)))

  return show_this

def get_doctypes():
  show_this = []
  another_list = []
  for rec in document_type_table.get_all():
    doc_id = rec['id']
    name = rec['fields']['Name']

    show_this.append(tuple((doc_id, name)))

  return show_this

def search_matters_by_id(name):
  rec_to_ret = matter_table.get(name)

  return rec_to_ret['fields']['Client']

def get_client_name_by_id(client_id):
  rec_to_ret = client_table.get(client_id[0])
  return rec_to_ret['fields']['Name']

def get_client_address_by_id(client_id):
  rec_to_ret = client_table.get(client_id[0])
  try: 
    street_ad = rec_to_ret['fields']['Mailing address']
  except Exception as e:
    street_ad = ''
  try: 
    city = rec_to_ret['fields']['City']
  except Exception as e:
    city = ''
  try:
    state = rec_to_ret['fields']['State']
  except Exception as e:
    state = ''
  try:
    zip_c = rec_to_ret['fields']['Zip']
  except Exception as e:
    zip_c = ''
  
  address_dict = {
                  'street_ad': street_ad,
                  'city': city,
                  'state': state,
                  'zip_c': zip_c,
                  }
  return address_dict

def search_docs_by_id(name):
  rec_to_ret = document_type_table.get(name)
  return rec_to_ret['fields']['Name']

def dnld_doc_by_id(name):
  rec_to_ret = document_type_table.get(name)
  response = requests.get(rec_to_ret['fields']['Attachments'][0]['url'])
  with open (str(name)+'.docx', 'wb') as f:
    f.write(response.content)
  return f

def upload_file_to_documents(file, f_type, description, related_matter, doc_title):
  record = {
              "Document": doc_title,
              "Related matter": [related_matter],
              "Type": [f_type],
              "Description": description,
              "File": [
                        {
                          "url": file
                        }
                      ]
            }
                       
  documents_table.insert(record)


def get_fields_from_intake():
  show_this = {}
  
  intake_obj = DAObject('intake_obj')
  for rec in intake_table.get_all():
    for field in rec['fields']:
      if str(field) not in show_this.keys():
        # variable_to_add = str(field).replace(' ', '_').replace('-', '')
        if 'Email' in str(field):
          dt = 'email'
        elif 'Date' in str(field):
          dt = 'date'
        else: 
          dt = ''
        show_this[str(field)] = {'question': str(field), 'label': str(field), 'dt': dt }
  return show_this
  