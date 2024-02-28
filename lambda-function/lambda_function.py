import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisitorCounter')

def lambda_handler(event, context):
    response = table.get_item(Key={
        'id': '1'
    })

    visits = response.get('Item', {}).get('visits', 0)
    visits += 1

    # Use a conditional expression to update the counter only if the current visits value matches the expected value
    table.update_item(
        Key={'id': '1'},
        UpdateExpression='SET visits = :new_visits',
        ConditionExpression='visits = :current_visits',
        ExpressionAttributeValues={
            ':current_visits': visits - 1,  # The expected current value
            ':new_visits': visits,           # The new value to set
        }
    )

    return visits
