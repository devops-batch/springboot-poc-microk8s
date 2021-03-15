
import json
import boto3
import csv

def lambda_handler(event, context):
    error = None
    try: 
        print("event printing")
        #import pprint 
        #pprint.pprint(event)
        #print(event)
        #print(context)
        #print("Hello")
    
        request_name = event['context']['resource-path']
        print(request_name ,"request_name")
        print("Hello1")
        v_condition =' '
        v_msg = ' '
        response_object = {} 
        error_response = {}
        #default the response to SUCCESS
        response_object['statusCode'] = '200'
        def do_error_message(message, status='400'):
            error_response['message'] =message
            response_object['body'] = json.dumps(error_response)
            response_object['statusCode'] = status
            raise Exception('[{}] Something Bad Request. Please check the submitted request'.format(status))

        request_method = event['context']['http-method']
        request_query_parameters = event['params']['querystring']
        # request_query_parameters = event['queryStringParameters'] 
        print(request_query_parameters)
        #read the configuration file to get the metadata of the requested resource
        config_file = open('./config.json',) 
        parameter_json_contents = json.load(config_file)
        try:
            input_config = parameter_json_contents[request_name]
            print(input_config)
        except Exception as ERROR:
            print("Connection Issue: " , ERROR)
            return " is not configured in DEP"
        for input in input_config:
            v_query_parameters = input['query_parameters']
            v_response_col_names = input['response_col_names']
        v_request_query_parameters_keys = request_query_parameters.keys()
        v_expected_parameters_keys = v_query_parameters[0].keys()
        if set(v_request_query_parameters_keys).issubset(set(v_expected_parameters_keys)) :
            print("request parameters are valid")
        else :
            print("request parameters have extra fields")
            print(set(v_request_query_parameters_keys))
            print(set(v_expected_parameters_keys))
            return do_error_message(
                "Request found extra parameter(s) : "
                + str(list(set(v_request_query_parameters_keys) - set(v_expected_parameters_keys)))
            )
        queryString = ""
        i = 0
        
        for x in request_query_parameters :
            v_col_name = v_query_parameters[0][x]
            v_col_value = request_query_parameters[x]
            '''
            if i == 0:
                queryString = 'y["' + v_col_name + '"] == "' + v_col_value + '"'
            else:
                queryString = queryString + ' and y["' + v_col_name + '"] == "' + v_col_value + '"'
            i = i + 1
        '''
        s3 = boto3.resource('s3')
        BUCKET_NAME = 'aws-coe'
        key = 'api-gateway-poc/covid-fci-data.csv'
        local_file_name = '/tmp/covid-fci-data.csv'
        s3.Bucket(BUCKET_NAME).download_file(key, local_file_name)
        data = []
        with open(local_file_name, encoding='ISO-8859-1') as csvf:
            csvReader = csv.DictReader(csvf)
            for rows in csvReader: 
                jsonStr = json.dumps(rows)
                data.append(jsonStr)
        returnVal = []
        print("%s--%s" %(v_col_name,v_col_value))
        for x in data:
            y = json.loads(x)
            finaldict = {}
            if (y[v_col_name]).strip() == v_col_value:
                for z in v_response_col_names:
                    finaldict[z] = (y[z]).strip()
                returnVal.append(finaldict)
        return returnVal
    except Exception as ERROR:
        print("Connection Issue: " , ERROR)
        return " API is not working"
