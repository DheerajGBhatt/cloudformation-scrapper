# URLs
clf_base_URL="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/"
sam_base_URL="https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/"
clf_url="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html"
test_url="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig-onfailure.html"
# sam resources
sam_api_http_url="sam-resource-httpapi.html"
sam_func_url="sam-resource-function.html" 
sam_graph_api_url="sam-resource-graphqlapi.html"
sam_layer_url="sam-resource-layerversion.html"
sam_table_url="sam-resource-simpletable.html"
sam_state_machine_url="sam-resource-statemachine.html"
sam_app_url="sam-resource-application.html"
sam_connecter_url="sam-resource-connector.html"
sam_api_url="sam-resource-api.html"
# clf resources
clf_func_url="aws-resource-lambda-function.html"
table_url="aws-resource-dynamodb-table.html"
bucket_url="aws-resource-s3-bucket.html"
sqs_url="aws-resource-sqs-queue.html"

improper_resource= [
    "-apigatewayv2-stage-stagevariables",
    "-events-rule-eventpattern",
   #  "-events-rule-target-deadletterconfig", 
   #  "-events-rule-target-retrypolicy",
    "-lambda-eventsourcemapping-destinationconfig",
    "-lambda-eventsourcemapping-sourceaccessconfigurations",
    "-sns-subscription-filterpolicy"
   #  "-scheduler-schedule-target-deadletterconfig"
   ]
fixed_resource={
    "-lambda-alias-provisionedconcurrencyconfig":"-lambda-alias-provisionedconcurrencyconfiguration",
    "-apigateway-usageplan-quota":"-apigateway-usageplan-quotasettings",
    "-apigateway-usageplan-throttle":"-apigateway-usageplan-throttlesettings",
    "-apigateway-stage-methodsettings":"-apigateway-stage-methodsetting",
    "-appsync-datasource-dynamodbconfig-deltasyncconfig":"-appsync-datasource-deltasyncconfig",
    "-appsync-functionconfiguration-runtime":"-appsync-functionconfiguration-appsyncruntime",
    "-appsync-resolver-runtime":"-appsync-resolver-appsyncruntime.html",
    "-appsync-graphqlapi-tags":"-appsync-graphqlapi-tag.html",
    "-stepfunctions-statemachine-definitions3location":"-stepfunctions-statemachine-s3location.html"
}
unique_type='List of [ String | RequestParameter ]'
types=["List","String","Boolean","Integer","List","Map","Object","JSON","Json"]