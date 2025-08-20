import pandas as pd
import streamlit as st




col1, col2, col3 = st.columns([0.1,4,1])
with col3:
    st.image('https://www.netimpactlimited.com/wp-content/uploads/2024/04/NetImpact-Logo-Final-Web-2.png')
with col2:
    st.subheader(f'Agent Performance Report📈')

# Agent file upload
raw_login = st.file_uploader('Please upload the Login hour file here')
if raw_login:
    st.success('File received successfully')

# Roaster File Upload
raw_advisor_File_data = st.file_uploader(f'Please upload the Advisor file')
if raw_advisor_File_data:
    st.success('File received successfully')    

if raw_login and raw_advisor_File_data:
    raw_login_1 = pd.ExcelFile(raw_login,engine='openpyxl')
    raw_advisor_File_data_1 = pd.ExcelFile(raw_advisor_File_data,engine='openpyxl')
    
    data = raw_login_1.parse('Main File')
    data_list = raw_advisor_File_data_1.parse('Sheet1')
    


    # Droping the column if they exists
    try:
        data.drop(['Emp ID', 'OLMS ID', 'Emp Name','TL Name', 'Shift ', 'LOB', 'CareManager Available', 'Follow Up','Productive (Avail+Follow Up)','Production (Avail+FollowUP+Tea+Lunch)'],axis=1,inplace=True)
    except:
        pass

    # changing to the upper case 

    data_list['AGENT ID'] = data_list['AGENT ID'].astype(str).str.upper()
    data['Emp ID']=data['Agent Email'].astype(str).str.split('@').str[0].str.upper()
    
    # performing the murger
    data = data.merge(data_list[['AGENT ID', 'AGENT NAME', 'TL Name', 'Sub-LOB']],
                  left_on='Emp ID',
                  right_on='AGENT ID',
                  how='left'
                  )
    # removing the NaN values
    data.dropna(subset=['AGENT ID'],inplace=True)

    
    # Convert datetime.time to timedelta
    data['LUNCH_BREAK'] = pd.to_timedelta(data['LUNCH_BREAK'])
    data['TEA_BREAK'] = pd.to_timedelta(data['TEA_BREAK'])


    data['CareManager Available'] = data['AVAILABLE'].apply(
        lambda t: pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second) if pd.notnull(t) else pd.NaT
    )
    data['Follow Up'] = data['FOLLOW_UP'].apply(
        lambda t: pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second) if pd.notnull(t) else pd.NaT
    )

    data['Productive (Avail+Follow Up)'] = data['CareManager Available'] + data['Follow Up']

    data['Production (Avail+FollowUP+Tea+Lunch)'] = data['Productive (Avail+Follow Up)'] + data['LUNCH_BREAK'] + data['TEA_BREAK'] 
    data['CareManager Available'] = data['CareManager Available'].astype(str).str.split('days').str[1]
    data['Follow Up'] = data['Follow Up'].astype(str).str.split('days').str[1]
    data['Productive (Avail+Follow Up)'] = data['Productive (Avail+Follow Up)'].astype(str).str.split('days').str[1]
    data['Production (Avail+FollowUP+Tea+Lunch)'] = data['Production (Avail+FollowUP+Tea+Lunch)'].astype(str).str.split('days').str[1]
    data['Date'] = data['Date'].astype(str).str.split(' ').str[0]

    # reseting the index
    data.reset_index(drop=True,inplace=True)

    # vizulalizing DataFram
    st.dataframe(data)