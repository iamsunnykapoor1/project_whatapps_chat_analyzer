import pandas as pd
import re
def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMapm]{2}\s-\s"

    messages = re.split(pattern, data)[1:]  # [1:]   skip first empty item
    dates = re.findall(pattern, data)

    # we have made a dataframe having user_message and message date
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # convert message_date type

    df['message_date'] = (
        df['message_date']
        .astype(str)
        .str.replace('\u202f', ' ', regex=False)
        .str.replace(' - ', '', regex=False)
        .str.replace(' -', '', regex=False)
        .str.strip()
    )

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        dayfirst=True,  # dayfirst=True means dates are interpreted as dd/mm/yyyy.
        errors='coerce'  # converts invalid dates into NaT instead of raising errors.
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # for splitting the user_name and message
    users = []
    messages = []

    for msg in df['user_message']:
        entry = msg.split(': ', 1)  # why 1  becouse message can contain, Rahul: Meet at 10:30 please
        # so jo pehla colon aayae ga usko sae split karega

        if len(entry) == 2:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
