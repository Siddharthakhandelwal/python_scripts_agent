
import requests
def add_data(df, phone_number, name, authtokeny,id):
    auth_token = authtokeny
    url = f"https://api.vapi.ai/call/{id}"
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    while True:
        response = requests.get(url, headers=headers)
        trans = response.json()
        print(trans[ 'monitor']['listenUrl'])
        print(trans['transport'])
        print(trans['status'])
        if trans['status'] =='ended' :
            transcript= trans['transcript']
            break
                
    # Check if the phone number exists in the DataFrame
    if phone_number in df['Phone number'].values:
        # Locate the index of the existing row
        idx = df.index[df['Phone number'] == phone_number][0]
        # Update the existing row
        df.at[idx, 'Name'] = name
        df.at[idx, 'authtoken'] += f" {auth_token}"
        df.at[idx, 'summary'] += f" {transcript}"

    else:
        # Create a new row as a dictionary
        new_data = {
            'Phone number': phone_number,
            'Name': name,
            'authtoken': auth_token,
            'summary': transcript
        }
        # Append the new row to the DataFrame
        df.loc[len(df)] = new_data
        # df = df.append(new_data, ignore_index=True)
    return df


