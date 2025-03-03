from genral import make_vapi_call  # Ensure correct import
num=input("Enter a number:")
name=input("Enter your name:")
knowledge_id_doctor="75592415-b855-4c43-89fa-e35de31b5227"
knowledge_id_real_estate="c9844897-17fc-432b-99a3-1916853fe58c"

make_vapi_call(name,num,knowledge_id_doctor)
#     return {"message": "Form submitted successfully!", "call_result": result
